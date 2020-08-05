def shap_tree(X_train, y_train, params):
    """
    create shap values
    see
    https://shap.readthedocs.io/en/latest/
    args:
        X_train : X data
        y_train : y
        params : xgboost parameters
    return:
        explainer: shap model
        shap_values : shap values 
        shap_interaction_values : shap interaction values
        shap_expected_value : shap expected values
    """
    import shap
    import xgboost as xgb

    #current versions do not support XGboost
    #this means that we need to make some tricks
    #and use sklearn xgboost
    if params['objective'] == 'reg:squarederror':
        thismodel = xgb.XGBRegressor(**params)
    if params['objective'] == 'multi:softmax':
        thismodel = xgb.XGBClassifier(**params)
        
    mymodel = thismodel.fit(X_train, y_train)
    mybooster = mymodel.get_booster()

    model_bytearray = mybooster.save_raw()[4:]
    def myfun(self=None):
        return model_bytearray
    mybooster.save_raw = myfun


    explainer = shap.TreeExplainer(mybooster,feature_perturbation='tree_path_dependent')
    shap_values = explainer.shap_values(X_train)
    shap_interaction_values = explainer.shap_interaction_values(X_train)
    shap_expected_value = explainer.expected_value

 
    return(explainer, shap_values, shap_interaction_values, shap_expected_value)