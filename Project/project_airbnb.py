#!/usr/bin/env python
# coding: utf-8

# In[1]:


from xml.dom.minidom import parse, parseString
import pandas as pd
import numpy as np
import sys
import math
from pykalman import KalmanFilter


# In[ ]:


data1 = pd.read_json('amenities-vancouver.json.gz', lines=True)
data2 = pd.read_csv('Airbnb_datalist.csv')


# In[ ]:


data1


# In[ ]:


print(data2)


# In[ ]:


# def get_data(file):
#     N_file = parse(file)
#     data = N_file.getElementsByTagName('trkpt')
#     result_data = pd.DataFrame(columns=['lat', 'lon'])
#     for i in range(len(data)):
#         result_data.loc[i]=float(data[i].attributes['lat'].value), float(data[i].attributes['lon'].value)
#     return result_data

# #This is found from:
# #https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
# def distance_TWO_points(lat1,lon1,lat2,lon2):
#     R = 6371 # Radius of the earth in km
#     dLat = math.radians(lat2-lat1)  #deg2rad below
#     dLon = math.radians(lon2-lon1)
#     a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#     dis = R * c # Distance in km
#     return dis
# dis_F = np.vectorize(distance_TWO_points)

# def distance(data):
#     data['distance'] = dis_F(data['lat'],data['lon'],data['lat'].shift(-1),data['lon'].shift(-1))
#     dis_sum = data['distance'].sum()
#     del data['distance']
#     return dis_sum * 1000

# def smooth(data):
#     initial_state = data.iloc[0]
#     observation_covariance = np.diag([15/10**5, 15/10**5]) ** 2
#     transition_covariance = np.diag([8/10**5,8/10**5]) ** 2
#     transition = [[1, 0], [0, 1]]
#     kf = KalmanFilter(initial_state_mean=initial_state,
#                 initial_state_covariance=observation_covariance,
#                 observation_covariance=observation_covariance,
#                 transition_covariance=transition_covariance,
#                 transition_matrices=transition)
#     kalman_smoothed, _ = kf.smooth(data)
#     result = pd.DataFrame(kalman_smoothed,columns=['lat','lon'])
#     return result

# def output_gpx(points, output_filename):
#     """
#     Output a GPX file with latitude and longitude from the points DataFrame.
#     """
#     from xml.dom.minidom import getDOMImplementation
#     def append_trkpt(pt, trkseg, doc):
#         trkpt = doc.createElement('trkpt')
#         trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
#         trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
#         trkseg.appendChild(trkpt)
    
#     doc = getDOMImplementation().createDocument(None, 'gpx', None)
#     trk = doc.createElement('trk')
#     doc.documentElement.appendChild(trk)
#     trkseg = doc.createElement('trkseg')
#     trk.appendChild(trkseg)
    
#     points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
#     with open(output_filename, 'w') as fh:
#         doc.writexml(fh, indent=' ')


# In[ ]:



# def main():
#     points = get_data(sys.argv[1])
#     print('Unfiltered distance: %0.2f' % (distance(points),))
    
#     smoothed_points = smooth(points)
#     print('Filtered distance: %0.2f' % (distance(smoothed_points),))
#     output_gpx(smoothed_points, 'out.gpx')


# if __name__ == '__main__':
#     main()

