def select_share(features_dict, column, minshare, included):
    from OrderedSet import OrderedSet
    included_new  = list(features_dict[features_dict[column]>minshare].index)
    included.extend(included_new)
    included_new = list(OrderedSet(included))
    return(included_new)

def select_logical(features_dict, column, included):
    from OrderedSet import OrderedSet
    included_new  = list(features_dict[features_dict[column]==True].index)
    included.extend(included_new)
    included_new = list(OrderedSet(included))
    return(included_new)


def select_columns(features_df, filename_selected_features=None, path=None, 
                                              total_gain = 0, 
                                              permutation_importance = 0, 
                                              kval = 0):

    import pandas as pd
    import os
    from OrderedSet import OrderedSet
    from saveloadmodel import save_obj, load_obj
    
    selected_cols = None
    
    if filename_selected_features != None:
        filename_selected_features = os.path.join(path, filename_selected_features)
        selected_cols = load_obj(filename_selected_features)
    
    
    if not isinstance(selected_cols, pd.DataFrame):
        
        included = []
    
        column = 'total_gain'
        minshare = total_gain
        included = select_share(features_df, column, minshare, included)
    
        column = 'Shap_permutation_importance'
        minshare = permutation_importance
        included = select_share(features_df, column, minshare, included)
    
        minshare = kval
        if 'mutual_info_regression' in features_df.columns:
            column = 'mutual_info_regression'
        else:
            column = 'chi2'
        included = select_share(features_df, column, minshare, included)  
    
        column = 'Boruta support'
        included = select_logical(features_df, column, included)
    
        column = 'RFECV Suport'
        included = select_logical(features_df, column, included)
    
    
        cols =  OrderedSet(features_df.loc[included]['Feature'].tolist())
        column = 'Cor support'
        cols = list(cols - OrderedSet(list(features_df[features_df[column]==False]['Feature'])))
        selected_cols = pd.DataFrame(cols, columns=['Feature'])
        if filename_selected_features != None:
            save_obj(selected_cols, filename_selected_features)
        
    return(selected_cols)

def select_features(filename_features, shap_data, path, estimator, X, y, params):
    from sklearn.feature_selection import RFECV
    from sklearn.feature_selection import SelectKBest, chi2, mutual_info_regression
    import xgboost as xgb
    import pandas as pd
    import numpy as np
    from boruta import BorutaPy
    import os
    
    from saveloadmodel import save_obj, load_obj
    
    filename_features = os.path.join(path, filename_features)
    
    all_df = load_obj(filename_features)
    if not isinstance(all_df , pd.DataFrame):
        #Kbest
        if params['objective'].startswith('reg'):
            kbest_score_func = mutual_info_regression
            score_func_name = 'mutual_info_regression'
        else:
            kbest_score_func = chi2
            score_func_name = 'chi2'
        if kbest_score_func == chi2:
            X=X.abs().copy()    
        k='all'
        selector = SelectKBest(kbest_score_func, k=k)
        selector.fit(X, y)
        features_names = X.columns
        features_scores = selector.scores_
        dict = {'Feature': features_names, score_func_name : features_scores}
        features_df = pd.DataFrame(dict)
        features_df.sort_values(score_func_name, inplace=True, ascending=False)
        features_df.reset_index(drop=True, inplace=True)
        
        
        #Importance
        importance_df = pd.DataFrame()
        for importance_type in ['weight', 'gain', 'cover', 'total_gain', 'total_cover']:
            importance = estimator.get_score(importance_type=importance_type)
            temp = pd.DataFrame.from_dict(importance, orient='index', columns=[importance_type])
            importance_df = pd.concat([importance_df, temp], axis=1)
        importance_df.reset_index(inplace=True)
        importance_df.rename(columns={'index':'Feature'}, inplace=True)        
        
            #native Xgboost not supported everywhere
        if params['objective'].startswith('reg'):
            sklearn_estimator=xgb.XGBRegressor(**params)
        else:
            sklearn_estimator=xgb.XGBClassifier(**params)
    
        #rfecv    
        selector = RFECV(sklearn_estimator, step=1, cv=5)
        selector = selector.fit(X, y)
    
        dict = {'Feature': features_names, "RFECV Ranking" : selector.ranking_, "RFECV Suport" : selector.support_, }
        rfecv_df = pd.DataFrame(dict)
        rfecv_df.sort_values("RFECV Ranking", inplace=True, ascending=True)
        rfecv_df.reset_index(drop=True, inplace=True)
        
        
        selector = BorutaPy(sklearn_estimator, n_estimators='auto', verbose=0, random_state=1)
        selector.fit(X.to_numpy(), y.to_numpy())
        
        dict = {'Feature': features_names, "Boruta Ranking" : selector.ranking_, "Boruta support" : selector.support_ }
        boruta_df = pd.DataFrame(dict)
        boruta_df.sort_values("Boruta Ranking", inplace=True, ascending=True)
        boruta_df.reset_index(drop=True, inplace=True)
        
        corr = X.corr()
        columns = np.full((corr.shape[0],), True, dtype=bool)
        cor_number = [0 for i in range(len(X.columns))]
        for i in range(corr.shape[0]):
            for j in range(i+1, corr.shape[0]):
                if abs(corr.iloc[i,j]) > 0.85 :
                    if columns[j]:
                        columns[j] = False
                        cor_number[j] = i
        d = {'Feature' : X.columns, 'Cor support' : columns, 'Corr feature' : X.columns[cor_number]}
        corr_df=pd.DataFrame(data=d)
        corr_df.loc[corr_df['Corr feature'] == corr_df.iloc[0]['Corr feature'], 'Corr feature']=""
        
        
        shap_sum = shap_data['shap_values_Partition'].abs.values.mean(axis=0)
        partition_importance_df = pd.DataFrame([X.columns.tolist(), shap_sum.tolist()]).T
        partition_importance_df.columns = ['Feature', 'Shap_partition_importance']

        shap_sum = shap_data['shap_values_Permutation'].abs.values.mean(axis=0)
        permutation_importance_df = pd.DataFrame([X.columns.tolist(), shap_sum.tolist()]).T
        permutation_importance_df.columns = ['Feature', 'Shap_permutation_importance']

        
        all_df = pd.DataFrame()
        all_df = rfecv_df.merge(features_df, on='Feature')
        all_df = all_df.merge(boruta_df, on='Feature')
        all_df = all_df.merge(corr_df, on='Feature')
        all_df = all_df.merge(partition_importance_df, on='Feature')
        all_df = all_df.merge(permutation_importance_df, on='Feature')
        all_df = all_df.merge(importance_df, on='Feature', how='outer')
        
        save_obj(all_df, filename_features)
    return(all_df)

def select_first_features(filename, path, t, train, test, initial_params, test_size, numeric_features, categorical_features, scaled = False):
    from sklearn.feature_selection import RFECV
    from sklearn.feature_selection import SelectKBest, chi2, mutual_info_regression
    import xgboost as xgb

    from sklearn.model_selection import train_test_split
    import pandas as pd
    import numpy as np
    from boruta import BorutaPy

    import os
    
    from prepare_and_scale_data import prepare_and_scale_data
    from saveloadmodel import load_obj
    
    params = {}
    data, train_scaled, train_non_scaled, test, test_scaled, test_non_scaled= prepare_and_scale_data(train, test, numeric_features, categorical_features)
    y = data[t]

    if scaled:
        X_train, X_validate, y_train, y_validate = train_test_split(train_scaled, y, test_size=test_size, random_state=42)
        X = train_scaled
        X_test = test_scaled
    else:
        X_train, X_validate, y_train, y_validate = train_test_split(train_non_scaled, y, test_size=test_size, random_state=42)
        X = train_non_scaled
        X_test = test_non_scaled


    
    filename_model =  filename + t + '_model' +'.pkl'
    filename_model = os.path.join(path, filename_model)
    estimator = load_obj(filename_model)
  
    if initial_params['objective'].startswith('reg'):
        kbest_score_func = mutual_info_regression
        score_func_name = 'mutual_info_regression'
    else:
        kbest_score_func = chi2
        score_func_name = 'chi2'
    if kbest_score_func == chi2:
        X=X.abs().copy()    
    k='all'
    selector = SelectKBest(kbest_score_func, k=k)
    selector.fit(X, y)
    features_names = X.columns
    features_scores = selector.scores_
    dict = {'Feature': features_names, score_func_name : features_scores}
    features_df = pd.DataFrame(dict)
    features_df.sort_values(score_func_name, inplace=True, ascending=False)
    features_df.reset_index(drop=True, inplace=True)
        
        
    #Importance
    importance_df = pd.DataFrame()
    for importance_type in ['weight', 'gain', 'cover', 'total_gain', 'total_cover']:
            importance = estimator.get_score(importance_type=importance_type)
            temp = pd.DataFrame.from_dict(importance, orient='index', columns=[importance_type])
            importance_df = pd.concat([importance_df, temp], axis=1)
    
    importance_df.reset_index(inplace=True)
    importance_df.rename(columns={'index':'Feature'}, inplace=True)        
        
    #native Xgboost not supported everywhere
    if initial_params['objective'].startswith('reg'):
            sklearn_estimator=xgb.XGBRegressor(**params)
    else:
            sklearn_estimator=xgb.XGBClassifier(**params)
    
    #rfecv    
    selector = RFECV(sklearn_estimator, step=1, cv=5, verbose = 1)
    selector = selector.fit(X, y)
    
    dict = {'Feature': features_names, "RFECV Ranking" : selector.ranking_, "RFECV Suport" : selector.support_, }
    rfecv_df = pd.DataFrame(dict)
    rfecv_df.sort_values("RFECV Ranking", inplace=True, ascending=True)
    rfecv_df.reset_index(drop=True, inplace=True)
        
        
    selector = BorutaPy(sklearn_estimator, n_estimators='auto', verbose=1, random_state=1)
    selector.fit(X.to_numpy(), y.to_numpy())
        
    dict = {'Feature': features_names, "Boruta Ranking" : selector.ranking_, "Boruta support" : selector.support_ }
    boruta_df = pd.DataFrame(dict)
    boruta_df.sort_values("Boruta Ranking", inplace=True, ascending=True)
    boruta_df.reset_index(drop=True, inplace=True)
        
    corr = X.corr()
    columns = np.full((corr.shape[0],), True, dtype=bool)
    cor_number = [0 for i in range(len(X.columns))]
    for i in range(corr.shape[0]):
        for j in range(i+1, corr.shape[0]):
            if abs(corr.iloc[i,j]) > 0.85 :
                if columns[j]:
                    columns[j] = False
                    cor_number[j] = i
    d = {'Feature' : X.columns, 'Cor support' : columns, 'Corr feature' : X.columns[cor_number]}
    corr_df=pd.DataFrame(data=d)
    corr_df.loc[corr_df['Corr feature'] == corr_df.iloc[0]['Corr feature'], 'Corr feature']=""
        
        
    all_df = pd.DataFrame()
    all_df = rfecv_df.merge(features_df, on='Feature')
    all_df = all_df.merge(boruta_df, on='Feature')
    all_df = all_df.merge(corr_df, on='Feature')
    all_df = all_df.merge(importance_df, on='Feature', how='outer')
        
    return(all_df)