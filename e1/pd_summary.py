#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[7]:


totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])


# In[3]:


sum_row = pd.DataFrame.sum(totals, axis = 1)
print('City with lowest total precipitation:')
print(sum_row.idxmin(axis = 0))


# In[4]:


sum_totals1 = pd.DataFrame.sum(totals, axis = 0)
sum_counts1 = pd.DataFrame.sum(counts, axis = 0)
print('Average precipitation in each month:')
print(sum_totals1/sum_counts1)


# In[5]:


sum_totals2 = pd.DataFrame.sum(totals, axis = 1)
sum_counts2 = pd.DataFrame.sum(counts, axis = 1)
print('Average precipitation in each city:')
print(sum_totals2/sum_counts2)

