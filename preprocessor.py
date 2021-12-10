from sklearn.preprocessing import MinMaxScaler
import pickle

class Preprocess:
    """this class will carry out the preprocessing the training and prediction data 
    """
    def __init__(self, data):
        self.data = data
        
    def splitFeaturesAndTarget(self, data):
        train_x = data.iloc[:, 0:50]
        train_y = data.iloc[:, 50:59]
        return train_x, train_y
    
    def minMaxScalingTrain(self, x_train):
        scaler = MinMaxScaler()
        scaler.fit(x_train)
        pickle.dump(scaler, open('Scaler/minmaxScaler.sav', 'wb'))
        x_array = scaler.transform(x_train)
        return x_array
        
    
    def preprocessTrain(self):
        data = self.data
        x_train, y_train = self.splitFeaturesAndTarget(data)
        x_train = self.minMaxScalingTrain(x_train)
        y_train = y_train.to_numpy()
        return x_train, y_train