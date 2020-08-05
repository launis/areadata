def display_scree_plot(X_scale, num_components = 10):
 
    """
    Display a scree plot for the pca
    args:
        X_scale, : scaled dataframe
        num_components: amount of max components

    """

    

    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.decomposition import PCA
    from display_scree_plot import display_scree_plot

    # Create the PCA model
    pca = PCA(n_components=num_components)

    # Fit the model with the standardised data
    pca.fit(X_scale)
    
    scree = pca.explained_variance_ratio_*100
    plt.bar(np.arange(len(scree))+1, scree)
    plt.plot(np.arange(len(scree))+1, scree.cumsum(),c="red",marker='o')
    plt.xlabel("Number of principal components")
    plt.ylabel("Percentage explained variance")
    plt.title("Scree plot")
    plt.show(block=False)