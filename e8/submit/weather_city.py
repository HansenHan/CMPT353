#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


# In[2]:


data_label = pd.read_csv(sys.argv[1])
data_unlabel= pd.read_csv(sys.argv[2])
# data_label = pd.read_csv('monthly-data-labelled.csv')
# data_unlabel = pd.read_csv('monthly-data-unlabelled.csv')


# In[3]:


# data_label


# In[4]:


# data_unlabel


# In[5]:


X = data_label.drop(['city', 'year'], axis=1)
y = data_label['city']


# In[6]:


# X


# In[7]:


# y


# In[8]:


X_train, X_valid, y_train, y_valid = train_test_split(X, y)


# In[9]:


bayes_model = make_pipeline(
        StandardScaler(),
        GaussianNB()
    )
bayes_model.fit(X_train, y_train)
bayes_model.score(X_train, y_train)


# In[10]:


bayes_model.score(X_valid, y_valid)


# In[11]:


knn_model = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors = 10)
    )
knn_model.fit(X_train, y_train)
knn_model.score(X_train, y_train)


# In[12]:


knn_model.score(X_valid, y_valid)


# In[13]:


rf_model = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(n_estimators=100, max_depth=7, min_samples_leaf=10)
    )
rf_model.fit(X_train, y_train)
rf_model.score(X_train, y_train)


# In[14]:


rf_model.score(X_valid, y_valid)


# In[15]:


print(knn_model.score(X_valid, y_valid))


# In[16]:


data_unlabel = data_unlabel.drop(['city', 'year'], axis=1)
result = knn_model.predict(data_unlabel)
# result


# In[17]:


# pd.Series(result).to_csv('labels.csv', index=False, header=False)
pd.Series(result).to_csv(sys.argv[3], index=False, header=False)

