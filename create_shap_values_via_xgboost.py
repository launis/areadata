
def create_shap_values_via_xgboost(path,
                                   filename,
                                   train,
                                   test,
                                   target,
                                   initial_params,
                                   numeric_features=[],
                                   categorical_features=[],
                                   scaled=False, 
                                   test_size = 0.2,
                                   Skfold=False,
                                   Verbose = False,
                                   testing = True):
    

    import pandas as pd
    import time
    import os
    import sklearn.metrics

    from shap_Xboost import shap_Xboost
    from create_prediction import create_prediction
    from select_features import select_features
    from select_features import select_columns
    from OrderedSet import OrderedSet
    from saveloadmodel import load_obj
    

    shap_data ={}
    model_params = {}
    model_list = {}
    features_dict = {}
    selected_columns_dict = {}

    y = {}
    y_test_pred = {}
    
    for t in target:
        params = initial_params.copy()
        data = pd.DataFrame()
        features_df = pd.DataFrame()
        filename = filename[:100]
        filename_features =  filename + t + '_features' +'.pkl'
        filename_selected_features =  filename + t + '_selected_features' +'.pkl'
        filename_shap =  filename + t + '_shap' +'.pkl'
        filename_model =  filename + t + '_model' +'.pkl'
        start_time = time.time()
        

        print(t)
                
        filename_sm = os.path.join(path, filename_model)
        model_features = load_obj(filename_sm)
            
        if model_features != None:
            numeric_features = model_features['numeric_features']
            categorical_features = model_features['categorical_features']
      
        data, X_train, y_train, test, X_test, y_test, model, params = create_prediction(filename_model,
                          path,
                          train,
                          test,
                          t,
                          params= params,
                          numeric_features=numeric_features,
                          categorical_features=categorical_features,
                          scaled=scaled,
                          test_size = test_size,
                          Skfold = Skfold,
                          Verbose = Verbose,
                          testing = testing)
    
        
        shap_dt = shap_Xboost(filename_shap, path, model, X_train, y_train)
        
        features_df = select_features(filename_features, shap_dt, path, model, X_train, y_train, params)

        selected_columns = select_columns(features_df, filename_selected_features, path)

        
        shap_data[t] = shap_dt
        model_list[t] = model
        model_params[t] = params
        features_dict[t] = features_df
        selected_columns_dict[t] = selected_columns
        y[t] = y_train
        y_test_pred[t] = pd.Series(y_test,name=t)
        print()
        if params['objective'].startswith('reg'):
            print("RMSE: ", sklearn.metrics.mean_squared_error(y[t],y_test_pred[t]))
        else:
            print(sklearn.metrics.classification_report(y[t],y_test_pred[t]))
        print()
        print("--- %s seconds ---" % (time.time() - start_time))
        print()
        #note predicted values with saved models do not match, only when all done from scartch work
    return(data, X_train, y, test, X_test, y_test_pred, model_list, model_params, shap_data, features_dict, selected_columns_dict)