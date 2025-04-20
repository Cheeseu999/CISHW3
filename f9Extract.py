# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 20:46:42 2025

@author: avana
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# get wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters"

try:
    page = requests.get(url)
except Exception as e:
    print('Error downloading page: ', e)
    
    
# create html soup of the page and grab all table sections
soup = BeautifulSoup(page.text)
tables = soup.find_all('table')

# create pandas data frame for each table
dfs = []
for table in tables:
    dfs.append(pd.read_html(str(table))[0])
    
    
# Clean up table 1
B1 = dfs[0].copy(deep = True)

# clean up table to follow hw format
B1 = B1.rename(columns={'S/N[a]': 'engine_number', 'Flight No.[b]': 'flight_number', 'Launch date (UTC)[6]' : 'launch_date',
                   'Launch (pad)' : 'launch_pad', 'Landing' : 'landing_location', 'Fate' : 'engine_status', 'Version' : 'block_type'})

# drop uneeded columns and rows
B1.drop(columns=['Payload[c]'], inplace = True)
B1.drop([25], inplace = True)

# create flight type and turnaround time columns and add to table
flight_type = []
for i in range(len(B1)): 
    flight_type.append(B1.iloc[i].flight_number[:2])
B1.insert(4, 'flight_type', flight_type)
B1.insert(7, 'turnaround_time', 0)
B1.insert(9, 'total_launches', 1)

# convert version to block type and remove brackets for engine_status
for i in range(len(B1)): 
    B1.loc[i, 'block_type'] = B1.iloc[i].block_type[1:4]

    # check if engine_status has brackets and remove if they do
    if(B1.iloc[i].engine_status[-1] == ']'):
        size = len(B1.iloc[i].engine_status) - 4
        B1.loc[i, 'engine_status'] = B1.iloc[i].engine_status[:size]


# convert dates to proper format
for i in range(len(B1)):
    try:
        B1.loc[i, 'launch_date'] = datetime.strptime(B1.loc[i, 'launch_date'], "%d %B %Y").strftime("%Y-%m-%d")
    except:
        B1.loc[i, 'launch_date'] = 'N/A'
        
        
        
# clean up table 2
B4 = dfs[1].copy()

# clean up table names to follow hw format
B4 = B4.rename(columns={'S/N': 'engine_number', 'Flight No.[a]': 'flight_number', 'Launch date (UTC)[6]' : 'launch_date', 
                   'Launch (pad)' : 'launch_pad', 'Landing (location)' : 'landing_location', 'Fate' : 'engine_status', 'Version' : 'block_type',
                    'Turnaround' : 'turnaround_time'})

# drop uneeded columns and rows
B4.drop(columns=['Payload[b]'], inplace = True)
B4.drop([41], inplace = True)

# create flight type and add to table
flight_type = []
for i in range(len(B4)): 
    flight_type.append(B4.iloc[i].flight_number[:2])
B4.insert(4, 'flight_type', flight_type)

# calculate count of launches per engine and put into new column
B4['total_launches'] = B4.groupby('engine_number')['engine_number'].transform('count')

# convert version to block type and remove brackets for engine_status
for i in range(len(B4)): 
    B4.loc[i, 'block_type'] = '4'

    # check if engine_status has brackets and remove if they do
    if(B4.iloc[i].engine_status[0] == 'R'):
        B4.loc[i, 'engine_status'] = 'Retired'
    elif(B4.iloc[i].engine_status[0] == 'D'):
        B4.loc[i, 'engine_status'] = 'Destroyed'
    elif(B4.iloc[i].engine_status[0] == 'E'):
        B4.loc[i, 'engine_status'] = 'Expended'

# convert dates to proper format
for i in range(len(B4)):
    if(B4.iloc[i].launch_date[-1] == ']'):
        size = len(B4.iloc[i].launch_date) - 4
        B4.loc[i, 'launch_date'] = B4.iloc[i].launch_date[:size]
    
    try:
        B4.loc[i, 'launch_date'] = datetime.strptime(B4.loc[i, 'launch_date'], "%d %B %Y").strftime("%Y-%m-%d")
    except:
        B4.loc[i, 'launch_date'] = B4.loc[i, 'launch_date']
        
        
# clean up table 3
B5 = dfs[2].copy()

# clean up table names to follow hw format
B5 = B5.rename(columns={'S/N': 'engine_number', 'Flight No.[a]': 'flight_number', 'Launch date (UTC)[6]' : 'launch_date', 
                   'Launch (pad)' : 'launch_pad', 'Landing (location)' : 'landing_location', 'Fate' : 'engine_status', 'Version' : 'block_type',
                    'Turnaround time' : 'turnaround_time', 'Type' : 'block_type', 'Launches' : 'total_launches'})

# drop uneeded columns and rows
B5.drop(columns=['Payload[b]'], inplace = True)
B5.drop([193], inplace = True)

# create flight type and add to table
flight_type = []
for i in range(len(B5)): 
    flight_type.append(B5.iloc[i].flight_number[:2])
B5.insert(5, 'flight_type', flight_type)

# fix block type 
for i in range(len(B5)): 
    B5.loc[i, 'block_type'] = '5'

    if(B5.iloc[i].engine_status[0] == 'R'):
        B5.loc[i, 'engine_status'] = 'Retired'
    elif(B5.iloc[i].engine_status[0] == 'D' or B5.iloc[i].engine_status[0] == 'I'):
        B5.loc[i, 'engine_status'] = 'Destroyed'
    elif(B5.iloc[i].engine_status[0] == 'E'):
        B5.loc[i, 'engine_status'] = 'Expended'


# convert dates to proper format
for i in range(len(B5)):
    if(B5.iloc[i].launch_date[-1] == ']'):
        size = len(B5.iloc[i].launch_date) - 5
        B5.loc[i, 'launch_date'] = B5.iloc[i].launch_date[:size]
        
    try:
        B5.loc[i, 'launch_date'] = datetime.strptime(B5.loc[i, 'launch_date'], "%d %B %Y").strftime("%Y-%m-%d")
    except:
        B5.loc[i, 'launch_date'] = B5.loc[i, 'launch_date']
        
        
# clean up table 4
B5_2 = dfs[3].copy()

# clean up table names to follow hw format
B5_2 = B5_2.rename(columns={'S/N': 'engine_number', 'Flight No.[a]': 'flight_number', 'Launch date (UTC)[6]' : 'launch_date', 
                   'Launch (pad)' : 'launch_pad', 'Landing (location)' : 'landing_location', 'Status' : 'engine_status', 'Version' : 'block_type',
                    'Turnaround time' : 'turnaround_time', 'Type' : 'block_type', 'Launches' : 'total_launches'})

# drop uneeded columns and rows
B5_2.drop(columns=['Payload[b]'], inplace = True)
B5_2.drop([244], inplace = True)

# create flight type and add to table
flight_type = []
for i in range(len(B5_2)): 
    flight_type.append(B5_2.iloc[i].flight_number[:2])
B5_2.insert(5, 'flight_type', flight_type)

# fix block type 
for i in range(len(B5_2)): 
    B5_2.loc[i, 'block_type'] = '5'

# convert dates to proper format
for i in range(len(B5_2)):
    if(B5_2.iloc[i].launch_date[-1] == ']'):
        size = len(B5_2.iloc[i].launch_date) - 5
        B5_2.loc[i, 'launch_date'] = B5_2.iloc[i].launch_date[:size]
        
    try:
        B5_2.loc[i, 'launch_date'] = datetime.strptime(B5_2.loc[i, 'launch_date'], "%d %B %Y").strftime("%Y-%m-%d")
    except:
        B5_2.loc[i, 'launch_date'] = B5_2.loc[i, 'launch_date']
        
        

# Move columns of tables so they align
move = B1.pop('launch_date')
B1.insert(4, 'launch_date', move) 

move = B4.pop('launch_date')
B4.insert(4, 'launch_date', move) 
move = B4.pop('turnaround_time')
B4.insert(7, 'turnaround_time', move) 

move = B5.pop('launch_date')
B5.insert(4, 'launch_date', move) 
move = B5.pop('total_launches')
B5.insert(9, 'total_launches', move) 
move = B5.pop('turnaround_time')
B5.insert(7, 'turnaround_time', move) 

move = B5_2.pop('launch_date')
B5_2.insert(4, 'launch_date', move) 
move = B5_2.pop('total_launches')
B5_2.insert(9, 'total_launches', move) 
move = B5_2.pop('turnaround_time')
B5_2.insert(7, 'turnaround_time', move) 


# combine all three data frames
df = pd.concat([B1, B4, B5, B5_2], ignore_index=True)

# clean all '-' entries
df = df.replace('—', 'N/A')
df = df.replace('‑', '‑')

# convert to csv
df.to_csv('Blocks.csv', index=False, sep=',')