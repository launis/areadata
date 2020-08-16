def pfa_fit(X, n_features, n_components):
    """
    Principal feature analysis exploits the structure of the principal components of a set of
    features to choose the principal features
    args:
        X: scaled dataframe
        n_features: demanded set of features
    returns:
        list of selected features
    """
    
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans
    from collections import defaultdict
    from sklearn.metrics.pairwise import euclidean_distances

    X_val = X.values
    pca = PCA(n_components=n_components).fit(X_val)
    pcs = pca.components_.T

    kmeans = KMeans(n_clusters=n_features).fit(pcs)
        
    clusters = kmeans.predict(pcs)
    cluster_centers = kmeans.cluster_centers_

    dists = defaultdict(list)
    for i, c in enumerate(clusters):
        dist = euclidean_distances([pcs[i, :]], [cluster_centers[c, :]])[0][0]
        dists[c].append((i, dist))
        
    indices = [sorted(f, key=lambda x: x[1])[0][0] for f in dists.values()]
    return(X.columns[indices])

