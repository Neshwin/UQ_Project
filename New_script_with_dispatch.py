

import os
import glob
import pandas as pd
from datetime import datetime
import numpy as np

import yaml
import pandas as pd
all_region1_data=pd.DataFrame()
all_region2_data=pd.DataFrame()
def load_controls_from_yaml(yaml_file_path): #Not used
    with open(yaml_file_path, 'rb') as file:
        yaml_data = yaml.safe_load(file)

    controls = yaml_data.get('controls', {})  # Extract the 'controls' section

    return pd.Series(controls)

def compile_specs_regions(yaml_file_path):#Not used
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    region_specs = pd.DataFrame(yaml_data.get('region_specs', []))
    
    return region_specs

def compile_specs_transmission(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    transmission_specs = pd.DataFrame(yaml_data.get('transmission_specs', []))
    
    return transmission_specs

def compile_specs_storage(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    storage_specs = pd.DataFrame(yaml_data.get('storage_specs', []))
    
    return storage_specs

def compile_specs_generation(yaml_file_path):#Not used
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    generation_specs = pd.DataFrame(yaml_data.get('generation_specs', []))
    
    return generation_specs

# def load_csv_data(yaml_file_path):
#     with open(yaml_file_path, 'r', encoding='utf-8') as file:
#         yaml_data = yaml.safe_load(file)

#     csv_file_path = yaml_data.get('csv_file_path', '')  # Get the path to the CSV file

#     if csv_file_path:
#         df = pd.read_csv(csv_file_path, index_col=0)
#         return df
#     else:
#         return None
    
def load_csv_data(yaml_file_path):#not used
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    csv_files = yaml_data.get('csv_files', [])  # Get the list of CSV files

    dfs = {}
    for csv_file in csv_files:
        name = csv_file.get('name', '')
        path = csv_file.get('path', '')

        if name and path:
            df = pd.read_csv(path, index_col=0)
            dfs[name] = df

    return dfs
def load_energy_data(regionList,load_data):
    df = pd.DataFrame()
    for reg in regionList['regionstorType']:
        # print(reg)
        # df = pd.DataFrame()
        df['demand-'  + reg]=load_data['load_data'][reg]
        # print(len(df))
        generation = pd.Series(0, index=load_data['profiles'].index)
        # print(len(generation))
        for carrier in load_data['VRE'].index:
            print(carrier)
            generation+=load_data['profiles'][carrier]*load_data['VRE'][reg][carrier]
        df['vreGen-'  + reg] = generation     
        df['mm-'  + reg] = df['demand-'  + reg] - df['vreGen-'  + reg]
        # print(len(df))
                        
    return df


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
    region2_long = convert_to_long(region2_data,'region2')
    combined_long = pd.concat([region1_long, region2_long], axis=1)
    combined_long = combined_long.resample('H').first()

    return combined_long/1000,region2_long/1000,region1_long/1000

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


# folder_path = r'C:\Users\neshw\Downloads\transfer_3149706_files_9c6f249d (1)\demand_step_change\demand_step_change'
# data = process_region_data(folder_path)
# data = data.resample('H').first()

def calculate_VRE_generation_profiles(csv_file_path):
    df = pd.read_csv(csv_file_path, header=[0, 1])
    solar_cols = df['solar (GW)']
    wind_cols = df['wind (GW)']
    VRE_cols = df['VRE supply (GW)']

    Region1_VRE_generation_profile = solar_cols['region1'] + wind_cols['region1'] + VRE_cols['region1']
    Region2_VRE_generation_profile = solar_cols['region2'] + wind_cols['region2'] + VRE_cols['region2']

    result_df = pd.DataFrame({
        'Date & Time': df['Date & Time']['Date & Time'],
        'region1': Region1_VRE_generation_profile,
        'region2': Region2_VRE_generation_profile
    })
    result_df['Date & Time'] = pd.to_datetime(result_df['Date & Time'], format='%d-%m-%Y %H:%M')

    result_df.set_index('Date & Time', inplace=True)
    result_df.index = result_df.index.map(lambda x: x.replace(year=2050))
    
    # # Update the year to 2050 for the entire index
    # result_df.index = result_df.index.map(lambda x: x.replace(year=2050))

    return result_df*0.25


folder_path = r'C:\Users\neshw\Downloads\transfer_3149706_files_9c6f249d (1)\demand_step_change\demand_step_change'
data,region2_long,region1_data = process_region_data(folder_path)

csv_file_path = r'C:\Users\neshw\Downloads\transfer_3149706_files_9c6f249d (1)\VRE_supply_2reg.csv'
VRE_generation = calculate_VRE_generation_profiles(csv_file_path)


def load_energy_data(regionList,load,vre_generation):
    df = pd.DataFrame()
    for reg in regionList:
        
        df['demand-'  + reg]=load[reg]
        df['vreGen-'  + reg]=vre_generation[reg]
        df['mm-'  + reg] = df['demand-'  + reg] - df['vreGen-'  + reg] 

        
    return df        

                        

regionList=['region1', 'region2']
mismatch = load_energy_data(regionList,data,VRE_generation)
all_region1_data['demand']=mismatch['demand-region1']
all_region1_data['vreGen-region1']=mismatch['vreGen-region1']
all_region2_data['demand']=mismatch['demand-region2']
all_region2_data['vreGen-region1']=mismatch['vreGen-region2']


splits = pd.DataFrame()
for reg in regionList:
    
    splits['surplus-'   + reg] = mismatch['mm-' + reg].clip(upper=0).abs()
    splits['shortfall-' + reg] = mismatch['mm-' + reg].clip(lower=0)
    
    # if ctrl.compileEnergyBalance
    balance = mismatch


def compile_specs_storage(yaml_file_path, storage_type=None):
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    storage_specs = pd.DataFrame(yaml_data.get('storage_specs', []))

    if storage_type:
        # Filter the DataFrame based on the specified 'type'
        storage_specs = storage_specs[storage_specs['type'] == storage_type]

    return storage_specs




yaml_file_path = 'config.yaml'
storType = 'sds'
specs = compile_specs_storage(yaml_file_path,storType) #These are only the characteristics of a general battery technology
# print(storagespecs)
# int(storagespecs.maxChargeRate[0])

def set_initial_state(df,initLvl, dataLength,indx):
    # df = pd.DataFrame()
    
    # Initialize 'lvl' column with 'initLvl' for the first row and zeros for the rest
    df['lvl_begin_'+reg] = [initLvl] + [0] * (dataLength-1)
    df['lvl_end_'+reg] = [0] + [0] * (dataLength-1)    
    # Initialize 'in' and 'out' columns with zeros for all rows
    df['in_'+reg] = np.zeros(dataLength)
    df['out_'+reg] = np.zeros(dataLength)
    df.index=indx
    
    return df
def storage_naive(stor_df,demandSeries, surplusSeries, specs, dataLength,reg):
    import time
    BESS_cap=pd.read_csv("BESS_CAP.csv",index_col=0)
    
    # initialise local variables
    initialChargeLvl = BESS_cap.loc[reg]['Battery_capacity_GW']*specs['initialCharge%'][0]/100 * int(specs.maxChargeLvl[0])/100

    stor = set_initial_state(stor_df,initialChargeLvl, dataLength,surplusSeries.index)
    
    check=1
    # time-sequential charge/discharge balance
    for ts in surplusSeries.index:
        # print(ts)
        # initialise loop variables
        charge = 0; discharge = 0
        if check==0:

            stor.at[ts,'lvl_begin_'+reg]=stor.loc[prev_ts]['lvl_end_'+reg]
            # print("end",stor.loc[prev_ts]['lvl_end'],stor.loc[ts]['lvl_begin'])

        priorChargeLvl = stor.loc[ts]['lvl_begin_'+reg]
        # time.sleep(3)
        # print("charge begining",stor.loc[ts]['lvl_begin'])

            
        surplus=surplusSeries[reg].loc[ts]
        shortfall=demandSeries[reg].loc[ts]
        # charge during hours of supply surplus
        if surplus > 0:
            
            if priorChargeLvl < int(specs.maxChargeLvl[0])*BESS_cap.loc[reg]['Battery_capacity_GW']/100:
                charge = min( int(specs['maxChargeLvl'][0])*BESS_cap.loc[reg]['Battery_capacity_GW']/100- priorChargeLvl, 
                              (BESS_cap.loc[reg]['Battery_capacity_GW']*int(specs.maxChargeRate[0]))/100,surplus)
            
                stor.loc[ts,'in_'+reg]  = charge
                surplusSeries.at[ts,reg] -= charge #/ (specs.rte/100)
                                
        # discharge during hours of supply shortfall
        
        elif shortfall > 0: 

            if priorChargeLvl > int(specs.minChargeLvl[0])*BESS_cap.loc[reg]['Battery_capacity_GW']/100:
                discharge = min( priorChargeLvl - int(specs.minChargeLvl[0])*BESS_cap.loc[reg]['Battery_capacity_GW']/100, 
                                 BESS_cap.loc[reg]['Battery_capacity_GW']*int(specs.maxDischRate[0])/100, shortfall )
                # print("ssss",discharge)
                stor.loc[ts,'out_'+reg] = discharge
                demandSeries.at[ts,reg]  -= discharge

                # discharge = min( priorChargeLvl - int(specs.minChargeLvl[0])*BESS_cap.loc[reg]['Battery_capacity_GW']/100, 
                #                  BESS_cap.loc[reg]['Battery_capacity_GW']*int(specs.maxDischRate[0])/100, shortfall )
 

                
        # update the charge level timeseries
        stor.at[ts,'lvl_end_'+reg] = priorChargeLvl + charge - discharge
        prev_ts=ts
        check=0
        # print("charge end",stor.loc[ts]['lvl_end'])
        
    return (demandSeries, surplusSeries, stor) 




demandSeries=pd.DataFrame()
surplusSeries=pd.DataFrame()
stor_df = pd.DataFrame()
for reg in regionList:
    print(reg)
    # get mismatch splits
    demandSeries[reg]  = splits['shortfall-' + reg]
    surplusSeries[reg] = splits['surplus-'   + reg]
    dataLength=len(demandSeries)
    # implement storage charge/discharge cycles
    demandSeries,surplusSeries, sb = storage_naive(stor_df,demandSeries, surplusSeries, 
                                                    specs, dataLength,reg)
    
    # update & store results
    splits['shortfall-' + reg] = demandSeries[reg]    
    splits['surplus-'   + reg] = surplusSeries[reg]
    
    # # if ctrl.compileEnergyBalance
    # balance[storType + '-' + reg] += sb['in'] - sb['out']
        
    # if ctrl.compileStorageBalance
    #     storage[storType + '-charge-' + reg] = sb['in']
    #     storage[storType + '-disch-'  + reg] = sb['out']
    #     storage[storType + '-level-'  + reg] = sb['lvl']

all_region1_data['BESS_Dispatch_in']=-sb['in_region1']
all_region1_data['BESS_Dispatch_out']=sb['out_region1']
all_region2_data['BESS_Dispatch_in']=-sb['in_region2']
all_region2_data['BESS_Dispatch_out']=sb['out_region2']

# splits2=splits
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:30:49 2023

@author: neshw
"""

def calculate_transfers(region_list, splits, yaml_file_path):
    transfers = pd.DataFrame()
    trans_specs = compile_specs_transmission(yaml_file_path)

    for i in range(len(region_list)):
        for j in range(i + 1, len(region_list)):
            regA = region_list[i]
            regB = region_list[j]

            surplusA = splits['surplus-' + regA]
            surplusB = splits['surplus-' + regB]
            shortfallA = splits['shortfall-' + regA]
            shortfallB = splits['shortfall-' + regB]

            capAtoB = trans_specs.cap[0]
            capBtoA = trans_specs.cap[0]

            capBtoA_series = pd.Series(data=100, index=surplusA.index)

            transferAtoB = pd.DataFrame({'surplusA': surplusA, 'shortfallB': shortfallB, 'capBtoA_series': capBtoA_series}).min(axis=1)
            transferAtoB = pd.Series(transferAtoB.values, index=surplusA.index)

            transferBtoA = pd.DataFrame({'surplusB': surplusB, 'shortfallA': shortfallA, 'capBtoA_series': capBtoA_series}).min(axis=1)
            transferBtoA = pd.Series(transferBtoA.values, index=surplusA.index)

            splits['surplus-' + regA] -= transferAtoB
            splits['shortfall-' + regB] -= transferAtoB

            splits['surplus-' + regB] -= transferBtoA
            splits['shortfall-' + regA] -= transferBtoA

            transfers[f'{regA}-{regB}'] = transferAtoB
            transfers[f'{regB}-{regA}'] = transferBtoA

    return splits, transfers

splits, transfers = calculate_transfers(regionList, splits, yaml_file_path)

all_region1_data['region1-region2']=-transfers['region1-region2']
all_region2_data['region1-region2']=transfers['region1-region2']
all_region1_data['region2-region1']=transfers['region2-region1']
all_region2_data['region2-region1']=-transfers['region2-region1']
# splits2['surplus-region1_n']=splits['surplus-region1']
# splits2['shortfall-region1_n']=splits['shortfall-region1']
# splits2['surplus-region2_n']=splits['surplus-region2']
# splits2['shortfall-region2_n']=splits['shortfall-region2']

# splits2['region1-region2']=transfers['region1-region2']
# splits2['region2-region1']=transfers['region2-region1']
# splits2['surplus-region1_n']=splits['surplus-region1']

gen_list=pd.read_csv("gen_list.csv",index_col=0)
gen_dispatch_df=pd.DataFrame(0,columns=gen_list.index,index=demandSeries.index)
hydro_inflow=pd.read_csv("hydro_inflow.csv",index_col=0)
hydro_inflow1=pd.read_csv("hydro_inflow.csv",index_col=0)
reg_gen_dispatch=pd.DataFrame(index=splits.index,columns=regionList)

for reg in regionList:
    # get mismatch splits
    reg_gen_list=gen_list[gen_list.region==reg]
    reg_gen_list = reg_gen_list.sort_values(by='dispatch_order')
    ds = splits['shortfall-' + reg]
    for idx in ds.index:
        demand=ds.at[idx]
        for gen in reg_gen_list.index:
            if demand>0.06:                

                    
                if idx.hour==0 and gen_list.at[gen,"generation_limit"]:
                    gen_limit_hydro=hydro_inflow.at[reg, str(idx.month)] / idx.days_in_month

                if gen_list.at[gen,"generation_limit"]:
                    # hydro_inflow=pd.read_csv("hydro_inflow.csv",index_col=0)
                    gen_limit=gen_limit_hydro
                else:
                    gen_limit=1000000000

                
                if idx==ds.index[0]:                
                    cap_lst=reg_gen_list.at[gen,'Capacity (GW)']
                    cap_avail=cap_lst
                    prev_gen=reg_gen_list.at[gen,'Capacity (GW)'] #remeber to add this
                    cap_avail=min(cap_lst,gen_limit)
                else:
                    cap_lst=reg_gen_list.at[gen,'Capacity (GW)']
                    rmp_rate=gen_list.at[gen,"ramp_rate"]/100
                    prev_gen=gen_dispatch_df.at[prev_ts,gen]
                    cap_avail=min(cap_lst,prev_gen+cap_lst*rmp_rate,gen_limit)
                
                # cap_avail=min(cap_lst,prev_gen*rmp_rate,gen_limit)
                    
                gen_dispatch=min(demand,cap_avail)
                demand-=gen_dispatch
                if gen_list.at[gen,"generation_limit"]:
                    # hydro_inflow=pd.read_csv("hydro_inflow.csv",index_col=0)
                    # hydro_inflow.at[reg,str(idx.month)]-=gen_dispatch #make sure its hourly reolution
                    gen_limit_hydro-=gen_dispatch
                gen_dispatch_df.at[idx,gen]=gen_dispatch
                prev_ts=idx
    
    splits['shortfall-' + reg]-=gen_dispatch_df[list(reg_gen_list.index)].sum(axis=1) 
    reg_gen_dispatch[reg]=gen_dispatch_df[list(reg_gen_list.index)].sum(axis=1)  
    if reg=='region1':
        all_region1_data[list(reg_gen_list.index)]=gen_dispatch_df[list(reg_gen_list.index)]
    if reg=='region2':
        all_region2_data[list(reg_gen_list.index)]=gen_dispatch_df[list(reg_gen_list.index)]
          
#Question!: What do you do with the surplus series. Its quiet large even after storage and transfer
#Question2  Some zero values showing up after the storage and trasfer dispatch                
#Most of the surplus after dispacth is due to under capacity or inadequate water in the reservoir 

#Question!: What do you do with the surplus series. Its quiet large even after storage and transfer
all_region1_data.to_csv("all_region1_data.csv")
all_region2_data.to_csv("all_region2_data.csv")