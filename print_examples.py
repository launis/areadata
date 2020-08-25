def create_example_df(data, X, included_columns, shap_index, shap_values, col_num=5):
    from OrderedSet import OrderedSet
    import numpy as np
    import pandas as pd

    if type(included_columns) != list:
        included_columns = [included_columns]
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
    new_x = list(OrderedSet(new_x)-OrderedSet(included_columns))
    
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

def find_most_different(data, compare_to, included_columns, row_type='std'):

    import pandas as pd
    
    inc_1 = pd.DataFrame([compare_to[included_columns].describe().iloc[1, 0:]])
    inc_2 = pd.DataFrame([data[included_columns].describe().iloc[1, 0:]])
    incl_data = pd.concat([inc_1, inc_2])
    incl_data = pd.DataFrame([incl_data.describe().loc[row_type, :]]).T.sort_values(row_type,ascending=False).copy()
    incl_data.reset_index(inplace=True)

    return(incl_data.iloc[0,0])

def show_real_share(compare_to, sum_columns, share, total, list_of_members):
    import pandas as pd
    aanet = pd.DataFrame(columns=[share])
    j=0
    compare_to_party = pd.DataFrame(compare_to[sum_columns].sum())
    for i in sum_columns:

        aanet.loc[list_of_members[j]] = pd.Series({share : compare_to[i].sum()/compare_to[total].sum()})
        j= j+1
    aanet.plot(kind='bar', figsize=(15, 10))
    return (aanet)

def plot_difference(data, compare_to,  X, included_columns, shap_values, shap_index, col_num=6, scaled=False):
    import pandas as pd
    from OrderedSet import OrderedSet
    from sklearn.preprocessing import MinMaxScaler
    
    
    scaler = MinMaxScaler() 
    new_df=pd.DataFrame()
    new_reg_df=pd.DataFrame()
    
    if type(included_columns) != list:
        included_columns = [included_columns]
    included_columns = list(OrderedSet(included_columns)- (OrderedSet(included_columns)-OrderedSet(included_columns)))

    new_df, k2, col_list = create_example_df(compare_to, X, included_columns, shap_index, shap_values, col_num=col_num)
    new_df['df_type']=True
    
    new_x = list(OrderedSet(X.columns.to_list())- (OrderedSet(X.columns.to_list())-OrderedSet(col_list)))
    new_x = list(OrderedSet(col_list)-OrderedSet(included_columns))
    new_reg_df = pd.concat([data[included_columns], X[new_x]], axis=1)
    new_reg_df['df_type']=False

    col_list = list(OrderedSet(col_list)-OrderedSet(included_columns))
    col_list.extend(included_columns)

    if scaled:
        all_data = pd.concat([new_reg_df, new_df])
        scaled_values = scaler.fit_transform(all_data)
        all_data.loc[:,:] = scaled_values
        new_df = all_data[all_data['df_type']==True].copy()
        new_reg_df = all_data[all_data['df_type']==False].copy()

    new_reg_df.drop(['df_type'], axis=1, inplace=True)
    new_df.drop(['df_type'], axis=1, inplace=True)
    bar1 = pd.DataFrame([new_reg_df[col_list].describe().iloc[1, 0:]])
    bar1.rename(index={'mean':'Regural mean'},inplace=True)
    if len(new_df) == 1: #only one column, describe acts differently
        bar2 = new_df[col_list]
    else:
        bar2 = pd.DataFrame([new_df[col_list].describe().iloc[1, 0:]])
        bar2.rename(index={'mean':'Selected mean'},inplace=True)
    
    stats_data = pd.concat([bar1, bar2])

    stats_data.plot(kind='bar', figsize=(15, 10))
    return(stats_data, k2)