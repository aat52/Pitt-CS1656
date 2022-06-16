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

    def t1(self):
        df = pd.read_csv('http://data.cs1656.org/bike_share.csv')
        self.bike_data = df.sample(1000)
        train = self.bike_data.iloc[0:900]
        train_x = train[['weekday']].values
        train_y = train[['cnt']].values

        test=self.bike_data.iloc[900:]
        test_x = test[['weekday']].values
        test_y = test[['cnt']].values

        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(train_x, train_y)

        predict_y = regr.predict(test_x)

        meansq_error = np.mean((predict_y - test_y) ** 2)
        return meansq_error

    def t2_1(self):
        df = pd.read_csv('http://data.cs1656.org/bike_share.csv')
        self.bike_data = df.sample(1000)
        train = self.bike_data.iloc[0:900]
        train_x = train[['season','hr','holiday','weekday','workingday','weathersit','temp','temp_feels','hum','windspeed']].values
        train_y = train[['cnt']].values

        test=self.bike_data.iloc[900:]
        test_x = test[['season','hr','holiday','weekday','workingday','weathersit','temp','temp_feels','hum','windspeed']].values
        test_y = test[['cnt']].values

        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(train_x, train_y)

        predict_y = regr.predict(test_x)

        meansq_error = np.mean((predict_y - test_y) ** 2)
        return meansq_error
        #2.2 The mean squared error is lower. The lower the MSE, the closer it is to the forecasted value, so generally a lower value is better. However, using too many attributes can skew the data so you have to be mindful of that when calculating MSE.

    def t3(self):
        dt = pd.read_csv('http://data.cs1656.org/bank-data.csv')
        dt['sex'] = dt['sex'].replace(['FEMALE', 'MALE'], [1, 2])
        dt['married'] = dt['married'].replace(['YES', 'NO'], [1, 2])
        dt['mortgage'] = dt['mortgage'].replace(['YES', 'NO'], [1, 2])
        dt['region'] = dt['region'].replace(['INNER_CITY', 'TOWN','RURAL','SUBURBAN'], [1, 2, 3, 4])
        dt_train_x = dt.iloc[:500][['region','sex','married']].values
        dt_train_y = dt.iloc[:500][['mortgage']].values

        dt_test_x = dt.iloc[500:][['region','sex','married']].values
        dt_test_y = dt.iloc[500:][['mortgage']].values
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(dt_train_x, dt_train_y)

        dt_predict_y = clf.predict(dt_test_x)
        accuracy = metrics.accuracy_score(dt_test_y,dt_predict_y)
        return accuracy

if __name__ == "__main__":
    t = Task(pd.read_csv('http://data.cs1656.org/bike_share.csv'), pd.read_csv('http://data.cs1656.org/bank-data.csv'))
    print("---------- Task 1 ----------")
    print(t.t1())
    print("--------- Task 2.1 ---------")
    print(t.t2_1())
    print("---------- Task 3 ----------")
    print(t.t3())
