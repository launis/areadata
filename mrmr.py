def mrmr(X, y, RMR_type='MIQ'):
    

    """
    The Minimum Redundancy Maximum Relevance feature selection 
    aims for the selection of features showing low correlations 
    among the features (Minimum Redundancy) but still having
    a high correlation to the classification variable (Maximum Relevance).
    
    see https://pypi.org/project/pymrmr/
    
    args:
        X, dataframe 
        RMR_type='MIQ'

    Returns:
        selected_cols:
        ordered list of selected columns
    """

    import pymrmr
    
    selected_cols=[]
    col_sum = len(X.columns)
    X.insert(0, 'cluster', y)
    selected_cols=pymrmr.mRMR(X, RMR_type, col_sum)

    return(selected_cols)
