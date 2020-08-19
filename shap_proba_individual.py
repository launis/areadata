def shap_proba_individual(explainer, mymodel, data, target, X, id_col, pnro, log = False):
    
    import shap
    import pandas as pd

    df = pd.DataFrame()
    dfadd = pd.DataFrame()
    clst = data[data[id_col]==pnro][target].item()
    idx = data[data[id_col]==pnro].index.item()
    X_rand = X[X.index==idx].copy()

    shap_values = explainer.shap_values(X.iloc[idx])
    shap.initjs()
    if mymodel.get_xgb_params()['objective'] == 'reg:squarederror':
        if log:
            display(shap.force_plot(explainer.expected_value, shap_values, X_rand, link='logit'))
        else:
            display(shap.force_plot(explainer.expected_value, shap_values, X_rand))
        df = pd.DataFrame(data=shap_values)
    else:
        for which_class in range(0,len(data[target].unique())):
            if log:
                display(shap.force_plot(explainer.expected_value[which_class], shap_values[which_class], X_rand, link='logit'))
            else:
                display(shap.force_plot(explainer.expected_value[which_class], shap_values[which_class], X_rand))
        for i in range(0,len(data[target].unique())):
            dfadd = pd.DataFrame(data=shap_values[i], columns=X.columns, index=[i])
            df = pd.concat([df, dfadd], axis = 0)
    df = df.transpose()

    return(df, X_rand, clst)

def print_individual(df,pnro, clst):
    
    import pandas as pd
    import numpy as np
    
    individual_df = pd.DataFrame(df[clst])
    individual_df.reset_index(inplace=True)
    individual_df.columns=[pnro,'SHAP_abs']
    individual_df['Sign'] = np.where(individual_df['SHAP_abs']>0,'red','blue')
    individual_df.loc[:,'SHAP_abs'] = np.abs(individual_df['SHAP_abs'])
    individual_df.sort_values(by='SHAP_abs', ascending=True, inplace=True)
    individual2=individual_df[individual_df['SHAP_abs']!=0].copy()
    colorlist = individual2['Sign']

    individual2.tail(15).plot.barh(x=pnro,y='SHAP_abs',color = colorlist, title= clst, figsize=(5,6),legend=False)
    
 
def print_individual_waterfall(data, target, X, shap_expected_value, shap_values, id_col, pnro):

    import shap 
    shap.initjs()
    clst = data[data[id_col]==pnro][target].item()
    idx = data[data[id_col]==pnro].index.item()
    shap.waterfall_plot(shap_expected_value[clst], shap_values[clst][idx], X.iloc[idx,:])
    
def print_reason(X_rand, explainer, shap_values, mymodel, clst):
    #define a function to convert logodds to probability for multi-class 
    def logodds_to_proba(logodds):
        import numpy as np
        return np.exp(logodds)/np.exp(logodds).sum()

    #generate predictions for our row of data and do conversion
    logodds = mymodel.predict(X_rand, output_margin=True)
    probas = mymodel.predict_proba(X_rand)
    which_class = clst
    base_val = explainer.expected_value[which_class]
    pred_val = explainer.expected_value[which_class] + shap_values[which_class][0].sum() #delta between base value and pred value
    converted_prob_val = logodds_to_proba(logodds)[0][which_class]
    proba = probas[0][which_class]

    print('Class: ',which_class)
    print('Base value: ', base_val)
    print('Prediction value: ', pred_val)
    print('Converted Proba value:', converted_prob_val)
    print('Proba value:', proba, '\n')
