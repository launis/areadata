def create_target_columns(list_col_ends, target_col_start):
    
    target = []
    for t in list_col_ends:
        target.append(target_col_start+" " +t)

    return(target)