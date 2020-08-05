def display_factorial_planes(clusterer, data, X, n_components, axis_ranks, labels=None, alpha=1):
    '''Display a scatter plot on a factorial plane, one for each factorial plane'''

    from sklearn.decomposition import PCA
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np 

    # Create a PCA model to reduce our data to 2 dimensions for visualisation
    pca = PCA(n_components=n_components)
    pca.fit(X)
    # Transfor the scaled data to the new PCA space
    X_reduced = pca.transform(X)
    illustrative_var=data['cluster']

    # Convert to a data frame
    X_reduceddf = pd.DataFrame(X_reduced, index=data['Postinumero'])
    X_reduceddf['cluster'] = data['cluster']
    centres_reduced = pca.transform(clusterer.cluster_centers_)

    # For each factorial plane
    for d1,d2 in axis_ranks:
        if d2 < n_components:
 
            # Initialise the matplotlib figure      
            plt.figure(figsize=(7,6))
        
            # Display the points
            if illustrative_var is None:
                plt.scatter( X_reduced[:, d1],  X_reduced[:, d2], alpha=alpha)
            else:
                illustrative_var = np.array(illustrative_var)
                for value in np.unique(illustrative_var):
                    selected_data = np.where(illustrative_var == value)
                    plt.scatter(X_reduced[selected_data, d1], X_reduced[selected_data, d2], alpha=alpha, label=value)
                plt.legend()

            # Display the labels on the points
            if labels is not None:
                for i,(x,y) in enumerate( X_reduced[:,[d1,d2]]):
                    plt.text(x, y, labels[i],
                              fontsize='10', ha='center',va='center') 
                
            # Define the limits of the chart
            boundary = np.max(np.abs( X_reduced[:, [d1,d2]])) * 1.1
            plt.xlim([-boundary,boundary])
            plt.ylim([-boundary,boundary])
        
            # Display grid lines
            plt.plot([-100, 100], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-100, 100], color='grey', ls='--')

            # Label the axes, with the percentage of variance explained
            plt.xlabel('PC{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('PC{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Projection of points (on PC{} and PC{})".format(d1+1, d2+1))
            plt.scatter(centres_reduced[:, 0], centres_reduced[:, 1], marker='x', s=300, linewidths=5,c='r', zorder=10)
            plt.show()
