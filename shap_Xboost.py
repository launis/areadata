def shap_Xboost(filename_shap, path, model, X):

    import shap
    import os
    
    from saveloadmodel import save_obj, load_obj

    filename_shap = os.path.join(path, filename_shap)
    
    data = load_obj(filename_shap)
    if data == None:
        explainer = shap.TreeExplainer(model, X)
        shap_values = explainer(X)

        data = {
            'explainer': explainer,
            'shap_values': shap_values,
            }

        save_obj(data, filename_shap)
    else:
        explainer = data['explainer']
        shap_values = data['shap_values']


    return(explainer, shap_values)