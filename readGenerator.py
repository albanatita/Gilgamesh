# -*- coding: utf-8 -*-
"""
Created on Mon May 11 12:12:32 2015

@author: admin
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import datetime,time
import os
import h5py
#import readHdf5
import environmentGilga as envi
import core.hdf5Manager as h5
import gilgamesh as gil

#filename=r'D:\ISHTARmay\data_20150119_20150610.csv'
def convertGenerator(fileN,firstShot,lastShot,env,sm):
    #filename=r'D:\DATA\IShTAR_Process\data_20150119_20150715.csv'
    filename=os.path.normpath(fileN)
    shotstart=firstShot
    shotend=lastShot
    included_cols=[1,2,3,11,12]
    df=pd.read_csv(filename,sep='\t',parse_dates=[0])
    data0=df['Time'].values
#    data1=[]
#    for x in data0:
#        data1.append(datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')))
    #print df.dtypes
    df.loc[df['ForwardPower[W]']!=0,'Run']=1
    #print dataar
    data2=[]
    inittime=data0[0]
    value=0
    for x in data0:
        #res=int(float((x-inittime).item())*1e-9/60)
        res=float((x-inittime).item())*1e-9
        if res>5:        
            value=value+1 
        data2.append(value)
        inittime=x
    df['block2']=data2
    #print df['block']
    #df['block2']=(df.block.shift(1)!=df.block).astype(int).cumsum()
    df.reset_index().groupby(['block2'])['index'].apply(lambda x: np.array(x))
    df=df.drop_duplicates(subset='Time')
    #df=df[df['Run']==1]
    nbr=np.max(df['block2'])
    print nbr
    liste=np.arange(shotstart,shotend)
    listefile=[]
    for x in liste:
        listefile.append(str(x).zfill(5)+'_Data.h5')     
    j=1
    timediff=datetime.timedelta(minutes=1,seconds=0)
    timecorrection=datetime.timedelta(minutes=1,seconds=0)
    #path=r"D:"+os.sep+"DATA"+os.sep+"Acquired_data"
    #path=env.path
    for x in listefile:
        #timei=datetime.datetime.strptime(time.ctime(os.path.getmtime(path+os.sep+x+'.h5')),"%a %b %d %H:%M:%S %Y")
        try:    
            #timea=readHdf5.getAttr(x,'date',env)
            timea=sm.getAttr(h5.getNbrfromFile([x])[0],'Date')
            print x+' - '+str(timea)
            #timei=datetime.datetime.strptime(timea,'%d.%m.%Y %H:%M:%S')
            timei=timea
            #print x
            matched=False
            while not(matched):
                data0=df[df['block2']==j]['Time'].values
                #print data0
                timef=datetime.datetime.utcfromtimestamp((data0[0]- np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's'))
                print timei,(timef+timecorrection),timef
                timef=timef+timecorrection        
                if timei>timef:        
                    deltat=timei-timef
                else:
                    deltat=timef-timei
                print deltat
                if (deltat<=timediff):
                    matched=True
                    timedata=df[df['block2']==j]['Time'].values
                    data=df[df['block2']==j]['ForwardPower[W]'].values
                    data2=df[df['block2']==j]['ReflectedPower[W]'].values
                    #sampling=1/(float((data0[1]-data0[0]).item())*1e-9)
                    timedata=[(float((y-timedata[0]).item()))*1e-9/60 for y in timedata]
                    print x
                    hdf5=h5py.File(envi.H5path+os.sep+x,'a')
                    try:
                        grouph=hdf5.create_group('Generator')
                    except:
                        grouph=hdf5['Generator']
                        if '/Generator/Fpower' in hdf5:
                            hdf5.__delitem__('/Generator/Fpower')
                        if '/Generator/Rpower' in hdf5:                            
                            hdf5.__delitem__('/Generator/Rpower')
                        if '/Generator/Time' in hdf5:                            
                            hdf5.__delitem__('/Generator/Rpower')
                        #hdf5.__delitem__('Generator/sampling')
                    grouph.create_dataset('Fpower',data=data,compression="gzip")
                    grouph.create_dataset('Rpower',data=data2,compression="gzip")
                    grouph.create_dataset('Time',data=timedata,compression="gzip")
                    #grouph.attrs['sampling']=sampling
                    hdf5.close()
                    shot=int(x[0:4])
                    #gil.sm.addShot(shot)
                    j=j+1
                    print 'Generator for '+x
                    
                if (deltat>timediff) and (timei>timef) and (j<nbr):
                    j=j+1
                    print 'Power without discharge'
                if (deltat>timediff) and (timei>timef) and (j>=nbr):    
                    matched=True
                if (deltat>timediff) and (timei<timef):
                    matched=True
                    print 'No generator for '+x
        except Exception,e:
         print e  

