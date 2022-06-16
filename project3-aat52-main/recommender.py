# from requests import get
# import json
# from datetime import datetime, timedelta, date
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine
# from scipy.stats import pearsonr

# import csv
# import re
import pandas as pd
# import argparse
# import collections
# import json
# import glob
import math
# import os
# import requests
# import string
import sys
# import time
# import xml
# import random





class Recommender(object):
  def __init__(self, training_set, test_set):
    if isinstance(training_set, str):
      # the training set is a file name
      self.training_set = pd.read_csv(training_set)
    else:
      # the training set is a DataFrame
      self.training_set = training_set.copy()

    if isinstance(test_set, str):
      # the test set is a file name
      self.test_set = pd.read_csv(test_set)
    else:
      # the test set is a DataFrame
      self.test_set = test_set.copy()

  def train_user_euclidean(self, data_set, userId):
    sim_weights = {}
    for user in data_set:
        if (user != 'movieId' and user != userId):
            data_set_subset = data_set[[userId,user]][data_set[userId].notnull() & data_set[user].notnull()]
            dist = euclidean(data_set_subset[userId], data_set_subset[user])
            sim_weights[user] = 1.0 / (1.0 + dist)
    return sim_weights  # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}

  def train_user_manhattan(self, data_set, userId):
    sim_weights = {}
    for user in data_set:
        if (user != 'movieId' and user != userId):
            data_set_subset = data_set[[userId,user]][data_set[userId].notnull() & data_set[user].notnull()]
            dist = cityblock(data_set_subset[userId], data_set_subset[user])
            sim_weights[user] = 1.0 / (1.0 + dist)
    return sim_weights # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}

  def train_user_cosine(self, data_set, userId):
    sim_weights = {}
    for user in data_set.columns[1:]:
        if (user != 'movieId' and user != userId):
            data_set_subset = data_set[[userId,user]][data_set[userId].notnull() & data_set[user].notnull()]
            if (data_set_subset.empty):
                sim_weights[user] = 0
            else:
                sim_weights[user] = cosine(data_set_subset[userId], data_set_subset[user])
    return sim_weights # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}

  def train_user_pearson(self, data_set, userId):
    vec1 = data_set[userId]
    simdict = {}
    for user in data_set:
      if user != "movieId" and user != userId:
        simdict[user] = self.pear_dist(vec1,data_set[user])
    return simdict  # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}

  def cos_dist(self,vector1,vector2):
    summ = 0
    summ1 = 0
    summ2 = 0
    for index in range(0,len(vector1)-1):
      if pd.isna(vector1[index]) or pd.isna(vector2[index]):
        continue
      summ1 += vector1[index] * vector1[index]
      summ2 += vector2[index] * vector2[index]
      summ +=  vector2[index] * vector1[index]
    summ1 = math.sqrt(summ1)
    summ2 = math.sqrt(summ2)
    bot = summ1 * summ2
    cos_dist = summ / bot
    return cos_dist

  def eu_dist(self,vector1,vector2):
    summ = 0
    for index in range(0,len(vector1)-1):
      if pd.isna(vector1[index]) or pd.isna(vector2[index]):
        continue
      summ += (vector2[index] - vector1[index])**2
    summ = math.sqrt(summ)
    return summ

  def man_dist(self,vector1,vector2):
    summ = 0
    for index in range(0,len(vector1)-1):
      if pd.isna(vector1[index]) or pd.isna(vector2[index]):
        continue
      summ += abs(vector2[index] - vector1[index])
    return summ

  def pear_dist(self,vector1,vector2):
    return vector1.corr(vector2)



  def train_user(self, data_set, distance_function, userId):
    if distance_function == 'euclidean':
      return self.train_user_euclidean(data_set, userId)
    elif distance_function == 'manhattan':
      return self.train_user_manhattan(data_set, userId)
    elif distance_function == 'cosine':
      return self.train_user_cosine(data_set, userId)
    elif distance_function == 'pearson':
      return self.train_user_pearson(data_set, userId)
    else:
      return None

  def get_user_existing_ratings(self, data_set, userId):
      tuples = []

      ratings = data_set[['movieId', userId]].copy()
      ratings = ratings[ratings[userId].notnull()]
      tuples = ratings.apply(tuple, axis = 1).tolist()
      return tuples # list of tuples with movieId and rating. e.g. [(32, 4.0), (50, 4.0)]

  def predict_user_existing_ratings_top_k(self, data_set, sim_weights, userId, k):
     sim_top = sorted(sim_weights.items(), key=lambda x:x[1], reverse=True)[:k]
     sim_top = dict(sim_top)
     predictions = []
     for index, row in data_set.iterrows():
         if (not np.isnan(row[userId])):
             predicted_rating = 0
             weights_sum = 0.0
             ratings = data_set.iloc[index][1:]
             for user in data_set.columns[1:]:
                 if (user != userId):
                     if (not np.isnan(ratings[user]) and user in sim_top.keys()):
                         predicted_rating += ratings[user] * sim_top[user]
                         weights_sum += sim_top[user]
             if (weights_sum != 0):
                 predicted_rating /= weights_sum
                 predictions.append((row['movieId'], predicted_rating))
     return predictions # list of tuples with movieId and rating. e.g. [(32, 4.0), (50, 4.0)]

  def evaluate(self,existing_ratings, predicted_ratings):
      existing = self.tuple_list_to_dict(existing_ratings)
      predicted = self.tuple_list_to_dict(predicted_ratings)
      resids2 = 0
      n = 0
      # print(existing)
      # print(predicted)
      beegn = len(existing_ratings)
      for key in predicted:
        if not pd.isna(existing[key]):
          if not pd.isna(predicted[key]):
            n+=1
            # print(existing[key])
            # print(predicted[key])
            resids2 += (existing[key] - predicted[key])**2
            #print(resids2)
        else:
          beegn -= 1
      mse = resids2/n
      rmse = math.sqrt(mse)
      ratio = n / beegn
      # print(rmse)
      # print(ratio)
      return {'rmse':rmse, 'ratio':ratio} # dictionary with an rmse value and a ratio. e.g. {'rmse':1.2, 'ratio':0.5}

  def tuple_list_to_dict(self,tuplelist):
    usable = {}
    for element in tuplelist:
      usable[element[0]] = element[1]
    return usable

  def single_calculation(self, distance_function, userId, k_values):
    user_existing_ratings = self.get_user_existing_ratings(self.test_set, userId)
    print("User has {} existing and {} missing movie ratings".format(len(user_existing_ratings), len(self.test_set) - len(user_existing_ratings)), file=sys.stderr)

    print('Building weights')
    sim_weights = self.train_user(self.training_set[self.test_set.columns.values.tolist()], distance_function, userId)

    result = []
    for k in k_values:
      print('Calculating top-k user prediction with k={}'.format(k))
      top_k_existing_ratings_prediction = self.predict_user_existing_ratings_top_k(self.test_set, sim_weights, userId, k)
      result.append((k, self.evaluate(user_existing_ratings, top_k_existing_ratings_prediction)))
    return result # list of tuples, each of which has the k value and the result of the evaluation. e.g. [(1, {'rmse':1.2, 'ratio':0.5}), (2, {'rmse':1.0, 'ratio':0.9})]

  def aggregate_calculation(self, distance_functions, userId, k_values):
    print()
    result_per_k = {}
    for func in distance_functions:
      print("Calculating for {} distance metric".format(func))
      for calc in self.single_calculation(func, userId, k_values):
        if calc[0] not in result_per_k:
          result_per_k[calc[0]] = {}
        result_per_k[calc[0]]['{}_rmse'.format(func)] = calc[1]['rmse']
        result_per_k[calc[0]]['{}_ratio'.format(func)] = calc[1]['ratio']
      print()
    result = []
    for k in k_values:
      row = {'k':k}
      row.update(result_per_k[k])
      result.append(row)
    columns = ['k']
    for func in distance_functions:
      columns.append('{}_rmse'.format(func))
      columns.append('{}_ratio'.format(func))
    result = pd.DataFrame(result, columns=columns)
    return result

if __name__ == "__main__":
    recommender = Recommender("data/train.csv", "data/small_test.csv")
    print("Training set has {} users and {} movies".format(len(recommender.training_set.columns[1:]), len(recommender.training_set)))
    print("Testing set has {} users and {} movies".format(len(recommender.test_set.columns[1:]), len(recommender.test_set)))

    result = recommender.aggregate_calculation(['euclidean', 'cosine', 'pearson', 'manhattan'], "0331949b45", [1, 2, 3, 4])
    print(result)
