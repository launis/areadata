def select_columns(selected, numeric_features, categorical_features, RMR_type='MIQ', n_clusters=6, cols=20):
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


    X_col, X_scale, data = prepare_cluster_data(selected, numeric_features, categorical_features)
    kmeans, data = create_kmeans_clusters(data, X_col, n_clusters, silhouette_print=0)
    X_col.insert(0, 'cluster', data['cluster'])
    selected_cols=pymrmr.mRMR(X_col, RMR_type, cols)
    X=X_col[selected_cols]
    X_scale=X_scale[selected_cols]

    return(X, X_scale, data)