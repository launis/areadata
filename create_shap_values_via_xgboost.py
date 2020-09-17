
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


    from shap_Xboost import shap_Xboost
    from create_prediction import create_prediction
    from select_features import select_features

    shap_values ={}
    explainer_list= {}
    model_params = {}
    model_list = {}
    features_dict = {}

    y = {}
    y_test_pred = {}
    
    for t in target:
        params = initial_params.copy()
        data = pd.DataFrame()
        features_df = pd.DataFrame()
        filename_features =  filename + t + '_features' +'.pkl'
        filename_shap =  filename + t + '_shap' +'.pkl'
        filename_model =  filename + t + '_model' +'.pkl'
        start_time = time.time()
        

        print(t)
        
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
    
        
        expl, shap_val= shap_Xboost(filename_shap, path, model, X_train)
        
        features_df = select_features(filename_features, path, model, X_train, y_train, params)
        
        shap_values[t] = shap_val
        
        explainer_list[t] = expl
        
        model_list[t] = model
        model_params[t] = params
        
        features_dict[t] = features_df

        y[t] = y_train
        y_test_pred[t] = pd.Series(y_test,name=t)
        print("--- %s seconds ---" % (time.time() - start_time))
        print()
        #note predicted values with saved models do not match, only when all done from scartch work
    return(data, X_train, y, test, X_test, y_test_pred, model_list, model_params, explainer_list, shap_values, features_dict)
        