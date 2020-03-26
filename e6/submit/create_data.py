#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import time
from implementations import all_implementations


# In[2]:


random_array = np.random.rand(7000)
# random_array


# In[3]:


number = 200
result = np.zeros((7,number))
# result


# In[4]:


count = 0
for sort in all_implementations:
    for i in range(0,number):
        st = time.time()
        res = sort(random_array)
        en = time.time()
        result[count][i] = en-st
    count+=1
# result


# In[5]:


result = np.transpose(result)
result = pd.DataFrame(result, columns=['qs1','qs2','qs3','qs4','qs5','merge1','partition_sort'])
# result


# In[6]:


result.to_csv('data.csv', index=False)

