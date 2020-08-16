from sklearn.feature_selection import  mutual_info_classif

def select_columns_and_clean_data(selected,
                                  numeric_features, 
                                  categorical_features, 
                                  frac = 0.2,
                                  outlier_fraction = 0.003,
                                  kbest_score_func = mutual_info_classif,
                                  k_selected = 'all',
                                  RMR_type='MIQ', 
                                  n_clusters=6,
                                  scaled=False):
    

    """
    Scale data, geneate categorcal columns
    and create Kmeans model
    args:
        selected: selected dataframe
        numeric_features: numeric column names
        categorical_features: : catgorical data column names
        n_clusters: amount of clusters

    Returns:

        X managed data
        X_scale scaled and managed data
        data: al data together with cluster value
    """

    import pymrmr
    from draw_and_create_clusters import  prepare_cluster_data, create_kmeans_clusters 
    from create_prediction import select_kbest
    from pyod.models.knn import KNN

    selected.sample(frac=frac, replace=True)

    X, X_scale, data = prepare_cluster_data(selected, numeric_features, categorical_features)

    knn_outlier = KNN(n_neighbors=n_clusters, contamination=outlier_fraction)
    knn_outlier.fit(X)

    # get the prediction labels and outlier scores of the training data

    data['outlier']=knn_outlier.labels_  # pred labels (0: inliers, 1: outliers)
    data['outlier_score']=knn_outlier.decision_scores_ # raw outlier scores
    
    #remove outliers from data
    outliers = data[data['outlier']==1].copy()
    data = data[data['outlier']==0].copy()
    X = X.loc[data.index]
    X_scale= X_scale.loc[data.index]

    if scaled:
        kmeans, data = create_kmeans_clusters(data, X_scale, n_clusters, silhouette_print=0)
        X_mrmr=X_scale.copy()    
        features_df=select_kbest(X_scale, data['cluster'], kbest_score_func, k_selected)
    else:
        kmeans, data = create_kmeans_clusters(data, X, n_clusters, silhouette_print=0)
        X_mrmr=X.copy()
        features_df=select_kbest(X, data['cluster'], kbest_score_func, k_selected)

    X_mrmr.insert(0, 'cluster', data['cluster'])
    selected_cols=pymrmr.mRMR(X_mrmr, 'MIQ', len(X_mrmr.columns))
    selected_cols.remove('cluster') 

    return(kmeans, X, X_scale, data, selected_cols, features_df, outliers)