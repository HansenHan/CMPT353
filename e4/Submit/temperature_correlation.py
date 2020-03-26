#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import math


# In[ ]:


file1 = sys.argv[1]
file2 = sys.argv[2]
result = sys.argv[3]


# In[2]:


#This is found from:
#https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
def distance_TWO_points(lat1,lon1,lat2,lon2):
    R = 6371 # Radius of the earth in km
    dLat = math.radians(lat2-lat1)  #deg2rad below
    dLon = math.radians(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dis = R * c # Distance in km
    return dis
dis_F = np.vectorize(distance_TWO_points)

def distance(city, stations):
    stations['distance'] = dis_F(city['latitude'],city['longitude'],stations['latitude'],stations['longitude'])
    return stations['distance']

def best_tmax(city, stations):
    stations['distance'] = distance(city, stations)
    return stations['avg_tmax'][stations['distance'].idxmin()]


# In[3]:


# stations = pd.read_json('stations.json.gz', lines=True)
stations = pd.read_json(file1, lines=True)

stations['avg_tmax'] = stations['avg_tmax']/10
# stations


# In[4]:


# city = pd.read_csv('city_data.csv').dropna()
city = pd.read_csv(file2).dropna()

# print(city)
city['area'] = city['area']/1000000
city = city[city['area'] <= 10000].reset_index(drop=True)
# print(city)


# In[5]:


# The function blow is learned from https://blog.csdn.net/qq_19528953/article/details/79348929
city['best_tmax'] = city.apply(best_tmax, axis = 1, stations = stations)
city['density'] = city['population']/city['area']
# city


# In[7]:


plt.plot(city['best_tmax'],city['density'], 'b.')
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
# plt.show()


# In[ ]:


plt.savefig(result)

