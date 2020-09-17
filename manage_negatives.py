def manage_negatives(stat, col_list):
    """
    negatives to scaled positives

    args:
        stat : postocode level values
  

    Returns:
         stat
    """

    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()   
    
    
    share_word = " nollatta"

    
    for col in col_list:
        target_col = col + share_word
        stat[target_col] = scaler.fit_transform(stat[[col]])
    return(stat)