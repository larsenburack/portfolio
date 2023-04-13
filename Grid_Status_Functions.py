#!/usr/bin/env python
# coding: utf-8

# In[83]:


import ipynb


# In[71]:


import gridstatusio as gs
import gridstatus as g
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime


# In[87]:


def hourly_data(df):
    df["Hour"] = df["Time"].dt.hour
    cols_dict = {}
        
    for c in range(len(df.dtypes)):
        if df.dtypes[c] in ['int64','float64']:
            cols_dict[df.columns[c]] = 'mean'
    
    df2 = df.groupby(['Hour'], as_index=False).agg(cols_dict)
    return df2


# In[5]:


def hourly_daily_data(df):
    fuel_mix_hourly = df.set_index("Time").resample("H").mean().reset_index()
    return fuel_mix_hourly

# def hourly_data_by_day(df):
#     #fuel_mix_hourly = df.set_index("Time").resample("H").mean().reset_index could be more effective
#     df["Hour"] = df["Time"].dt.hour
#     df["Date"] = df["Time"].dt.date
#     cols_dict = {}
        
#     for c in range(len(df.dtypes)):
#         if df.dtypes[c] != 'object':
#             cols_dict[df.columns[c]] = 'mean'
    
#     df2 = df.groupby(['Date','Hour'], as_index=False).agg(cols_dict) 
#     df2["Date"] = pd.to_datetime(df2["Date"])
#     return df2


# In[ ]:


def line_single(df, num_params): 
    
    #if we enter the whole name of the df and its colname this should work with multiple dfs, actually it won't
    
    #x axis column
    x_axis = input('Enter x-axis colname: ')
    while x_axis not in df.columns:
        print('***Invalid colname***')
        x_axis = input('Enter x-axis colname: ')
    
    #enter columns to plot
    params = []
    for i in range(num_params):
        col = input('Enter y-axis colname: ')      
        while col not in df.columns:
            print('***Invalid colname***')
            col = input('Enter colname: ')
        params.append(col)
             
    #set up figure
    fig, ax = plt.subplots(figsize=(10,6))
    ax.set_title(input('Enter title: '))
    ax.set_ylabel(input('Enter y-axis label: '))
    ax.set_xlabel(input('Enter x-axis label: '))
    colors = list(mcolors.TABLEAU_COLORS.keys())
        
    labs = []
    lns_list = []
    count = 0
    for p in params: #set a parameter for xticks for date ranges +- longer than a day
        #if len(df[x_axis]) > 24:
        lns_var = ax.plot(df[x_axis] ,df[p], label = p, color=colors[count])
        lns_list.append(lns_var)
        labs.append(p)
        count += 1

    #set up legend
    lns = []
    for l in lns_list:
        for m in l:
            lns.append(m)
            
    legend_loc = input('Legend in or out of plot? ')
    if legend_loc == 'in':
        loc = int(input('Enter legend location: '))
        ax.legend(lns, labs, loc=loc)  #loc=loc, #put the legend to the right side every time
    elif legend_loc == 'out':
        plt.legend(bbox_to_anchor=(1.05, .5), loc='center left')
        plt.tight_layout()
        
    plt.show()
    
#Add annotation feature


# In[ ]:


def line_dual(df, num_params): #num dfs
    
    #if we enter the whole name of the df and its colname this should work with multiple dfs, actually it won't
    
    #x axis column
    x_axis = input('Enter x-axis colname: ')
    while x_axis not in df.columns:
        print('***Invalid colname***')
        x_axis = input('Enter x-axis colname: ')
    
    #enter columns to plot
    params = {}
    for i in range(num_params):
        col = input('Enter y-axis colname: ')      
        while col not in df.columns:
            print('***Invalid colname***')
            col = input('Enter y-axis colname: ')
        axis = input('Which axis? (left or right): ')
        while axis not in ['left','right']:
            print('***Invalid axis***')
            axis = input('Which axis? (left or right): ')
        params[col] = axis
    
    #print(params)
    
    #set up figure
    fig, ax = plt.subplots(figsize=(10,6))
    ax.set_title(input('Enter title: '))
    ax.set_ylabel(input('Enter left y-axis label: '))
    ax.set_xlabel(input('Enter x-axis label: '))
    colors = list(mcolors.TABLEAU_COLORS.keys())
    
    #for dual axis
    ax2 = ax.twinx()
    ax2.set_ylabel(input('Enter right y-axis label: '))
        
    lns_list = []
    count = 0
    for p,a in params.items():
        if a == 'left':
            ax.plot(df[x_axis] ,df[p], label = p)
            lns_list.append(ax.plot(df[x_axis] ,df[p], label = p, color = colors[count]))
        else:
            ax2.plot(df[x_axis] ,df[p], label = p)
            lns_list.append(ax2.plot(df[x_axis] ,df[p], label = p, color = colors[count]))
        count += 1

    #set up legend
    lns = []
    for l in lns_list:
        for m in l:
            lns.append(m)
    labs = [l.get_label() for l in lns]
    
    legend_loc = input('Legend in or out of plot? ')
    if legend_loc == 'in':
        loc = int(input('Enter legend location: '))
        ax.legend(lns, labs, loc=loc)  #loc=loc, #put the legend to the right side every time
    elif legend_loc == 'out':
        plt.legend(bbox_to_anchor=(1.05, .5), loc='center left')
        plt.tight_layout()
        
    plt.show()


# In[91]:


def basics(df):
    if 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time'])
    print(df.info(), '\n\n', df.describe(), '\n\n', df.isna().sum(), '\n\n')
    return df.head()


# In[ ]:


# def multi_df(*args):
    
#     #set up figure
#     fig, ax = plt.subplots(figsize=(10,6))
#     ax.set_title(input('Enter title: '))
#     ax.set_ylabel(input('Enter y-axis label: '))
#     ax.set_xlabel(input('Enter x-axis label: '))
#     colors = list(mcolors.TABLEAU_COLORS.keys())
    
#     for c in args:
#         c.columns


# In[ ]:


#def binned(df,bins,labels): #binning function


# In[ ]:


#def bar_hour(df):


# In[46]:


# caiso = g.CAISO()
# mix_df = caiso.get_fuel_mix("2023-03-16")
# load_df = caiso.get_load("2023-03-16")
# as_df = caiso.get_as_prices("2023-03-16")
# full_df = hourly_mix_load_as(mix_df,load_df,as_df)


# In[33]:


# mix_df2023 = caiso.get_fuel_mix(start='2023-01-01',end='today')

