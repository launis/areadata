def plot_history(hist):
    import matplotlib.pyplot as plt

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Squared Error')
    plt.plot(hist['epoch'], hist['mean_squared_error'],
           label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_squared_error'],
           label = 'Val Error')
    plt.legend()
    plt.show()
    
    
def create_neuro_prediction(train, test, target, mainpath, numeric_features=[], categorical_features=[], scaled=True, test_size = 0.2, Skfold=False):
    
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import train_test_split        
    import numpy as np
    import pandas as pd

    import tensorflow as tf  
   
    from prepare_and_scale_data import prepare_and_scale_data
    from get_compiled_model import get_compiled_model
    from create_tensorpad_path import create_tensorpad_path
    
    #split the initial train dataframe to test/train dataframes
 
    data, train_scaled, train_non_scaled, test_scaled, test_non_scaled = prepare_and_scale_data(train, test, numeric_features, categorical_features)
    y_train = data[target]
    
    if scaled:
        X_train, X_test, y_train, y_test = train_test_split(train_scaled, y_train, test_size=test_size)
        test = test_scaled
    else:
        X_train, X_test, y_train, y_test = train_test_split(train_non_scaled, y_train, test_size=test_size)
        test = test_non_scaled

    
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=test_size)

    # Prepare the training dataset
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train.values, y_train.values))
    train_dataset = train_dataset.shuffle(buffer_size=1024).batch(32)

    # Prepare the test dataset
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test.values, y_test.values))
    test_dataset = test_dataset.batch(32)

    # Prepare the validation dataset
    val_dataset = tf.data.Dataset.from_tensor_slices((X_val.values, y_val.values))
    val_dataset = val_dataset.batch(32)

    log_path, log_dir = create_tensorpad_path(mainpath)
    model, callbacks = get_compiled_model(X_train, target, log_dir)

    history = model.fit(train_dataset, epochs=50, validation_data=val_dataset, callbacks=callbacks)

    result = model.evaluate(test_dataset)
    print(dict(zip(model.metrics_names, result)))


    pred_train = model.predict(X_train)
    print(np.sqrt(mean_squared_error(y_train,pred_train)))

    pred = model.predict(X_test)
    print(np.sqrt(mean_squared_error(y_test,pred)))

    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    if scaled:
        pred_all = model.predict(test_scaled)
    else:
        pred_all = model.predict(test_non_scaled)

    pred_df = pd.DataFrame(pred_all, columns = target)

    for t in target:
        data.loc[:, "Ennustettu " + t] = pred_df[t]
    return(data, test, model, hist, log_path)