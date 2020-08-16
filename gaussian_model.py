def create_gaussian_model(data, X, model):

    from sklearn import metrics
    import geopandas as gp
    
    labels = model.predict(X)
    data['cluster'] = labels
    sscore = metrics.silhouette_score(X, labels, metric='sqeuclidean')
    mscore = metrics.calinski_harabasz_score(X, labels)
    print("Silhouette Coefficient: %0.3f" % sscore, 'Calinski Harabaz Index: %d' % mscore)
    data = gp.GeoDataFrame(data, geometry='geometry')
    
    return(data)




def create_and_draw_best_gaussian_mix(train, test, numeric_features=[], categorical_features=[], scaled=True, covariance_type = 'full'):

           
    """
    Create and draw gaussian mix
    both bic &aic

    args:
        bic
        aic
  

    Returns:
    """
    from sklearn.mixture import GaussianMixture
    import matplotlib.pyplot as plt
    from prepare_and_scale_data import prepare_and_scale_data


    bic_list = []
    aic_list = []
    lowest_bic = 9999999
    lowest_aic = 9999999
    ranges = range(1,40)

    
    data, train_scaled, train_non_scaled, test_scaled, test_non_scaled = prepare_and_scale_data(train, test, numeric_features, categorical_features)
    if scaled:
        X = train_scaled
        test = test_scaled
    else:
        X = X_train
        test = test_non_scaled
    
    

    for i in ranges:
        gmm = GaussianMixture(n_components=i, covariance_type=covariance_type).fit(X)
        # BIC
        bic = gmm.bic(X)
        bic_list.append(bic)
        if bic_list[-1] < lowest_bic:
            lowest_bic = bic_list[-1]
            best_gmm_bic = gmm

        # AIC
        aic = gmm.aic(X)
        aic_list.append(aic)

        if aic_list[-1] < lowest_aic:
            lowest_aic = aic_list[-1]
            best_gmm_aic = gmm
                
    plt.figure(figsize=(15, 8))
    plt.plot(ranges, bic_list, label='BIC');
    plt.plot(ranges, aic_list, label='AIC');
    plt.legend(loc='best')

    return(data, X, test, best_gmm_bic, best_gmm_aic)