#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
from requests import get
import json
import csv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# In[6]:


class Task(object):
    def __init__(self):
        self.response = get('http://db.cs.pitt.edu/courses/cs1656/data/hours.json', verify=False) 
        self.hours = json.loads(self.response.content) 

    def part4(self):
        #For this part, you must use `self.hours` we defined in part 3, 
        #and store its data as a CSV file (hours.csv), 
        #with the fields `name`, `day` and `time`. 
        #You should look up the `csv` module and the `writer()` function in particular. 
        #The command to open the csv file for writing is already in the template, 
        #so, don't change it.
        hours = csv.writer(open("hours.csv", "w"))
        hours.writerow(["name", "day", "time"])
        for x in self.hours:
            hours.writerow([x["name"],
                        x["day"],
                        x["time"]])
       
    def part5(self):
            #For this part, you must open the CSV file created from part 4,
            #read its contents, and write them in the file `part5.txt`.
        f = open('part5.txt', 'w') 
        with open('hours.csv','r') as g:
            data = g.readlines()
        for row in data:
            f.write(row)
        f.close()


    def part6(self):
            #For this part, you must open the CSV file again, 
            #but this time you must parse it using `csv.reader()`, 
            #and write only the rows, one row at a time, in the file `part6.txt`.
        with open('hours.csv', 'r') as f:
            reader = csv.reader(f)
            g = open("part6.txt",'w')
            for row in reader:
                g.write(str(row))


    def part7(self):
            #For this part, you must open the CSV file again, parse it using `csv.reader()`,
            #iterate through the rows, and write every cell, one cell at a time, in the 
            #file `part7.txt`.
        with open('hours.csv', 'r') as f:
            reader = csv.reader(f)
            g = open("part7.txt",'w')
            for row in reader:
                bonk2 = str(row).replace("\'","").replace("[","").replace("]","")
                bonk = bonk2.split(",")
                for item in bonk:
                    if item[0] == " ":
                        item = item[1:]
                    g.write(item)



# In[5]:


if __name__ == '__main__':
    task = Task()
    #task.part4()
    #task.part5()
    #task.part6()
    #task.part7()


# In[ ]:



    

