def select_features(filename_features, path, estimator, X, y, params):
    from sklearn.feature_selection import RFECV
    from sklearn.feature_selection import SelectKBest, chi2, mutual_info_regression
    import xgboost as xgb
    import pandas as pd
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
        
        all_df = pd.DataFrame()
        all_df = rfecv_df.merge(features_df, on='Feature')
        all_df = all_df.merge(boruta_df, on='Feature')
        all_df = all_df.merge(importance_df, on='Feature', how='outer')
        save_obj(all_df, filename_features)
    return(all_df)