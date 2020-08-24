
def get_compiled_model(X, target, log_dir):

    import tensorflow as tf
    from tensorflow import keras

    from tensorflow.keras.layers import Input, Dense
    from tensorflow.keras.models import Model
    
    input_layer = Input(shape=(X.values.shape[1]), name='Areadata')
    dense_layer_1 = Dense(64, activation='relu', name='Dense_1')(input_layer)
    dense_layer_2 = Dense(64, activation='relu', name='Dense_2')(dense_layer_1)
    dense_layer_3 = Dense(64, activation='relu', name='Dense_3')(dense_layer_2)
    dense_layer_4 = Dense(64, activation='relu', name='Dense_4')(dense_layer_3)
    dense_layer_5 = Dense(64, activation='relu', name='Dense_5')(dense_layer_4)
    dense_layer_6 = Dense(64, activation='relu', name='Dense_6')(dense_layer_5)
    out = Dense(len(target), activation='linear', name='Party_shares')(dense_layer_6)
    
    model = Model(inputs=input_layer, outputs=[out],  name="areadata_model")
        
    initial_learning_rate = 0.0001
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate,
        decay_steps=10000,
        decay_rate=0.96,
        staircase=True)

    optimizer=tf.optimizers.Adam(learning_rate=lr_schedule)
    
    model.compile(
        optimizer=optimizer,
        loss=['mean_squared_error'],
        metrics=["mean_squared_error"])
    
    earlystopping_callback = keras.callbacks.EarlyStopping(
            # Stop training when `val_loss` is no longer improving
            monitor="val_loss",
            # "no longer improving" being defined as "no better than 1e-2 less"
            min_delta=0.001,
            # "no longer improving" being further defined as "for at least 2 epochs"
            patience=50,
            verbose=1)

    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    callbacks = [earlystopping_callback, tensorboard_callback]

    return(model, callbacks)