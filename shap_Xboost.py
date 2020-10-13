def shap_Xboost(filename_shap, path, model, X, y):

    import shap
    import os
    import xgboost
    
    from saveloadmodel import save_obj, load_obj

    filename_shap = os.path.join(path, filename_shap)
    
    shap_data = load_obj(filename_shap)
    if shap_data == None:
        
        f = lambda x: model.predict(xgboost.DMatrix(x), output_margin=True, validate_features=False)
    
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(X)
        expected_value = explainer.expected_value
        shap_interaction_values = explainer.shap_interaction_values(X)

        bg = shap.maskers.Partition(shap.utils.sample(X,100))
        explainer = shap.explainers.Partition(f, bg)
        shap_values_Partition = explainer(X)
        
        clustering = shap.utils.hclust(X, y)
    
        masker = shap.maskers.Partition(X, clustering=clustering)
        explainer = shap.explainers.Permutation(f,  masker)
        shap_values_Permutation = explainer(X)
        
        
        shap_data = {
            'shap_values': shap_values,
            'expected_value': expected_value,
            'shap_interaction_values' : shap_interaction_values,
            'shap_values_Partition': shap_values_Partition,
            'shap_values_Permutation': shap_values_Permutation,
            'clustering' : clustering,
            }

        save_obj(shap_data, filename_shap)
    else:
        shap_values = shap_data['shap_values']
        expected_value = shap_data['expected_value']
        shap_interaction_values = shap_data['shap_interaction_values']
        shap_values_Partition = shap_data['shap_values_Partition']
        shap_values_Permutation = shap_data['shap_values_Permutation']
        clustering = shap_data['clustering']



    return(shap_data)