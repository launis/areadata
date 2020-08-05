def create_dbscan_clusters(X, numeric_features, categorical_features, data, eps, min_samples, silhouette_print=0, scaled=False):
    
    import numpy as np
    import pandas as pd
    from sklearn.cluster import DBSCAN
    import geopandas as gp

    from scale_data import scale_data
    
    data = data.replace([np.inf, -np.inf], np.nan)
    data.dropna(inplace=True)
    col_selected =  numeric_features + categorical_features
    X_scale, column_list = scale_data(data, pd.DataFrame(), numeric_features, categorical_features)
    X = pd.concat([data[numeric_features], X_scale[list(set(column_list) - set(col_selected))]], axis = 1)

    if scaled:
        X=X_scale
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    # Number of clusters in labels, ignoring noise if present.
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    data['cluster'] = labels
    data = gp.GeoDataFrame(data, geometry='geometry')
    #sscore = metrics.silhouette_score(X, labels, metric='sqeuclidean')
    #mscore = metrics.calinski_harabasz_score(X, labels)
    #if sscore >= silhouette_print:
    #    print('EPS: %0.2f' % eps, 'Min samples: %d' % min_samples, ' Number of clusters: %d' % n_clusters, ' Number of noise clusters: %d' % n_noise, 'Silhouette Coefficient: %0.3f' % sscore, 'Calinski Harabaz Index: %d' % mscore )
    print('EPS: %0.2f' % eps, 'Min samples: %d' % min_samples, ' Number of clusters: %d' % n_clusters, ' Number of noise clusters: %d' % n_noise)
    return(db, data)