# import argparse
# import collections
# import csv
import json
# import glob
import math
# import os
# import pandas
# import re
import requests
# import string
# import sys
# import time
# import xml

class Bike():
  def __init__(self, baseURL, station_info, station_status):
    # initialize the instance
    #baseURL is https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en
    #station_infoURL = baseURL+'/station_information.json'
    #station_statusURL = baseURL+'/station_status.json'
    self.baseURL = baseURL
    self.station_info = baseURL + station_info
    self.station_status = baseURL + station_status

  def total_bikes(self):
    page = requests.get(self.station_status)
    data = json.loads(page.content)
    total = 0
    for point in data["data"]["stations"]:
      total += int(point["num_bikes_available"])
    return total

  def total_docks(self):
    page = requests.get(self.station_status)
    data = json.loads(page.content)
    total = 0
    for point in data["data"]["stations"]:
      total += int(point["num_docks_available"])
    return total

  def percent_avail(self, station_id):
    page = requests.get(self.station_status)
    data = json.loads(page.content)
    station = ""
    for point in data["data"]["stations"]:
      if point["station_id"] == str(station_id):
        station = point
        break
    if station == "":
      return station
    else:
      perc = math.floor(((station["num_docks_available"]) / (station["num_docks_available"]  + station["num_bikes_available"])) * 100)
      percstr = str(perc) + "%"
      return percstr

  def percent_avail_useful(self, station_id, data):
    for point in data["data"]["stations"]:
      if point["station_id"] == str(station_id):
        station = point
        break
    if station["num_docks_available"] == 0:
      return 0
    else:
      perc = ((station["num_docks_available"]) / (station["num_docks_available"]  + station["num_bikes_available"]))
      return perc

  def closest_stations(self, latitude, longitude):
    # return the stations closest to the given coordinates
    page = requests.get(self.station_info)
    data = json.loads(page.content)
    least = data["data"]["stations"][1]
    mindist = self.distance(latitude,longitude,least["lat"],least["lon"])
    for point in data["data"]["stations"]:
      dist = self.distance(latitude,longitude,point["lat"],point["lon"])
      if dist < mindist:
        least = point
        mindist = dist

    data["data"]["stations"].remove(least)
    least2 = data["data"]["stations"][1]
    mindist = self.distance(latitude,longitude,least2["lat"],least2["lon"])
    for point in data["data"]["stations"]:
      if point["station_id"] == least["station_id"]: continue
      dist = self.distance(latitude,longitude,point["lat"],point["lon"])
      if dist < mindist:
        least2 = point
        mindist = dist

    data["data"]["stations"].remove(least2)
    least3 = data["data"]["stations"][1]
    mindist = self.distance(latitude,longitude,least3["lat"],least3["lon"])
    for point in data["data"]["stations"]:
      if point["station_id"] == least["station_id"]: continue
      dist = self.distance(latitude,longitude,point["lat"],point["lon"])
      if dist < mindist:
        least3 = point
        mindist = dist
    out = {least["station_id"]: least["name"], least2["station_id"]: least2["name"], least3["station_id"]: least3["name"]}
    return out


  def closest_bike(self, latitude, longitude):
    page = requests.get(self.station_info)
    data = json.loads(page.content)
    page2 = requests.get(self.station_status)
    data2 = json.loads(page2.content)
    first = True
    for point in data["data"]["stations"]:
      if self.percent_avail_useful(int(point["station_id"]),data2) == 1:
        continue
      if first:
        first = False
        least = point
        mindist = self.distance(latitude,longitude,point["lat"],point["lon"])
        continue
      dist = self.distance(latitude,longitude,point["lat"],point["lon"])
      if dist < mindist:
        least = point
        mindist = dist
    return {least["station_id"] : least["name"]}

  def station_bike_avail(self, latitude, longitude):
    # return the station id and available bikes that correspond to the station with the given coordinates
    page = requests.get(self.station_info)
    data = json.loads(page.content)
    station = {}
    for point in data["data"]["stations"]:
      if (float(point["lat"]) == latitude) and (float(point["lon"]) == longitude):
        station = point
        break
    if station == {}:
      return station
    else:
      page = requests.get(self.station_status)
      data = json.loads(page.content)
      for point in data["data"]["stations"]:
        if point["station_id"] == station["station_id"]:
          out = {station["station_id"] : int(point["num_bikes_available"])}
          return out


  def distance(self, lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p)*math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p)) / 2
    return 12742 * math.asin(math.sqrt(a))



#testing and debugging the Bike class

if __name__ == '__main__':
    instance = Bike('https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en', '/station_information.json', '/station_status.json')
    print('------------------total_bikes()-------------------')
    t_bikes = instance.total_bikes()
    print(type(t_bikes))
    print(t_bikes)
    print()

    print('------------------total_docks()-------------------')
    t_docks = instance.total_docks()
    print(type(t_docks))
    print(t_docks)
    print()

    print('-----------------percent_avail()------------------')
    p_avail = instance.percent_avail(342885) # replace with station ID
    print(type(p_avail))
    print(p_avail)
    print()

    print('----------------closest_stations()----------------')
    c_stations = instance.closest_stations(40.444618, -79.954707) # replace with latitude and longitude
    print(type(c_stations))
    print(c_stations)
    print()

    print('-----------------closest_bike()-------------------')
    c_bike = instance.closest_bike(40.444618, -79.954707) # replace with latitude and longitude
    print(type(c_bike))
    print(c_bike)
    print()

    print('---------------station_bike_avail()---------------')
    s_bike_avail = instance.station_bike_avail(40.438761, -79.997436) # replace with exact latitude and longitude of station
    print(type(s_bike_avail))
    print(s_bike_avail)
