def scale_data(train, test=[], numeric_features=[],  categorical_features=[]):
    
    """Scales separately both train and test dataframes
    

        train:  first dataframe
        test: second dataframe, if empty, only first one will be used
        columns_to_encode, columns needing encoding 
        columns_to_scale, scaling needed
    
    Returns:
         Scaled test and train dataframes (only first one is needed to be returned)
         Column lists as encoding might have created new columns
    """


    import pandas as pd
    from OrderedSet import OrderedSet

    def scale(df, numeric_features, categorical_features):
    
        from sklearn.preprocessing import StandardScaler

        scaler=StandardScaler()

        #scale and encode dataframe columns inplace
        column_list_encode = []
        new_df = pd.DataFrame()
        df_scale = pd.DataFrame()
        df_encode  = pd.DataFrame()
        df_col   = pd.DataFrame()

        if categorical_features != []:
            df_encode=pd.DataFrame()
            for col in categorical_features:
                df.loc[:,col]=df[col].astype('category')
                df_col= pd.concat([df[col],pd.get_dummies(df[col], prefix='Category__' + col,dummy_na=False)],axis=1).drop(col,axis=1).copy()
                df_encode = pd.concat([df_encode, df_col],axis=1).copy() 
            column_list_encode=df_encode.columns[df_encode.columns.str.startswith("Category__")].tolist()
        if numeric_features != []:
            #note, we must store the original index 
            df_scale=pd.DataFrame(scaler.fit_transform(df[numeric_features]), columns=numeric_features, index=df.index).copy()

        if (categorical_features != []) & (numeric_features != []):
            new_df=pd.concat([df_scale,df_encode],axis=1).copy()

        elif categorical_features != []:
            new_df=df_encode.copy()

        else:
            new_df=df_scale.copy()

        column_list = numeric_features + column_list_encode

        return(new_df, column_list)

    train_scaled = pd.DataFrame()
    test_scaled = pd.DataFrame()
    
    train_scaled, column_list_train = scale(train, numeric_features, categorical_features)
    if not test.empty:
        test_scaled, column_list_test = scale(test, numeric_features, categorical_features)

        #The creation of dummy values can create different set of columns between train/test
        #therefore we need to take only those columns that are available on both
        column_list_diff_train_test = list(OrderedSet(column_list_train) - OrderedSet(column_list_test))
        column_list_diff_test_train = list(OrderedSet(column_list_test) - OrderedSet(column_list_train))
        column_list = list(OrderedSet(column_list_train) - OrderedSet(column_list_diff_train_test) - OrderedSet(column_list_diff_test_train))
        return(train_scaled, test_scaled, column_list)
    else:
        column_list = column_list_train
        return(train_scaled, column_list)
        
