def shap_vals(X_train, shap_values):
    """
    create simple drawing ou of shap values
    see
    https://shap.readthedocs.io/en/latest/
    args:
        X_tarin : X data
        shap_values
    return:
        k2 : shap values modified
    """
    import numpy as np
    import pandas as pd
        
    shap_v = pd.DataFrame(shap_values)
    feature_list = X_train.columns
    shap_v.columns = feature_list
    df_v = X_train.copy().reset_index().drop('index',axis=1)
    
    # Determine the correlation in order to plot with different colors
    corr_list = list()
    for i in feature_list:
        b = np.corrcoef(shap_v[i],df_v[i])[1][0]
        corr_list.append(b)

    corr_df = pd.concat([pd.Series(feature_list),pd.Series(corr_list)],axis=1).fillna(0)
    # Make a data frame. Column 1 is the feature, and Column 2 is the correlation coefficient
    corr_df.columns  = ['Variable','Corr']
    corr_df['Sign'] = np.where(corr_df['Corr']>0,'red','blue')
    
    shap_abs = np.abs(shap_v)
    k=pd.DataFrame(shap_abs.mean()).reset_index()
    k.columns = ['Variable','SHAP_abs']
    k2 = k.merge(corr_df,left_on = 'Variable',right_on='Variable',how='inner')
    k2 = k2.sort_values(by='SHAP_abs',ascending = True)
    k2 = k2[k2['SHAP_abs']>0]
    return(k2)