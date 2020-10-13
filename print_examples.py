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

def cluster_dedndogram(X):

    import scipy as sp
    import matplotlib.pyplot as plt

    D = sp.spatial.distance.pdist(X.fillna(X.mean()).T, metric="correlation")
    cluster_matrix = sp.cluster.hierarchy.complete(D)
    plt.figure(figsize=(15, 6))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    sp.cluster.hierarchy.dendrogram(
        cluster_matrix,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=10.,  # font size for the x axis labels
        labels=X.columns
    )
    plt.show()


def create_party_results(target_col_start, val, data, vaalidata, compare_value):

    from create_share_of_values import create_share_of_values
    from create_new_values import create_new_values

    target = target_col_start + str(val)
    aanet = 'Äänet yhteensä lkm ' + str(val)

    compared_value = compare_value * (data[aanet].sum()/data['Äänet yhteensä lkm Äänet'].sum())
    compare_to = data[(data[target]) > compared_value].copy()
        
    compare_to = create_share_of_values(compare_to)
    compare_to = create_new_values(compare_to, vaalidata)
    return(compare_to, target)
    
    
def create_compare(target_col_start, val, data, vaalidata):
    
    from create_share_of_values import create_share_of_values
    from create_new_values import create_new_values

    target = target_col_start + str(val)

    compare_to = data[(data[target]) == 1].copy()
    compare_to = create_share_of_values(compare_to)
    compare_to = create_new_values(compare_to, vaalidata)
    
    return(compare_to, target)


def compare_scatter(selected_cols, included_col_start, X, col1, col2, shap_data, ylim_min=-0.05, ylim_max=0.05):
    import matplotlib.pyplot as plt
    import shap
    from create_target_columns import create_target_columns

    columns_to_print = create_target_columns(selected_cols, included_col_start)
    
    for t in columns_to_print:

        shap.plots.scatter(shap_data[t]['shap_values'][:,col1], color=shap_data[t]['shap_values'][:,col2],  show=False)
        plt.ylim([ylim_min, ylim_max]) 
        plt.title(t)
    plt.show()


# we can use shap.approximate_interactions to guess which features may interact 
def print_scatter(shap_values, t, order = 0, rng =  5, low = 0, high = 100):

    
    import matplotlib.pyplot as plt
    import numpy as np
    import shap
    

    top_inds = np.argsort(-np.sum(np.abs(shap_values.values), 0))
    
    
    
    
    interaction  = np.where(top_inds==order)[0].item()
    
    inds=shap.utils.potential_interactions(shap_values[:, interaction], shap_values)

    feature = shap_values[:,interaction]
    
    # make plots colored by each of the top three possible interacting features
    for i in range(rng):
        shap.plots.scatter(feature, color=shap_values[:,inds[i]], ymin=feature.percentile(low), ymax=feature.percentile(high), xmin=feature.percentile(low), xmax=feature.percentile(high), show=False)
        plt.title(t)
        # plt.savefig("my_dependence_plot.pdf") # we can save a PDF of the figure if we want
        plt.show()

def show_all_results(compare_to, data, X, y, shap_data, target, columns, all_included_columns, show_cols, comp_col, scaled=True, included_columns=[], samples=5):
    
    import shap
    import matplotlib.pyplot as plt

    shap_values = shap_data['shap_values']
    expected_value = shap_data['expected_value']
    shap_interaction_values = shap_data['shap_interaction_values']
    shap_values_Partition = shap_data['shap_values_Partition']
    shap_values_Permutation = shap_data['shap_values_Permutation']
    clustering = shap_data['clustering']
        
    comp = X[comp_col]>X[comp_col].median()
    
    shap.plots.bar(shap_values, max_display=columns, show=False)
    plt.title(target)
    plt.show()
    shap.plots.bar(shap_values_Partition, max_display=columns, show=False)
    plt.title(target)
    plt.show()
    shap.plots.bar(shap_values_Permutation, max_display=columns, show=False)
    plt.title(target)
    plt.show()
    shap.plots.beeswarm(shap_values, max_display=columns, show=False)
    plt.title(target)
    plt.show()
    shap.plots.bar(shap_values.cohorts(2).mean(0), show=False)
    plt.title(target)
    plt.show()

    shap.plots.bar(shap_values, clustering=clustering, max_display=columns, clustering_cutoff=0.6, show=False)
    plt.title(target)
    plt.show()
    shap.group_difference_plot(shap_values_Permutation.values, comp, feature_names=X.columns, max_display=columns, show=False)
    plt.title(target + "\n verrattuna " + comp_col)
    plt.show()
    shap.decision_plot(expected_value,shap_values.values, X, feature_order='hclust', feature_display_range=range(columns, -1, -1), ignore_warnings=True, show=False)
    plt.title(target)
    plt.show()
    
    shap.plots.heatmap(shap_values_Permutation, instance_order=shap_values_Permutation.sum(1), max_display=columns, show=False)
    plt.title(target)
    plt.show()
    
    
    for order in range(3):
        print_scatter(shap_values_Permutation, target, order = order, rng =  3, low = 1, high = 99)  

        
    stats_data, k = plot_difference(data, compare_to, X, included_columns, shap_values_Permutation, col_num=columns, scaled=scaled)
    colorlist = k['Sign']
    k.sort_values(by='SHAP_abs',ascending = True, inplace=True)
    k.tail(columns).plot.barh(x='Variable',y='SHAP_abs',color = colorlist, figsize=(6,8),legend=False, fontsize=14)
    plt.show()
    stats_data_party, k = plot_difference(data, compare_to, X, all_included_columns, shap_values, col_num=0, scaled=False)
    new = show_cols.copy()
    new.append(target)
    new_df, k2, col_list = create_example_df(compare_to, X, new, shap_values, col_num=columns)
    

    if len(new_df) < samples:
        display(new_df)
    else:
        display(new_df.sample(samples))
    return(stats_data, k, col_list)

def show_one_results(data, X, y, model, shap_data, target, key, key_value, columns):
    
    import shap
    import matplotlib.pyplot as plt

    shap_val = []
    shap_bas = []
    shap_clu = {}
    
    
    for i in target:
        shap_val.append(shap_data[i]['shap_values_Permutation'].values)
        shap_bas.append(shap_data[i]['shap_values_Permutation'].base_values[0])
        shap_clu[i] = shap_data[i]['clustering']
        
        
        
    shap.multioutput_decision_plot(shap_bas,shap_val, row_index=data[data[key]==key_value].index.to_list()[0], feature_names=list(X.columns), legend_labels=target, ignore_warnings=True, show=False)
    plt.title(key_value)
    plt.show()

    for i in target:
        key_shap = shap_data[i]['shap_values_Permutation'][data[data[key]==key_value].index.to_list()[0]]
        shap.plots.bar(key_shap, clustering=shap_clu[i], max_display=columns, clustering_cutoff=0.6, show=False)
        plt.title(i + " " + key_value)
        plt.show()
    
        shap.plots.waterfall(key_shap, show=False)
        plt.title(i + " " + key_value)
        plt.show()