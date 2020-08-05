def display_parallel_coordinates_centroids(kmeans, num_clusters=6, labels=None):
    
    """
    Display a parallel coordinates plot for the centroids in kmeans
    args:
        kmeans : kmeans cluster algorythm
        n_clusters: amount of clusters
        labels: columns


    """

    

    import matplotlib.pyplot as plt
    from pandas.plotting import parallel_coordinates
    import seaborn as sns
    
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