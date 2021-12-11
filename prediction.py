from tensorflow.keras.models import load_model
import pandas as pd

class Predict_Output:
    """this class predicts the output of the input data passed in 
    """
    def __init__(self, data_arr):
        self.array = data_arr
        
    def predictOutput(self):
        model = load_model('Best_Model/Best_model.h5')
        prediction = model.predict(self.array)
        df = pd.DataFrame(prediction)
        return df