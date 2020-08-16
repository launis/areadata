def select_kbest(X, y, kbest_score_func, k='all'):
    from sklearn.feature_selection import SelectKBest
    import pandas as pd
    
    selector = SelectKBest(kbest_score_func, k=k)
    selector.fit(X, y)
    features_names = X.columns
    features_scores = selector.scores_
    features_selected = selector.get_support()
    
    dict = {'Column': features_names, 'Score': features_scores, 'Selected': features_selected}
    features_df = pd.DataFrame(dict)
    features_df.sort_values('Score', inplace=True, ascending=False)
    features_df.reset_index(drop=True, inplace=True)
    return(features_df)

def one_value(gridsearch_params,
              small_better,
              param_a,
              params,
              dvalue,
              metrics,
              num_boost_round,
              early_stopping_rounds,
              Skfold=True,
              verbose=False):
    
    """This searches the best hyperparameter for selected hyperparameter
    

    Args:
        gridsearch_params: hyperparameter-values to be evaluated 
        small_better:  if small value is searched = true
        param_a: name of the hyperparameter
        params: parameters dictionary
        dtrain: traindata
        metrics: the metric that defines the score
        num_boost_round: max evaluation round 
        Skfold: id used True
        verbose: how much data is showed    
    
    Returns:
        parameter dictionary

    """

    import xgboost as xgb
    
    if small_better == True:
        result_best = float(999999)
    else:
        result_best = float(-999999)
    best_params = None

    for i in gridsearch_params:
        # Update our parameters
        if verbose:
            print("xgb.cv with {}={}".format(param_a, i))
        params[param_a] = i
  
        # Run CV
        cv_results = xgb.cv(
            params,
            dvalue,
            nfold =3,
            stratified=Skfold,
            verbose_eval = 0,
            num_boost_round = num_boost_round,
            early_stopping_rounds=early_stopping_rounds)
        
        # Update best result
        result_col = "test-" + metrics + "-mean"


        if small_better == True:
            result = cv_results[result_col].min()
            boost_rounds = cv_results[result_col].argmin()
            if result < result_best:
                result_best = result
                best_params = i
        else:
            result = cv_results[result_col].max()
            boost_rounds = cv_results[result_col].argmin()
            if result > result_best:
                result_best = result
                best_params = i
        if verbose:
            print("xgb.cv {} {} for {} rounds".format(metrics, result,  boost_rounds))
        
    print("Best xgb.cv params: {} {}, {}: {}".format(param_a, best_params, metrics, result_best))
    params[param_a] = best_params
    return(params)

def two_values(gridsearch_params,
               small_better,
               param_a,
               param_b,
               params,
               dvalue,
               metrics,
               num_boost_round,
               early_stopping_rounds,
               Skfold=True,
               verbose=False):

    """This searches the best hyperparameter for the two selected hyperparameters
    

    Args:
        gridsearch_params: hyperparameter-values to be evaluated 
        small_better:  if small value is searched = true
        param_a: name of the first hyperparameter
        param_b: name of the second hyperparameter
        params: parameters dictionary
        dtrain: traindata
        metrics: the metric that defines the score
        num_boost_round: max evaluation round 
        Skfold: id used True
        verbose: how much data is showed    
    
    Returns:
        parameter dictionary

    """
    
    import xgboost as xgb
    
    if small_better == True:
        result_best = float(999999)
    else:
        result_best = float(-999999)
    best_params = None

    for i, j in gridsearch_params:
        # Update our parameters
 
        if verbose:
            print("xgb.cv with {}={}, {}={}".format(param_a, i, param_b, j))
        params[param_a] = i
        params[param_b] = j
  
        # Run CV
        cv_results = xgb.cv(
            params,
            dvalue,
            nfold =3,
            stratified=Skfold,
            verbose_eval = 0,
            num_boost_round = num_boost_round,
            early_stopping_rounds=early_stopping_rounds)
       
        # Update best result
        result_col = "test-" + metrics + "-mean"
    

        if small_better == True:
            result = cv_results[result_col].min()
            boost_rounds = cv_results[result_col].argmin()
            if result < result_best:
                result_best = result
                best_params = (i,j)
        else:
            result = cv_results[result_col].max()
            boost_rounds = cv_results[result_col].argmax()
            if result > result_best:
                result_best = result
                best_params = (i,j)
        if verbose:
            print("xgb.cv {} {} for {} rounds".format(metrics, result, boost_rounds))
        
    print("Best xgb.cv params: {} {}, {} {}, {}: {}".format(param_a, best_params[0], param_b, best_params[1], metrics, result_best))
    
    params[param_a] = best_params[0]
    params[param_b] = best_params[1]
    return(params)

def hyperparameter_grid(params,
                        dtrain,
                        metrics,
                        watchlist,
                        testing=True,
                        Skfold=False,
                        Verbose=False):
    
    """This function finds the optimum hyperparameters with a loop
    

    Args:
        params: parameter dictionary
        dtrain: data
        dtest: data
        metrics: the optimization metrics {'auc'}
        num_boost_round: the num_boost running value
        testing: sets variables lighter when true
        num_boost_round: max evaluation round 
        Skfold: id used True
        verbose: how much data is showed    
    
    Returns:
        trainde and optimized model
    """
    
    import xgboost as xgb
    
    num_boost_round = 2000
    early_stopping_rounds = 10
    
    if Verbose == False:
        verbose_eval = num_boost_round
    else:
        verbose_eval = 10
    
    model = xgb.train(
        params,
        dtrain,
        verbose_eval=verbose_eval,
        num_boost_round = num_boost_round,
        early_stopping_rounds = early_stopping_rounds,
        evals=watchlist
    )
    #for testing purposes a light set to save some time
    if testing:
        rounds=2
        print('testing')
        gridsearch_params_tree = [
            (i, j)
            for i in range(1,8)
            for j in range(1,5)
            ]
        gridsearch_params_0_1 = [i/5. for i in range(0,6)]
        gridsearch_params_0_1_deep = [i/5. for i in range(0,6)]
        gridsearch_params_gamma = [i/5. for i in range(0,26)]
        
        gridsearch_params_pair_0_1 = [
            (i0, i1)
            for i0 in gridsearch_params_0_1
            for i1 in gridsearch_params_0_1
            ]
    else: #for real
        rounds=3
        print('for real')
        gridsearch_params_tree = [
            (i, j)
            for i in range(1,20)
            for j in range(1,20)
            ]
        gridsearch_params_0_1 = [i/20. for i in range(0,21)]
        gridsearch_params_0_1_deep = [i/50. for i in range(0,51)]
        gridsearch_params_gamma = [i/50. for i in range(0,251)]
        gridsearch_params_pair_0_1 = [
            (i0, i1)
            for i0 in gridsearch_params_0_1_deep
            for i1 in gridsearch_params_0_1_deep
            ]
    
    dvalue = dtrain
    result_col = "test-" + metrics + "-mean"
    cv_results = xgb.cv(
            params,
            dvalue,
            stratified=Skfold,
            num_boost_round = num_boost_round,
            early_stopping_rounds = early_stopping_rounds,
            metrics= metrics
    )
   
    print("Start with xgb.cv params: {}: {}".format(metrics, cv_results[result_col].min()))


    #Tries to do semi-automatic genetic model for hyperparameter selection
    for round in range(rounds):
    
        #Maximum depth/height of a tree
        #Minimum sum of instance weight (hessian) needed in a child
        param_a = 'max_depth'
        param_b = 'min_child_weight'
        params=two_values(gridsearch_params_tree, True, param_a, param_b, params, dvalue, metrics, num_boost_round, early_stopping_rounds,  Skfold, Verbose)


        #Gamma finds minimum loss reduction/min_split_loss required to make a further partition 
        param_a = 'gamma'
        params=one_value(gridsearch_params_gamma, True, param_a, params, dvalue, metrics, num_boost_round, early_stopping_rounds,  Skfold, Verbose)
    

        #L1 regularization term on weights - alpha  - Lasso Regression 
        #adds “absolute value of magnitude” of coefficient as penalty term to the loss function.
        #L2 regularization term on weights - lambda  - Ridge Regression 
        #adds “squared magnitude” of coefficient as penalty term to the loss function.
        #the sample is so small, so most propably no effect
        param_a = 'lambda'
        param_b = 'alpha'
        params=two_values(gridsearch_params_pair_0_1 , True, param_a, param_b, params, dvalue, metrics, num_boost_round, early_stopping_rounds, Skfold, Verbose)


        #Subsamble denotes the fraction of observations to be randomly samples for each tree.
        #Colsample_bytree enotes the fraction of columns to be randomly samples for each tree.
        param_a = 'colsample_bytree'
        param_b = 'subsample'
        params=two_values(gridsearch_params_pair_0_1, True, param_a, param_b, params, dvalue, metrics, num_boost_round, early_stopping_rounds, Skfold, Verbose)
    
        #Same as learning_rate - this needs to be in sync with num_boost_round (alias n_tree parameter)
        param_a = 'eta'
        params=one_value(gridsearch_params_0_1_deep, True, param_a, params, dvalue, metrics, num_boost_round, early_stopping_rounds,  Skfold, Verbose)
        
        #Balance of positive and negative weights.  This is regression and binary classification only parameter.
        if params['objective'].startswith('reg'):
            param_a = 'scale_pos_weight'
            params=one_value(gridsearch_params_0_1_deep, True, param_a, params, dvalue, metrics, num_boost_round, early_stopping_rounds, Skfold, Verbose)


    print('Found hyperparameters with {} rounds '.format(round+1))
    print(params)
    print()
    
    model = xgb.train(
        params,
        dtrain,
        verbose_eval=verbose_eval,
        evals=watchlist,
        num_boost_round = num_boost_round,
        early_stopping_rounds = early_stopping_rounds,
        )   
        
    num_boost_round = model.best_iteration + 1

    best_model = xgb.train(
        params,
        dtrain,
        num_boost_round=num_boost_round,
        verbose_eval=verbose_eval,
        evals=watchlist)
    params['n_estimators']=num_boost_round
    
    return(best_model, params)

def create_prediction(train, test, target, kbest_score_func, metric, params, numeric_features=[], categorical_features=[], scaled=False, k_selected = 'all', test_size = 0.2, Skfold=False, Verbose = False, testing=True):
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    import pandas as pd
    from prepare_and_scale_data import prepare_and_scale_data

    data = pd.DataFrame()
    train_scaled = pd.DataFrame()
    train_non_scaled = pd.DataFrame()
    test_scaled = pd.DataFrame()
    test_non_scaled = pd.DataFrame()

    
    #split the initial train dataframe to test/train dataframes
    
    data, train_scaled, train_non_scaled, test_scaled, test_non_scaled = prepare_and_scale_data(train, test, numeric_features, categorical_features)
    y_train = data[target]
    
    if scaled:
        X_train, X_test, y_train, y_test = train_test_split(train_scaled, y_train, test_size=test_size)
        test = test_scaled
    else:
        X_train, X_test, y_train, y_test = train_test_split(train_non_scaled, y_train, test_size=test_size)
        test = test_non_scaled

    features_df = select_kbest(X_train, y_train, kbest_score_func,k_selected)
    
    dXtrain = xgb.DMatrix(X_train, label=y_train)
    dXtest = xgb.DMatrix(X_test, label=y_test)
    watchlist = [(dXtrain, 'train'), (dXtest, 'test')]
    model, params = hyperparameter_grid(params, dXtrain, metric, watchlist, testing, Skfold, Verbose)
    
    #Available importance_types = [‘weight’, ‘gain’, ‘cover’, ‘total_gain’, ‘total_cover’]
    importance_df = pd.DataFrame()
    for importance_type in ['weight', 'gain', 'cover', 'total_gain', 'total_cover']:
        importance = model.get_score(importance_type=importance_type)
        temp = pd.DataFrame.from_dict(importance, orient='index', columns=['Score'])
        temp['Importance type'] = importance_type
        importance_df = pd.concat([importance_df, temp])
    
    importance_df.reset_index(inplace=True)
    importance_df.rename(columns={'index':'Feature'}, inplace=True)
    importance_df.sort_values(['Importance type', 'Score'], inplace=True, ascending=False)
    importance_df.reset_index(inplace=True, drop=True)


    if scaled:
        dtest = xgb.DMatrix(test_scaled)
    else:
        dtest = xgb.DMatrix(test_non_scaled)

    #test_pred = xgb.DMatrix(test_scale, label=y_data)
    y_pred = model.predict(dtest)
    data.loc[:, "Ennustettu " + target] = y_pred
    
    return(data, test, features_df, importance_df, model, params, dXtest, X_train, y_train, X_test, y_test)