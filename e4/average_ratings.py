#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import sys
import difflib


# In[2]:


file1 = sys.argv[1]
file2 = sys.argv[2]
result = sys.argv[3]
# file1 = 'movie_list.txt'
# file2 = 'movie_ratings.csv'
# result = 'output.csv'


# In[3]:


def to_new_line(data):
    return data.rstrip()
func_newline = np.vectorize(to_new_line)


# In[4]:


name_list = pd.DataFrame(open(file1).readlines(), columns=['name']).apply(func_newline)


# In[5]:


rate_list = pd.read_csv(file2)


# In[6]:


def match(data):
    new_data = difflib.get_close_matches(data, name_list['name'])
    if len(new_data) != 0:
        return new_data[0]
    else:
        return None
func_match = np.vectorize(match)


# In[7]:


rate_list['title'] = rate_list['title'].apply(func_match)


# In[8]:


rate_list = rate_list.dropna()


# In[9]:


rate_list = rate_list.groupby('title').mean().round(2)


# In[10]:


# rate_list
rate_list.to_csv(result)


# In[ ]:




