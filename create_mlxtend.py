def create_mlxtend(clusterer, X, y, forward=True, floating=True , cv=10):
    

    """
    The motivation behind feature selection algorithms is to
    automatically select a subset of features that is most relevant to the problem.
    
    see http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/
    
    args:
        X, dataframe 
        RMR_type='MIQ'

    Returns:
        selected_cols:
        ordered list of selected columns
    """
    
    from mlxtend.feature_selection import SequentialFeatureSelector as SFS
    from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
    
    import matplotlib.pyplot as plt
    import pandas as pd

    sfs1 = SFS(clusterer, 
           k_features=len(X.columns), 
           forward=forward, 
           floating=floating, 
           verbose=1,
           cv=cv,
           n_jobs=-1,
           scoring='accuracy')

    sfs1 = sfs1.fit(X, y, custom_feature_names=X.columns)
    sfs1_df = pd.DataFrame.from_dict(sfs1.get_metric_dict()).T

    features_max = sfs1_df[sfs1_df['avg_score']==sfs1_df['avg_score'].max()]['feature_names'].values[0]
    result = []
    for x in features_max:
        result.append(x)

    plot_sfs(sfs1.get_metric_dict(), kind='std_err')

    plt.title('Sequential Forward Selection (w. StdErr)')
    plt.grid()
    plt.show()
    return(sfs1_df, result)