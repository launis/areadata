def create_example_df(data, X, included_columns, shap_index, shap_values, col_num=5):
    from OrderedSet import OrderedSet
    import numpy as np
    import pandas as pd

    shap_v = pd.DataFrame(shap_values[shap_index])
    feature_list = X.columns
    shap_v.columns = feature_list
    df_v = X.copy().reset_index().drop('index',axis=1)
    X = X.iloc[list(data.index.values.tolist())]

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
    new_df=pd.concat([data[included_columns],X[new_x]], axis=1)
    return(new_df, k2, col_list)

def print_examples(new_df, target, shap_index, n=0):
    import numpy as np

    if n == 0:
        show_df = new_df[new_df[target]==shap_index].copy()
    else:
        show_df = new_df[new_df[target]==shap_index].sample(n=n).copy()
    show_df = np.round(show_df,2)
    return(show_df)



def plot_difference(data, compare_to,  X, included_columns, shap_values, shap_index, col_num=6, scaled=False):
    import pandas as pd
    from OrderedSet import OrderedSet
    from sklearn.preprocessing import MinMaxScaler
    
    
    scaler = MinMaxScaler() 

    new_df, k2, col_list = create_example_df(compare_to, X, included_columns, shap_index, shap_values, col_num=col_num)
    new_df['df_type']=True
    
    new_x = list(OrderedSet(X.columns.to_list())- (OrderedSet(X.columns.to_list())-OrderedSet(col_list)))    
    new_reg_df = pd.concat([data[included_columns], X[new_x]], axis=1)

    
    new_reg_df['df_type']=False

    if scaled:
        all_data = pd.concat([new_reg_df, new_df])
        scaled_values = scaler.fit_transform(all_data)
        all_data.loc[:,:] = scaled_values
        new_df = all_data[all_data['df_type']==True].copy()
        new_reg_df = all_data[all_data['df_type']==False].copy()
        new_reg_df.drop(['df_type'], axis=1, inplace=True)
        new_df.drop(['df_type'], axis=1, inplace=True)
        
    else:
        if type(included_columns) == list:
            col_list.extend(included_columns)
        else:
            col_list.append(included_columns)
    bar1 = pd.DataFrame([new_reg_df[col_list].describe().iloc[1, 0:]])
    bar1.rename(index={'mean':'Regural mean'},inplace=True)
    bar2 = pd.DataFrame([new_df[col_list].describe().iloc[1, 0:]])
    bar2.rename(index={'mean':'Selected mean'},inplace=True)
    stats_data = pd.concat([bar1, bar2])

    stats_data.plot(kind='bar', figsize=(15, 10))
    return(stats_data, k2)