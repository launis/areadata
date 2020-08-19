def print_examples(data, X, new, target, clst, shap_values, col_num=5, n=5):
    from OrderedSet import OrderedSet
    import numpy as np
    import pandas as pd

    shap_v = pd.DataFrame(shap_values[clst])
    feature_list = X.columns
    shap_v.columns = feature_list
    df_v = X.copy().reset_index().drop('index',axis=1)
    
    # Determine the correlation in order to plot with different colors
    corr_list = list()
    for i in feature_list:
        b = np.corrcoef(shap_v[i],df_v[i])[1][0]
        corr_list.append(b)

    corr_df = pd.concat([pd.Series(feature_list),pd.Series(corr_list)],axis=1).fillna(0)
    # Make a data frame. Column 1 is the feature, and Column 2 is the correlation coefficient
    corr_df.columns  = ['Variable','Corr']    
    shap_abs = np.abs(shap_v)
    k=pd.DataFrame(shap_abs.mean()).reset_index()
    k.columns = ['Variable','SHAP_abs']
    k2 = k.merge(corr_df,left_on = 'Variable',right_on='Variable',how='inner')
    k2 = k2.sort_values(by='SHAP_abs',ascending = False)
    col_list=k2['Variable'].head(col_num).to_list()

    new_x = list(OrderedSet(X.columns.to_list())- (OrderedSet(X.columns.to_list())-OrderedSet(col_list)))
    new_df=pd.concat([data[new],X[new_x]], axis=1)

    show_df = new_df[new_df[target]==clst].sample(n=n).copy()
    show_df = np.round(show_df,2)
    return(show_df, col_list)