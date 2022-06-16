import json
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Task(object):
    def __init__(self, data):
        self.df = pd.read_csv(data)

    def t1(self, name):
        return []

    def t2(self, name):
        return []
    
    def t3(self, name):
        return []
        
if __name__ == "__main__":
    # using the class movie ratings data we collected in http://data.cs1656.org/movie_class_responses.csv
    t = Task('http://data.cs1656.org/movie_class_responses.csv')
    print(t.t1('BabyKangaroo'))
    print('------------------------------------')
    print(t.t2('BabyKangaroo'))
    print('------------------------------------')
    print(t.t3('BabyKangaroo'))
    print('------------------------------------')