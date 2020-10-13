

def one_value(gridsearch_params,
              param_a,
              params,
              dtrain,
              num_boost_round,
              early_stopping_rounds,
              Skfold=True,
              nfold = 3,
              Verbose =False):
    
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
    
    small_better = True    
    
    if Verbose == False:
        verbose_eval = 0
    else:
        verbose_eval = 10

    if small_better == True:
        result_best = float(999999)
    else:
        result_best = float(-999999)
    best_params = None
    metrics = params['eval_metric']

    for i in gridsearch_params:
        # Update our parameters
        if Verbose:
            print("xgb.cv with {}={}".format(param_a, i))
        params[param_a] = i
  
        # Run CV
        cv_results = xgb.cv(
            params,
            dtrain,
            verbose_eval = verbose_eval,
            num_boost_round = num_boost_round,
            early_stopping_rounds = early_stopping_rounds,
            stratified = Skfold,
            nfold=nfold,
            metrics=metrics)
        
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
        if Verbose:
            print("xgb.cv {} {} for {} rounds".format(metrics, result,  boost_rounds))
        
    print("Best xgb.cv params: {} {}, {}: {}".format(param_a, best_params, metrics, result_best))
    params[param_a] = best_params
    return(params)

def two_values(gridsearch_params,
               param_a,
               param_b,
               params,
               dtrain,
               num_boost_round,
               early_stopping_rounds,
               Skfold=True,
               nfold = 3,
               Verbose =False):

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
    
    small_better = True    
    if Verbose == False:
        verbose_eval = 0
    else:
        verbose_eval = 10
    
    if small_better == True:
        result_best = float(999999)
    else:
        result_best = float(-999999)
    best_params = None
    
    metrics = params['eval_metric']

    for i, j in gridsearch_params:
        # Update our parameters
 
        if Verbose:
            print("xgb.cv with {}={}, {}={}".format(param_a, i, param_b, j))
        params[param_a] = i
        params[param_b] = j
  
        # Run CV
        cv_results = xgb.cv(            
                params,
                dtrain,
                verbose_eval = verbose_eval,
                num_boost_round = num_boost_round,
                early_stopping_rounds = early_stopping_rounds,
                stratified = Skfold,
                nfold=nfold,
                metrics=metrics)
       
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
        if Verbose:
            print("xgb.cv {} {} for {} rounds".format(metrics, result, boost_rounds))
        
    print("Best xgb.cv params: {} {}, {} {}, {}: {}".format(param_a, best_params[0], param_b, best_params[1], metrics, result_best))
    
    params[param_a] = best_params[0]
    params[param_b] = best_params[1]
    return(params)

def hyperparameter_grid(params,
                        dtrain,
                        dvalidate,
                        testing=True,
                        Skfold=False,
                        Verbose =False):
    
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
    
    num_boost_round = 9999
    early_stopping_rounds = 50
    nfold=5
    watchlist = [(dtrain, 'train'), (dvalidate, 'test')]
    metrics = params['eval_metric']
    
    if Verbose == False:
        verbose_eval = 0
    else:
        verbose_eval = 10
    print("Initial parameters:")
    print(params)
    print()
    
    
    model = xgb.train(
        params,
        dtrain,
        verbose_eval = num_boost_round,
        num_boost_round = num_boost_round,
        early_stopping_rounds = early_stopping_rounds,
        evals = watchlist)
    
    if testing is not None:
        #for testing purposes a light set to save some time
        if testing:
            rounds=1
            print('testing')
            gridsearch_params_tree = [
                (i, j)
                for i in range(1,20)
                for j in range(1,20)
                ]
            gridsearch_params_0_1 = [i/5. for i in range(0,6)]
            gridsearch_params_0_1_deep = [i/5. for i in range(0,6)]
            gridsearch_params_gamma = [i/5. for i in range(0,26)]
            gridsearch_params_eta = [i/500 for i in range(0,201)]
            gridsearch_params_colsamp = [i/20 for i in range(12,21)]
        
            gridsearch_params_pair_0_1 = [
                (i0, i1)
                for i0 in gridsearch_params_0_1
                for i1 in gridsearch_params_0_1
                ]
        
            gridsearch_params_colsamp_pair_0_1 = [
                (i0, i1)
                for i0 in gridsearch_params_colsamp
                for i1 in gridsearch_params_colsamp
                ]

        else: #for real
            rounds=2
            print('for real')
            gridsearch_params_tree = [
                (i, j)
                for i in range(1,25)
                for j in range(1,25)
                ]
            gridsearch_params_0_1 = [i/20. for i in range(0,21)]
            gridsearch_params_0_1_deep = [i/50. for i in range(0,51)]
            gridsearch_params_gamma = [i/50. for i in range(0,251)]
            gridsearch_params_eta = [i/1000 for i in range(0,401)]
            gridsearch_params_colsamp = [i/50 for i in range(30,51)]

            gridsearch_params_pair_0_1 = [
                (i0, i1)
                for i0 in gridsearch_params_0_1_deep
                for i1 in gridsearch_params_0_1_deep
                ]
        
            gridsearch_params_colsamp_pair_0_1 = [
                (i0, i1)
                for i0 in gridsearch_params_colsamp
                for i1 in gridsearch_params_colsamp
                ]

    
        result_col = "test-" + metrics + "-mean"
        cv_results = xgb.cv(            
            params,
            dtrain,
            verbose_eval = verbose_eval,
            num_boost_round = num_boost_round,
            early_stopping_rounds = early_stopping_rounds,
            stratified = Skfold,
            nfold=nfold,
            metrics=metrics
            )
    
   
        print("Unoptimized xgb.cv params xgb.cv params: {}: {}".format(metrics, cv_results[result_col].min()))


        #Tries to do semi-automatic genetic model for hyperparameter selection
        for round in range(rounds):
    
            #Maximum depth/height of a tree
            #Minimum sum of instance weight (hessian) needed in a child
            param_a = 'max_depth'
            param_b = 'min_child_weight'
            params=two_values(gridsearch_params_tree, param_a, param_b, params, dtrain, num_boost_round, early_stopping_rounds,  Skfold, nfold, Verbose)


            #L1 regularization term on weights - alpha  - Lasso Regression 
            #adds “absolute value of magnitude” of coefficient as penalty term to the loss function.
            #L2 regularization term on weights - lambda  - Ridge Regression 
            #adds “squared magnitude” of coefficient as penalty term to the loss function.
            #the sample is so small, so most propably no effect
            param_a = 'lambda'
            param_b = 'alpha'
            params=two_values(gridsearch_params_pair_0_1 , param_a, param_b, params, dtrain,  num_boost_round, early_stopping_rounds, Skfold, nfold, Verbose)
            

            #Subsamble denotes the fraction of observations to be randomly samples for each tree.
            #Colsample_bytree enotes the fraction of columns to be randomly samples for each tree.
            param_a = 'colsample_bytree'
            param_b = 'subsample'
            params=two_values(gridsearch_params_colsamp_pair_0_1, param_a, param_b, params, dtrain, num_boost_round, early_stopping_rounds, Skfold, nfold, Verbose)
            
            #Same as learning_rate - this needs to be in sync with num_boost_round (alias n_tree parameter)
            param_a = 'eta'
            params=one_value(gridsearch_params_eta, param_a, params, dtrain, num_boost_round, early_stopping_rounds,  Skfold, nfold, Verbose)
        
            #Balance of positive and negative weights.  This is regression and binary classification only parameter.
            if params['objective'].startswith('reg'):
                param_a = 'scale_pos_weight'
                params=one_value(gridsearch_params_0_1_deep, param_a, params, dtrain, num_boost_round, early_stopping_rounds, Skfold, nfold, Verbose)

            #Gamma finds minimum loss reduction/min_split_loss required to make a further partition 
            param_a = 'gamma'
            params=one_value(gridsearch_params_gamma, param_a, params, dtrain, num_boost_round, early_stopping_rounds,  Skfold, nfold, Verbose)
    

        print('Found hyperparameters with {} rounds '.format(round+1))
        print(params)
        print()
    
        model = xgb.train(
            params,
            dtrain,
            verbose_eval = verbose_eval,
            num_boost_round = num_boost_round,
            early_stopping_rounds = early_stopping_rounds,
            evals = watchlist,
            )   
        
        num_boost_round = model.best_iteration + 1

        best_model = xgb.train(
            params,
            dtrain,
            verbose_eval = num_boost_round,
            num_boost_round = num_boost_round,
            evals = watchlist,
            )
        print('Best numboost {} '.format(num_boost_round))
        print()
    else:
        best_model = model
    
    return(best_model, params)

def optimize_one_par(filename_model, 
                     path, 
                     params,
                     par,
                     gridsearch_par,
                     dtrain,
                     dvalidate,
                     Skfold=False,
                     Verbose =False):
    
    """This function finds trainded model with one optimized hyperparameters with a loop

    """
    from create_prediction import one_value
    from saveloadmodel import save_obj
    import xgboost as xgb
    import os
    
    num_boost_round = 9999
    early_stopping_rounds = 50
    nfold=5
    
    watchlist = [(dtrain, 'train'), (dvalidate, 'test')]
    metrics = params['eval_metric']
    
    if Verbose == False:
        verbose_eval = 0
    else:
        verbose_eval = 10
    metrics = params['eval_metric']
    
    model = xgb.train(
        params,
        dtrain,
        verbose_eval = verbose_eval,
        num_boost_round = num_boost_round,
        early_stopping_rounds = early_stopping_rounds,
        evals = watchlist)

    result_col = "test-" + metrics + "-mean"
    cv_results = xgb.cv(
        params,
        dtrain,
        verbose_eval = num_boost_round,
        num_boost_round = num_boost_round,
        early_stopping_rounds = early_stopping_rounds,
        stratified = Skfold,
        nfold=nfold,
        metrics=metrics
        )
   
    print("Unoptimized xgb.cv params: {}: {}".format(metrics, cv_results[result_col].min()))
    params=one_value(gridsearch_par, par, params, dtrain, num_boost_round, early_stopping_rounds, Skfold=Skfold, nfold=nfold, Verbose=Verbose)

    print('Found hyperparameters ')
    print(params)
    print()
    
    model = xgb.train(
        params,
        dtrain,
        verbose_eval = verbose_eval,
        num_boost_round = num_boost_round,
        early_stopping_rounds = early_stopping_rounds,
        evals = watchlist,
        )   
        
    num_boost_round = model.best_iteration + 1

    best_model = xgb.train(
        params,
        dtrain,
        verbose_eval = 1,
        num_boost_round = num_boost_round,
        evals = watchlist,
        )
    
    filename_model = os.path.join(path, filename_model)
    save_obj(best_model, filename_model)
    
    return(best_model, params)



def create_prediction(filename_model,  path, train, test, target, params, numeric_features=[], categorical_features=[], scaled=False, test_size = 0.2, Skfold=False, Verbose = False, testing=True):
    import os
    import json
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    import pandas as pd
    from prepare_and_scale_data import prepare_and_scale_data
    from saveloadmodel import save_obj, load_obj

    data = pd.DataFrame()
    train_scaled = pd.DataFrame()
    train_non_scaled = pd.DataFrame()
    test_scaled = pd.DataFrame()
    test_non_scaled = pd.DataFrame()
    
    #split the initial train dataframe to test/train dataframes
    
    data, train_scaled, train_non_scaled, test, test_scaled, test_non_scaled= prepare_and_scale_data(train, test, numeric_features, categorical_features)
    y = data[target]

    if scaled:
        X_train, X_validate, y_train, y_validate = train_test_split(train_scaled, y, test_size=test_size, random_state=42)
        X = train_scaled
        X_test = test_scaled
    else:
        X_train, X_validate, y_train, y_validate = train_test_split(train_non_scaled, y, test_size=test_size, random_state=42)
        X = train_non_scaled
        X_test = test_non_scaled

    
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dvalidate = xgb.DMatrix(X_validate, label=y_validate)
    filename_model = os.path.join(path, filename_model)
    
    
    model_features = load_obj(filename_model)
    
    if model_features == None:
        model, params = hyperparameter_grid(params, dtrain, dvalidate, testing, Skfold, Verbose)
        model_features = {
            'model': model,
            'numeric_features': numeric_features,
            'categorical_features' : categorical_features
            }

        save_obj(model_features, filename_model)
    else:
        model = model_features['model']
        config = model.save_config()
        
        list_of_float_params = ['max_depth', 'min_child_weight', 'lambda', 'alpha', 'colsample_bytree', 'subsample', 'eta', 'gamma']
        list_of_int_params = ['max_depth', 'min_child_weight']
        for par in list_of_float_params:
            params[par] = float(json.loads(config)["learner"]["gradient_booster"]["updater"]["prune"]["train_param"][par])
        for par in list_of_int_params:
            params[par] = int(json.loads(config)["learner"]["gradient_booster"]["updater"]["prune"]["train_param"][par])
        if params['objective'].startswith('reg'):
            params["scale_pos_weight"] = float(json.loads(config)["learner"]["objective"]["reg_loss_param"]["scale_pos_weight"])


        
    dtest = xgb.DMatrix(X_test)
    #test_pred = xgb.DMatrix(test_scale, label=y_data)
    y_test_pred = model.predict(dtest)
    
    return(data, X, y, test, X_test, y_test_pred, model, params)