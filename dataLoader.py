import pandas as pd

class Load_Data:
    """This class is to load the csv data as pandas dataframe after cleaning data
    """
    def __init__(self):
        self.train_path = 'traindata/trussDAdata.csv'
        
    def loadData(self):
        data = pd.read_csv(self.train_path, header=None, skiprows=1)
        data = data.round(decimals = 6)
        return data