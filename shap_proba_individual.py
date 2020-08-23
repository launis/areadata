
 
def print_individual_waterfall(data, target, X, shap_expected_value, shap_values, id_col, pnro):

    import shap 
    shap.initjs()
    clst = data[data[id_col]==pnro][target].item()
    idx = data[data[id_col]==pnro].index.item()
    shap.waterfall_plot(shap_expected_value[clst], shap_values[clst][idx], X.iloc[idx,:])
    


def print_reason(data, X, shap_values, shap_expected_value, mymodel, clst, pnro, id_col):
    #define a function to convert logodds to probability for multi-class 

    idx = data[data[id_col]==pnro].index.item()
    X_rand = X[X.index==idx].copy()
    #generate predictions for our row of data and do conversion
    pred_val = mymodel.predict(X_rand)
    probas = mymodel.predict_proba(X_rand)[clst]
    base_val = shap_expected_value[clst]

    print('Id: ', pnro)
    print('Value: ', clst)
    print('Base value/mean: ', base_val)
    print('Prediction value: ', pred_val)
    print('Probapility of value in class:', probas, '\n')
