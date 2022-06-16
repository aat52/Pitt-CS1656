import json
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
from sklearn import linear_model, tree, metrics
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Task(object):
    def __init__(self, bike_df, bank_df):
        np.random.seed(31415)
        self.bike_data = bike_df.sample(1000).copy()
        self.bank_data = bank_df.copy()

    def t1(self):
        return 0

    def t2_1(self):
        return 0
    
    def t3(self):
        return 0

if __name__ == "__main__":
    t = Task(pd.read_csv('http://data.cs1656.org/bike_share.csv'), pd.read_csv('http://data.cs1656.org/bank-data.csv'))
    print("---------- Task 1 ----------")
    print(t.t1())
    print("--------- Task 2.1 ---------")
    print(t.t2_1())
    print("---------- Task 3 ----------")
    print(t.t3())
