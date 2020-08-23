def shap_Xboost(filename_model, filename_shap, path, data, target, params, X):
    
    import shap
    import xgboost as xgb
    import os
    import pickle
    import numpy as np

    filename_model = os.path.join(path, filename_model)
    if os.access(filename_model, os.R_OK):
        print('load model')
        mymodel = pickle.load(open(filename_model, "rb"))        
        
    else:
        print('Create model')
        if params['objective'] == 'reg:squarederror':
            thismodel = xgb.XGBRegressor(**params)
        if params['objective'] == 'multi:softmax':
            thismodel = xgb.XGBClassifier(**params)
        if params['objective'] == 'multi:softprob':
            thismodel = xgb.XGBClassifier(**params)
        
        mymodel = thismodel.fit(X, data[target])
        mymodel.set_params(**params)
        pickle.dump(mymodel, open(filename_model, "wb"))


    filename_shap = os.path.join(path, filename_shap)
    if os.access(filename_shap, os.R_OK):
        print('load shap files')
        npzfile=np.load(filename_shap)
        if  npzfile['shap_expected_value'].ndim == 0:
            shap_values=npzfile['shap_values']
            shap_interaction_values = npzfile['shap_interaction_values']
            shap_expected_value=npzfile['shap_expected_value']
        else:
            shap_values=list(npzfile['shap_values'])
            shap_interaction_values = list(npzfile['shap_interaction_values'])
            shap_expected_value=list(npzfile['shap_expected_value'])
    else:
        print('Create shap files')
        mybooster = mymodel.get_booster()  
        model_bytearray = mybooster.save_raw()[4:]
        def myfun(self=None):
            return model_bytearray
        mybooster.save_raw = myfun

        explainer = shap.TreeExplainer(mybooster,feature_perturbation='tree_path_dependent')
    
        shap_values = explainer.shap_values(X)
        shap_interaction_values = explainer.shap_interaction_values(X)
        shap_expected_value = explainer.expected_value
        np.savez(filename_shap, shap_values=shap_values, shap_interaction_values=shap_interaction_values, shap_expected_value=shap_expected_value)
    return(mymodel, shap_values, shap_interaction_values, shap_expected_value)