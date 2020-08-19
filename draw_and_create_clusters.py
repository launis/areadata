def draw_puolue_varit(data, Y, ax):
    """
    Set color of different parties in Finland
    to the plot

    args:
        X: data
  

    Returns:
        ax         
    """

    from matplotlib.ticker import NullFormatter

    blue = data['Suurin_puolue'] == 'KOK'
    green = data['Suurin_puolue'] == 'VIHR'
    pink = data['Suurin_puolue'] == 'SDP'
    yellow = data['Suurin_puolue'] == 'RKP'
    darkgreen = data['Suurin_puolue'] == 'KESK'
    gold = data['Suurin_puolue'] == 'PS'
    red = data['Suurin_puolue'] == 'VAS'
    deepskyblue = data['Suurin_puolue'] == 'KD'

    
    ax.scatter(Y[blue, 0], Y[blue, 1], c="blue")
    ax.scatter(Y[green, 0], Y[green, 1], c="green")
    ax.scatter(Y[pink, 0], Y[pink, 1], c="deeppink")
    ax.scatter(Y[darkgreen, 0], Y[darkgreen, 1], c="darkgreen")
    ax.scatter(Y[gold, 0], Y[gold, 1], c="gold")
    ax.scatter(Y[red, 0], Y[red, 1], c="red")
    ax.scatter(Y[yellow, 0], Y[yellow, 1], c="yellow")
    ax.scatter(Y[deepskyblue, 0], Y[deepskyblue, 1], c="deepskyblue")
    
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.axis('tight')
    return(ax)


def draw_pca(X, data, n_components = 2, compare=True):
    
    """
    Create and draw PCA

    args:
        X: data
  

    Returns:
        PCA_components: Principal components dataframe
         
    """
    
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA

    (fig, subplots) = plt.subplots(1, 1, figsize=(15, 8))

    pca = PCA(n_components=n_components, svd_solver = 'full')
    y = pca.fit_transform(X)

    ax = subplots
    ax.set_title('PCA')
    if compare:
        draw_puolue_varit(data, y, ax)
    plt.show()

def drawTSNE(X, data, n_components = 2, compare=True):
    """
    Create and draw TSNE

    args:
        X: data
        compare,if 1 use colors from parties via 
        draw_puolue_varit function
  

    Returns:         
    """

    from sklearn import manifold
    from time import time
    import matplotlib.pyplot as plt

    (fig, subplots) = plt.subplots(1, 4, figsize=(15, 8))
    perplexities = [30, 50, 70, 100]

    for i, perplexity in enumerate(perplexities):
        ax = subplots[i]

        t0 = time()
        tsne = manifold.TSNE(n_components=n_components, init='random',
                         random_state=0, perplexity=perplexity)
        Y = tsne.fit_transform(X)
        t1 = time()
        print("Perplexity=%d in %.3g sec" % (perplexity, t1 - t0))
        ax.set_title("Perplexity=%d" % perplexity)
        if compare :
            draw_puolue_varit(data, Y, ax)

    plt.show()
    
def display_circles(X_scale, n_components, axis_ranks, labels=None, label_rotation=0, lims=None):
 
    """
    Display correlation circles, one for each factorial plane"
    args:
        X_scale, : scaled dataframe
        n_components: amount of max components

    """
    import matplotlib.pyplot as plt
    import numpy as np    
    from matplotlib.collections import LineCollection
    from sklearn.decomposition import PCA

    pca = PCA(n_components=n_components)
    pca.fit(X_scale)
    pcs = pca.components_ 

    # For each factorial plane
    for d1, d2 in axis_ranks: 
        if d2 < n_components:

            # Initialise the matplotlib figure
            fig, ax = plt.subplots(figsize=(10,10))

            # Determine the limits of the chart
            if lims is not None :
                xmin, xmax, ymin, ymax = lims
            elif pcs.shape[1] < 30 :
                xmin, xmax, ymin, ymax = -1, 1, -1, 1
            else :
                xmin, xmax, ymin, ymax = min(pcs[d1,:]), max(pcs[d1,:]), min(pcs[d2,:]), max(pcs[d2,:])

            # Add arrows
            # If there are more than 30 arrows, we do not display the triangle at the end
            if pcs.shape[1] < 30 :
                plt.quiver(np.zeros(pcs.shape[1]), np.zeros(pcs.shape[1]),
                   pcs[d1,:], pcs[d2,:], 
                   angles='xy', scale_units='xy', scale=1, color="grey")
                # (see the doc : https://matplotlib.org/api/_as_gen/matplotlib.pyplot.quiver.html)
            else:
                lines = [[[0,0],[x,y]] for x,y in pcs[[d1,d2]].T]
                ax.add_collection(LineCollection(lines, axes=ax, alpha=.1, color='black'))
            
            # Display variable names
            if labels is not None:  
                for i,(x, y) in enumerate(pcs[[d1,d2]].T):
                    if x >= xmin and x <= xmax and y >= ymin and y <= ymax :
                        plt.text(x, y, labels[i], fontsize='10', ha='center', va='center', rotation=label_rotation, color="blue", alpha=0.5)
            
            # Display circle
            circle = plt.Circle((0,0), 1, facecolor='none', edgecolor='b')
            plt.gca().add_artist(circle)

            # Define the limits of the chart
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
        
            # Display grid lines
            plt.plot([-1, 1], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-1, 1], color='grey', ls='--')

            # Label the axes, with the percentage of variance explained
            plt.xlabel('PC{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('PC{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Correlation Circle (PC{} and PC{})".format(d1+1, d2+1))
            plt.show(block=False)
    return(pcs)

def display_parallel_coordinates_centroids(kmeans, labels=None):
    
    """
    Display a parallel coordinates plot for the centroids in kmeans
    args:
        kmeans : kmeans cluster algorythm
        labels: columns


    """

    import matplotlib.pyplot as plt
    from pandas.plotting import parallel_coordinates
    import seaborn as sns
    import pandas as pd
    
    centroids = pd.DataFrame(kmeans.cluster_centers_, columns=labels)
    centroids['cluster'] = centroids.index

    # Create the plot
    fig = plt.figure(figsize=(12, 5))
    title = fig.suptitle("Parallel Coordinates plot for the Centroids", fontsize=12)
    fig.subplots_adjust(top=0.9, wspace=0)

    # Draw the chart
    palette = sns.color_palette("bright", 10)
    parallel_coordinates(centroids, 'cluster', color=palette)

    # Stagger the axes
    ax=plt.gca()
    for tick in ax.xaxis.get_major_ticks()[1::2]:
        tick.set_pad(20)


    return(centroids)

def display_scree_plot(X_scale, n_components = 10):
 
    """
    Display a scree plot for the pca
    args:
        X_scale, : scaled dataframe
        num_components: amount of max components

    """

    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.decomposition import PCA

    # Create the PCA model
    pca = PCA(n_components=n_components)

    # Fit the model with the standardised data
    pca.fit(X_scale)
    
    scree = pca.explained_variance_ratio_*100
    plt.bar(np.arange(len(scree))+1, scree)
    plt.plot(np.arange(len(scree))+1, scree.cumsum(),c="red",marker='o')
    plt.xlabel("Number of principal components")
    plt.ylabel("Percentage explained variance")
    plt.title("Scree plot")
    plt.show(block=False)

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
    
def draw_silhouette_score(X, clusterer):
    """
    Create and draw silhouette_score

    args:
        X: data
        clusterer: model 
  

    Returns:         
    """
    
    from sklearn.metrics import silhouette_samples, silhouette_score

    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np


    range_n_clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    for n_clusters in range_n_clusters:
        # Create a subplot with 1 row and 2 columns
        fig, (ax1) = plt.subplots(1, 1)
        fig.set_size_inches(15, 8)

        # The silhouette coefficient can range from -1, 1 
        ax1.set_xlim([-1, 1])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        clusterer.set_params(**{'n_clusters' : n_clusters})
        cluster_labels = clusterer.fit_predict(X)
 
        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i) / n_clusters)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
 
    plt.show()
    
def draw_clusters(X, range_end):
    #3 Using the elbow method to find out the optimal number of #clusters. 
    #KMeans class from the sklearn library.
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt

    wcss=[]

    for i in range(1, range_end):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', n_init =  20, max_iter = 500)
        kmeans.fit(X)
        # inertia method returns wcss for that model
        wcss.append(kmeans.inertia_)

    #4.Plot the elbow graph
    plt.plot(range(1,range_end),wcss)
    plt.title('The Elbow Method Graph')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()
    


def create_kmeans_clusters(filename_model, path, train, test, numeric_features=[], categorical_features=[], n_clusters=6, silhouette_print=0, scaled=True):

    """
    
    Scale data, geneate categorcal columns
    and create Kmeans model
    args:
        data: dataframe
        X: scaled data
        n_clusters: targetesd amountof clusters
        silhouette_print: the min score that will be printed 
 
    Returns:
        kmeans: model
        X managed data
        X_scale scaled and managed data
        data: al data together with cluster value
    """

    import os
    import pickle
    from shapely import wkt

    
    from sklearn.cluster import KMeans
    import geopandas as gp
    from sklearn import metrics
    from prepare_and_scale_data import prepare_and_scale_data

    
    data, train_scaled, train_non_scaled, test_scaled, test_non_scaled = prepare_and_scale_data(train, test, numeric_features, categorical_features)
    if scaled:
        X = train_scaled
        test = test_scaled
    else:
        X = X_train
        test = test_non_scaled
    
    filename_model = os.path.join(path, filename_model)
    if os.access(filename_model, os.R_OK):
        print('load model')
        kmeans = pickle.load(open(filename_model, "rb"))
    else:
        print('Create model')
        kmeans = KMeans(n_clusters=n_clusters, init = 'k-means++', n_init =  20, max_iter = 500)
        pickle.dump(kmeans, open(filename_model, "wb"))

    # We are going to use the fit predict method that returns for each #observation which cluster it belongs to. The cluster to which #client belongs and it will return this cluster numbers into a #single vector that is  called y K-means
    labels = kmeans.fit_predict(X)
    data['cluster'] = labels
    sscore = metrics.silhouette_score(X, labels, metric='sqeuclidean')
    mscore = metrics.calinski_harabasz_score(X, labels)
    if sscore >= silhouette_print:
        print('Number of clusters: %d' % n_clusters, "Silhouette Coefficient: %0.3f" % sscore, 'Calinski Harabaz Index: %d' % mscore)
    

    #data['geometry'] = data['geometry'].apply(wkt.loads)
    data = gp.GeoDataFrame(data, geometry='geometry')
    return(data, X, test, kmeans)

