# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 15:32:49 2015

@author: admin
"""

import pandas as pd
import numpy as np
import os
import datetime,time


#filename=r'D:\DATA\IShTAR_Process\data_20150119_20150715.csv'
filename=r'C:\Users\Public'+os.sep+'data_20150119_20151023.csv'

included_cols=[1,2,3,11,12]

df=pd.read_csv(filename,sep='\t',parse_dates=[0])
data0=df['Time'].values
data1=[]
for x in data0:
    data1.append(datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')))
#print df.dtypes
df.loc[df['ForwardPower[W]']!=0,'Run']=1
#print dataar
data2=[]
for x in data0:
    data2.append(int(float((x-data0[0]).item())*1e-9/60))
df['block']=data2
#print df['block']
df['block2']=(df.block.shift(1)!=df.block).astype(int).cumsum()
df.reset_index().groupby(['block2'])['index'].apply(lambda x: np.array(x))
#df=df[df['Run']==1]
nbr=np.max(df['block2'])
print nbr


