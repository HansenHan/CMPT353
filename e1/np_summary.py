#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']


# In[3]:


sum_row = np.sum(totals, axis = 1)
print('Row with lowest total precipitation:')
print(np.argmin(sum_row, axis = 0))


# In[4]:


sum_totals1 = np.sum(totals, axis = 0)
sum_counts1 = np.sum(counts, axis = 0)
print('Average precipitation in each month:')
print(sum_totals1/sum_counts1)


# In[5]:


sum_totals2 = np.sum(totals, axis = 1)
sum_counts2 = np.sum(counts, axis = 1)
print('Average precipitation in each city:')
print(sum_totals2/sum_counts2)


# In[6]:


new_totals = np.reshape(totals,(9,4,3))
quater_totals = np.sum(new_totals,axis = 2)
print('Quarterly precipitation totals:')
print(quater_totals)

