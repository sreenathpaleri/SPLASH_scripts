import os
import pandas as pd
import numpy as np
import pandas as pd
#import seaborn as sns
from matplotlib import pyplot as plt

#%%##### Create a flux dataset to pull in sigma_w. You can collapse this if of no interest.

#%pwd
#source directory inside SPLASH directory
#source = 'Tower_Data/Kettle_Ponds/KPA22_001-365'
file_dir = 'Tower_Data/Kettle_Ponds/KPA22_001-365'
KP10_flux_df = create_df(file_dir)

file_dir = 'Tower_Data/Kettle_Ponds/KPB22_001-365'
KP03_flux_df = create_df(file_dir)

#%%
KP10_flux_df['date'] = pd.to_datetime(KP10_flux_df.date,format='%Y-%m-%d')
KP03_flux_df['date'] = pd.to_datetime(KP03_flux_df.date,format='%Y-%m-%d')

#%%

fig, (ax1, ax2) = plt.subplots(2, 1,  sharex=True, sharey=False, figsize=(10, 10))

def flux_qc_10(flux_df):
    #NAN filter
    H_f1 = flux_df['H_10m']!=-999
    #qc flag
    H_f2 = flux_df['qc_H'] < 1

    LE_f1 = flux_df['LE_10m']!=-999
    #qc flag
    LE_f2 = flux_df['qc_LE'] < 1
    
    return(flux_df.loc[H_f1 & H_f2 & LE_f1 & LE_f2])


def flux_qc_03(flux_df):
    #NAN filter
    H_f1 = flux_df['H_3m']!=-999
    #qc flag
    H_f2 = flux_df['qc_H'] < 1

    LE_f1 = flux_df['LE_3m']!=-999
    #qc flag
    LE_f2 = flux_df['qc_LE'] < 1
    
    return(flux_df.loc[H_f1 & H_f2 & LE_f1 & LE_f2])


flux_qc_10(KP10_flux_df).plot(x='date',y='H_10m',ax=ax1)
flux_qc_10(KP10_flux_df).plot(x='date',y='LE_10m',ax=ax1)

flux_qc_03(KP03_flux_df).plot(x='date',y='H_3m',ax=ax2)
flux_qc_03(KP03_flux_df).plot(x='date',y='LE_3m',ax=ax2)

#%% 

KP10_flux_qc_df = flux_qc_10(KP10_flux_df).copy()

#%% if you just want to calculate Rib, start from here:

#use the 30-min met data to subset for the day and when delta_T (10_m - surf) < 0
file_path = '/home/sreenath/Documents/Work/NOAA/SPLASH/Tower_Data/Kettle_Ponds/met_data_v23052024/'
file_name = 'KP22_001-365.MET30X'
kp_met_df = pd.read_table(file_path + file_name,delimiter=r"\s+")#,skiprows = [1])

#%%

kp_met_df['date_time'] = pd.to_datetime((kp_met_df.date.astype(str) + ' ' + kp_met_df['time(MST)']))
kp_met_df = kp_met_df.set_index('date_time')

#i need a column for delta_T (let's say 10m - surf)
kp_met_df['Tair_10m_mean'] = (kp_met_df['Tair1_10m'] + kp_met_df['Tair2_10m'])/2
kp_met_df['SurfT_C_mean'] = (kp_met_df['SurfT1_C'] + kp_met_df['SurfT2_C'] + + kp_met_df['SurfT3_C'])/3

kp_met_df['delta_T']  =  kp_met_df['Tair_10m_mean'] - kp_met_df['SurfT_C_mean']
