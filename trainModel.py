import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import L2
from tensorflow.keras.metrics import MeanSquaredError

from sklearn.model_selection import train_test_split


class Train_Model:
    """This model is used to do the entire training of deep learning model"""
    model = Sequential([
                Dense(units = 544, input_shape = (50,), activation = 'relu'),
                Dense(units = 832, activation = 'relu'),
                Dense(units = 800, activation = 'relu'),
                Dense(units = 608, activation = 'relu'),
                Dense(units = 9, activation = 'relu')
                ])
    
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train
        
    def trainValSplit(self):
        x_train, x_val, y_train, y_val = train_test_split(self.x_train, self.y_train, random_state=1, test_size=0.25)
        return x_train, x_val, y_train, y_val
        
    def trainModel(self):
        x_train, x_val, y_train, y_val = self.trainValSplit()
        model = self.model
        callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
        for lr in [0.00103, 0.00102, 0.00101, 0.00100] * 2:
            model.compile(optimizer=Adam(learning_rate=lr), loss="MeanSquaredError", metrics=["MeanAbsoluteError"])
            history = model.fit(x_train, y_train, validation_data=(x_val, y_val), batch_size=64, epochs=90, shuffle=True, callbacks=[callback])
            
        model.save('Best_Model/Best_model.h5')

        return "training completed successfully"
    
    
