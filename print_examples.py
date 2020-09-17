def create_example_df(compare_to, X, included_columns, shap_values, col_num=5):
    from OrderedSet import OrderedSet
    import numpy as np
    import pandas as pd
    
    feature_list = X.columns
    
    if len(compare_to) == 1:
        idx = compare_to.index.item()
        shap_v = pd.DataFrame(shap_values.values[idx]).T
        shap_v.columns = feature_list
    
        shap_v=shap_v.T
        shap_abs = np.abs(shap_v)
        shap_v = shap_v.reset_index()
        shap_v.columns = ['Variable','SHAP']
    
        k=pd.DataFrame(shap_abs).reset_index()
        k.columns = ['Variable','SHAP_abs']
        k = k.merge(shap_v,left_on = 'Variable',right_on='Variable',how='inner')
    else:
        shap_v = pd.DataFrame(shap_values.values)
        shap_v.columns = feature_list
    
        shap_abs = np.abs(shap_v).describe().iloc[1, 0:]
        shap_true = shap_v.describe().iloc[1, 0:]
        k= pd.concat([shap_abs, shap_true], axis=1)
        k= k.reset_index()
        k.columns = ['Variable', 'SHAP_abs','SHAP']
        
    k2=k.sort_values(by='SHAP_abs', ascending = False)
    k2.loc[:,'Sign'] = np.where(k2['SHAP']>0,'red','blue')
    k2.drop(['SHAP'], axis=1, inplace=True)
    col_list=k2['Variable'].head(col_num).to_list()
    new_x = list(OrderedSet(X.columns.to_list())- (OrderedSet(X.columns.to_list())-OrderedSet(col_list)))
    new_x = list(OrderedSet(new_x)-OrderedSet(included_columns))
    
    X = X.iloc[list(compare_to.index.values.tolist())]
    new_df=pd.concat([compare_to[included_columns],X[new_x]], axis=1)
    return(new_df, k2, col_list)


def find_most_different(data, compare_to, included_columns, row_type='std'):

    import pandas as pd
    
    inc_1 = pd.DataFrame([compare_to[included_columns].describe().iloc[1, 0:]])
    inc_2 = pd.DataFrame([data[included_columns].describe().iloc[1, 0:]])
    incl_data = pd.concat([inc_1, inc_2])
    incl_data = pd.DataFrame([incl_data.describe().loc[row_type, :]]).T.sort_values(row_type,ascending=False).copy()
    incl_data.reset_index(inplace=True)

    return(incl_data.iloc[0,0])


def plot_difference(data, compare_to,  X, included_columns, shap_values,  col_num=6, scaled=False):
    import pandas as pd
    from OrderedSet import OrderedSet
    from sklearn.preprocessing import MinMaxScaler
    
    
    scaler = MinMaxScaler() 
    new_df=pd.DataFrame()
    new_reg_df=pd.DataFrame()
    
    if type(included_columns) != list:
        included_columns = [included_columns]
    included_columns = list(OrderedSet(included_columns)- (OrderedSet(included_columns)-OrderedSet(included_columns)))

    new_df, k2, col_list = create_example_df(compare_to, X, included_columns, shap_values, col_num=col_num)
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

def create_party_results(target_col_start, val, data, compare_value):

    target = target_col_start + str(val)
    aanet = 'Äänet yhteensä lkm ' + str(val)

    compared_value = compare_value * (data[aanet].sum()/data['Äänet yhteensä lkm Äänet'].sum())
    compare_to = data[(data[target]) > compared_value].copy()
    return(compare_to, target, aanet)
    
    
def create_compare(target_col_start, val, data):

    target = target_col_start + str(val)

    compare_to = data[(data[target]) == 1].copy()
    return(compare_to, target)





def show_all_results(compare_to, data, X, y, model, vaalidata, shap_values, target, columns, all_included_columns, show_cols, scaled=True, included_columns=[], samples=5):

    import shap    
    from create_new_values import create_new_values
    from create_share_of_values import create_share_of_values
    
    compare_to = create_share_of_values(compare_to)
    compare_to = create_new_values(compare_to, vaalidata)
    
    comp_col = 'Miehet, 2018 (HE) osuudesta asukkaat'
    comp = X[comp_col]>X[comp_col].median()
    


    shap.plots.bar(shap_values, max_display=columns)
    shap.plots.beeswarm(shap_values, max_display=columns)
    shap.plots.bar(shap_values.cohorts(2).mean(0))
    clustering = shap.utils.hclust(X, y)
    shap.plots.bar(shap_values, clustering=clustering, max_display=columns, cluster_threshold=0.6)
    shap.group_difference_plot(shap_values.values, comp, feature_names=X.columns, max_display=columns)
    
    explainer =  shap.TreeExplainer(model)
    expected_value = explainer.expected_value[0]
    shap_interaction_values = explainer.shap_interaction_values(X)

    shap.decision_plot(expected_value, shap_interaction_values, X, 
                   feature_order='hclust', feature_display_range=range(12, -1, -1), ignore_warnings=True)
    
    shap.plots.heatmap(shap_values, instance_order=shap_values.sum(1), max_display=columns)
    
    
    inds = shap.utils.potential_interactions(shap_values[:, shap_values.abs.mean(0).argsort[-1]], shap_values)

    # make plots colored by each of the top three possible interacting features
    for i in range(3):
        shap.plots.scatter(shap_values[:, shap_values.abs.mean(0).argsort[-1]], color=shap_values[:,inds[i]])
    stats_data, k = plot_difference(data, compare_to, X, included_columns, shap_values, col_num=columns, scaled=scaled)
    colorlist = k['Sign']
    k.sort_values(by='SHAP_abs',ascending = True, inplace=True)
    ax = k.tail(columns).plot.barh(x='Variable',y='SHAP_abs',color = colorlist, figsize=(6,8),legend=False, fontsize=20)
    ax.set_xlabel("SHAP Value (Punainen = Korostaa)")
    stats_data_party, k = plot_difference(data, compare_to, X, all_included_columns, shap_values, col_num=0, scaled=False)
    new = show_cols.copy()
    new.append(target)
    new_df, k2, col_list = create_example_df(compare_to, X, new, shap_values, col_num=columns)
    

    if len(new_df) < samples:
        display(new_df)
    else:
        display(new_df.sample(samples))
    return(stats_data, k, col_list)

def show_one_results(data, X, y, model, shap_values, included, pnro, columns):
    
    import shap

    shap_val = []
    shap_bas = []
    shap_clu = {}
    
    for i in included:
        shap_clu[i]=shap.utils.hclust(X, y[i])
        shap_val.append(shap_values[i].values)
        shap_bas.append(shap_values[i].base_values[0])
    shap.multioutput_decision_plot(shap_bas,shap_val, row_index=data[data['Postinumero']==pnro].index.to_list()[0], feature_names=list(X.columns), legend_labels=included, ignore_warnings=True)

    for i in included:
        print(i)
        pnro_shap = shap_values[i][data[data['Postinumero']==pnro].index.to_list()[0]]
        shap.plots.bar(pnro_shap, clustering=shap_clu[i], max_display=columns, cluster_threshold=0.6)
        shap.plots.waterfall(pnro_shap)
        explainer = shap.TreeExplainer(model[i])
        expected_value = explainer.expected_value
        shap.decision_plot(expected_value, pnro_shap.values, X.iloc[data[data['Postinumero']==pnro].index.to_list()[0]],feature_order='hclust')

