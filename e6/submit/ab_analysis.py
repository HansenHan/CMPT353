#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import sys
from scipy import stats


# In[2]:


OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)


# In[3]:


searchdata_file = sys.argv[1]
# searchdata_file = 'searches.json'
df = pd.read_json(searchdata_file, orient = 'records', lines = True)
# df


# In[4]:


odd_df = df[df['uid']%2==1]
even_df = df[df['uid']%2==0]
odd_df_search = odd_df[odd_df['search_count']>0].reset_index(drop = True)
odd_df_none = odd_df[odd_df['search_count']==0].reset_index(drop = True)
even_df_search = even_df[even_df['search_count']>0].reset_index(drop = True)
even_df_none = even_df[even_df['search_count']==0].reset_index(drop = True)
odd_df_number = odd_df.shape[0]
even_df_number = even_df.shape[0]
odd_df_search_number = odd_df_search.shape[0]
odd_df_none_number = odd_df_none.shape[0]
even_df_search_number = even_df_search.shape[0]
even_df_none_number = even_df_none.shape[0]

chi_matrix = [[even_df_search_number, even_df_none_number],[odd_df_search_number, odd_df_none_number]]
chi, p1, dof, expected = stats.chi2_contingency(chi_matrix)
# p1
# print(odd_df_number,
# even_df_number)
# print(odd_df_l0_number,
# odd_df_s0_number,
# even_df_l0_number,
# even_df_s0_number)
# print(odd_df_l0_number+
# odd_df_s0_number+
# even_df_l0_number+
# even_df_s0_number)
# print(df.shape[0])


# In[5]:


insdf = df[df['is_instructor'] == True]
odd_insdf = insdf[insdf['uid']%2==1]
even_insdf = insdf[insdf['uid']%2==0]
odd_insdf_search = odd_insdf[odd_insdf['search_count']>0].reset_index(drop = True)
odd_insdf_none = odd_insdf[odd_insdf['search_count']==0].reset_index(drop = True)
even_insdf_search = even_insdf[even_insdf['search_count']>0].reset_index(drop = True)
even_insdf_none = even_insdf[even_insdf['search_count']==0].reset_index(drop = True)
odd_insdf_number = odd_insdf.shape[0]
even_insdf_number = even_insdf.shape[0]
odd_insdf_search_number = odd_insdf_search.shape[0]
odd_insdf_none_number = odd_insdf_none.shape[0]
even_insdf_search_number = even_insdf_search.shape[0]
even_insdf_none_number = even_insdf_none.shape[0]

chi_matrix2 = [[even_insdf_search_number, even_insdf_none_number],[odd_insdf_search_number, odd_insdf_none_number]]
chi2, p2, dof2, expected2 = stats.chi2_contingency(chi_matrix2)
# p2
# print(odd_df_number,
# even_df_number)
# print(odd_df_l0_number,
# odd_df_s0_number,
# even_df_l0_number,
# even_df_s0_number)
# print(odd_df_l0_number+
# odd_df_s0_number+
# even_df_l0_number+
# even_df_s0_number)
# print(df.shape[0])


# In[6]:


p3 = stats.mannwhitneyu(odd_df['search_count'], even_df['search_count']).pvalue
p4 = stats.mannwhitneyu(odd_insdf['search_count'], even_insdf['search_count']).pvalue


# In[7]:


def main():
#     searchdata_file = sys.argv[1]
#     df = pd.read_json(searchdata_file, orient = 'records', lines = True)
    # ...
    
    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=p1,
        more_searches_p=p3,
        more_instr_p=p2,
        more_instr_searches_p=p4,
    ))


if __name__ == '__main__':
    main()


# In[ ]:




