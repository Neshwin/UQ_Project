# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 20:46:21 2023

@author: neshw
"""

import glob
import os
import pandas as pd

def load_energy_data(regionList, load_data):
    df = pd.DataFrame()
    for reg in regionList['regionstorType']:
        print(reg)
        df['demand-' + reg] = load_data['load_data'][reg]
        print(len(df))
        generation = pd.Series(0, index=load_data['profiles'].index)
        print(len(generation))
        for carrier in load_data['VRE'].index:
            print(carrier)
            generation += load_data['profiles'][carrier] * load_data['VRE'][reg][carrier]
        df['vreGen-' + reg] = generation
        df['mm-' + reg] = df['demand-' + reg] - df['vreGen-' + reg]

regionList = ...  # You need to define regionList and load_data

load_energy_data(regionList, load_data)

import os
import glob
import pandas as pd
from datetime import datetime

def process_region_data(folder_path):
    csv_files = glob.glob(f"{folder_path}/*.csv")
    region1_data = None
    region2_data = None

    for csv_file in csv_files:
        region_name = os.path.basename(csv_file).split('_')[0]
        file = pd.read_csv(csv_file)
        
        if region_name in ['CNQ', 'GG', 'SQ']:
            if region1_data is None:
                region1_data = file[['Year', 'Month', 'Day']]
            region1_data = region1_data.add(file.iloc[:, 3:], fill_value=0)
        else:
            if region2_data is None:
                region2_data = file[['Year', 'Month', 'Day']]
            region2_data = region2_data.add(file.iloc[:, 3:], fill_value=0)

    region1_data = region1_data[region1_data.Year == 2050]
    region2_data = region2_data[region2_data.Year == 2050]

    region1_data.to_csv('region1_data.csv', index=False)
    region2_data.to_csv('region2_data.csv', index=False)

    region1_long = convert_to_long(region1_data,'region1')
    region2_long = convert_to_long(region2_data,'region1')
    combined_long = pd.concat([region1_long, region2_long], axis=1)

    return combined_long

def convert_to_long(df,region):
    new_df = pd.DataFrame()
    for idx in df.index:
        year = int(df.loc[idx].Year)
        month = int(df.loc[idx].Month)        
        day = int(df.loc[idx].Day)  
        
        for ix in df.loc[idx].index[:-3]:
            hour = int((int(ix) - 1) / 2)
            minute = int((((int(ix) - 1) / 2) - hour) * 60)
            
            timestamp = datetime(year, month, day, hour, minute)
            new_df.at[timestamp, region] = df.loc[idx][ix]
           
    return new_df


folder_path = r'C:\Users\neshw\Downloads\transfer_3149706_files_9c6f249d (1)\demand_step_change\demand_step_change'
data = process_region_data(folder_path)
data = data.resample('H').first()

def calculate_VRE_generation_profiles(csv_file_path):
    df = pd.read_csv(csv_file_path, header=[0, 1])
    solar_cols = df['solar (GW)']
    wind_cols = df['wind (GW)']
    VRE_cols = df['VRE supply (GW)']

    Region1_VRE_generation_profile = solar_cols['region1'] + wind_cols['region1'] + VRE_cols['region1']
    Region2_VRE_generation_profile = solar_cols['region2'] + wind_cols['region2'] + VRE_cols['region2']

    result_df = pd.DataFrame({
        'Date & Time': df['Date & Time']['Date & Time'],
        'Region1': Region1_VRE_generation_profile,
        'Region2': Region2_VRE_generation_profile
    })

    return result_df

csv_file_path = r'C:\Users\neshw\Downloads\transfer_3149706_files_9c6f249d (1)\VRE_supply_2reg.csv'
VRE_generation = calculate_VRE_generation_profiles(csv_file_path)
VRE_generation['Date & Time'] = pd.to_datetime(VRE_generation['Date & Time'], format='%d-%m-%Y %H:%M')

if VRE_generation.index.equals(data.index):
    print("The indices are identical.")

# import pandas as pd

# # Assuming df1 and df2 are your DataFrames
# # Check if the indices are identical
# if VRE_generation.index.equals(data.index):
#     # Combine DataFrames along columns (axis=1) since the indices are identical
#     combined_df = pd.concat([VRE_generation, data], axis=1)
#     print("The indices are identical. Combined DataFrame created.")
#     print(combined_df)
# else:
#     print("The indices are not identical.")


# Set 'Date & Time' as the index
VRE_generation.set_index('Date & Time', inplace=True)

# Update the year to 2050 for the entire index
VRE_generation.index = VRE_generation.index.map(lambda x: x.replace(year=2050))

# Example of the resulting DataFrame



