#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import sys
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd


# In[2]:


data = pd.read_csv('data.csv')
# data


# In[3]:


# plt.hist(data['qs1'])
# plt.show()


# In[4]:


mean = data.agg('mean')
mean = mean.sort_values()
mean = pd.DataFrame(mean, columns = ['mean_time']) 
# print(mean)


# In[5]:


anova = stats.f_oneway(data['qs1'],data['qs2'],data['qs3'],data['qs4'],data['qs5'],data['merge1'],data['partition_sort'])
# anova


# In[6]:


data_melt = pd.melt(data)
posthoc = pairwise_tukeyhsd(
    data_melt['value'], data_melt['variable'],
    alpha=0.05)
# print(posthoc)


# In[7]:


print('Mean running times for the 7 sorting methods:')
print(mean)
print('The ANOVA p_value is:', anova.pvalue, ' which means there is a difference among the mean running times for different sorting methods.')
print('Here is the posthoc table')
print(posthoc)

