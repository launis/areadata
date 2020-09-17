def develop_target_category(data, target_col):
    import pandas as pd

    from pandas.api.types import is_numeric_dtype
    
    
    if is_numeric_dtype(data[target_col]):
        data.loc[:,target_col]=data[target_col].astype('category')
        data_targets=pd.concat([data[target_col],pd.get_dummies(data[target_col], prefix='Category__' + target_col,dummy_na=False)],axis=1).drop(target_col,axis=1).copy()
        data = pd.concat([data, data_targets],axis=1).copy()
        data.loc[:,target_col]=data[target_col].astype('int')
    else:
        data_targets=pd.concat([data[target_col],pd.get_dummies(data[target_col], prefix='Category__' + target_col,dummy_na=False)],axis=1).drop(target_col,axis=1).copy()
        data = pd.concat([data, data_targets],axis=1).copy()

    list_of_targets = sorted(list(data[target_col].unique()))
    target_col_start = data_targets.columns[0].rsplit('_', 1)[0] + '_'

    
    return(data, list_of_targets, target_col_start)