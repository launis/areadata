def create_dbscan_clusters(data, X, eps, min_samples, silhouette_print=0):
    
    import numpy as np
    from sklearn.cluster import DBSCAN
    import geopandas as gp
    from sklearn import metrics
    
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    # Number of clusters in labels, ignoring noise if present.
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    data['cluster'] = labels
    data = gp.GeoDataFrame(data, geometry='geometry')
    sscore = metrics.silhouette_score(X, labels, metric='sqeuclidean')
    mscore = metrics.calinski_harabasz_score(X, labels)
    if sscore >= silhouette_print:
        print('EPS: %0.2f' % eps, 'Min samples: %d' % min_samples, ' Number of clusters: %d' % n_clusters, ' Number of noise clusters: %d' % n_noise, 'Silhouette Coefficient: %0.3f' % sscore, 'Calinski Harabaz Index: %d' % mscore )
    return(db, data)