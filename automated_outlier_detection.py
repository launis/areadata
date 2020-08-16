def automated_outlier_detection(X, X_scale, data, scaled, n_clusters, outlier_fraction):
    """
    

    Parameters
    ----------
    X : dataframe.
    X_scale : Tscaled dataframe
    data : all data
    n_clusters : cluster amount
    outlier_fraction : share of outliers 

    Returns
    -------
    X : dataframe.
    X_scale : Tscaled dataframe
    data : all data

    https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.knn

    """
    
   
    from pyod.models.knn import KNN


 
    knn_outlier = KNN(n_neighbors=n_clusters, contamination=outlier_fraction)
    if scaled:
        knn_outlier.fit(X_scale)
    else:
        knn_outlier.fit(X)
    # get the prediction labels and outlier scores of the training data

    data['outlier']=knn_outlier.labels_  # pred labels (0: inliers, 1: outliers)
    data['outlier_score']=knn_outlier.decision_scores_ # raw outlier scores
    
    #remove outliers from data
    outliers = data[data['outlier']==1].copy()
    data = data[data['outlier']==0].copy()
    X = X.loc[data.index]
    X_scale= X_scale.loc[data.index]
    return(X, X_scale, data, outliers)