# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 14:14:56 2015

@author: admin
"""
import sys
sys.path.append(r'C:\ISHTAR\\')
import h5py
import os,os.path
import gilgamesh.environmentGilga as env
import pandas as pd
import numpy as np

   
def showFile(shotnbr):
    file=getFilefromNbr([shotnbr])
    hdf5=h5py.File(os.path.join(env.H5path,file[0]),'r')
#channel=tdms_file.object('PXI M6251','Lang_U')
    liste=[]    
    hdf5.visit(liste.append)
    liste2=[x for x in liste if isinstance(hdf5[x],h5py.Dataset)]
    #liste2=[x for x in liste]
    print liste2
    hdf5.close()

def getNbrfromFile(fileList):
    liste=[]
    for x in fileList:
        liste.append(int(x[0:-8]))
    return liste    

def getFilefromNbr(nbrList):
    liste=[]
    for x in nbrList:
        liste.append(str(x).zfill(5)+'_Data.h5')
    return liste   
    
def listFiles(detail=None):
    if detail==None:
        liste=[]
        for file in os.listdir(env.H5path):
            if file.endswith(".h5"):
                liste.append(file)
        return liste

def setAttr(shotnbr,attrpath,value):
    file=getFilefromNbr([shotnbr])
    if os.path.isfile(os.path.join(env.H5path,file[0])):
        hdf5=h5py.File(os.path.join(env.H5path,file[0]),'a')
        attrpath=str(attrpath[0].values[0])
        [groupname,attrname]=attrpath.split('/',-1)
        e = '/'+groupname in hdf5
        if e:
            group=hdf5['/'+groupname]
        else:
            group=hdf5.create_group('/'+groupname)
        group.attrs[attrname]=value
        hdf5.close()
        return 1
    else:
        return 0

def listAttrs(shotnbr,attrpaths):
    file=getFilefromNbr([shotnbr])
    hdf5=h5py.File(os.path.join(env.H5path,file[0]),'r')
    liste=[]
    for x in attrpaths:  
        try:
               x=str(x.values[0])
               [groupname,attrname]=x.split('/',-1)
               group=hdf5['/'+groupname]
        #print x
               attr=group.attrs[attrname] 
        except Exception as e:
               print e
               attr=np.nan
        liste.append(attr)
    return liste
    hdf5.close()

def saveData(shotnbr,item,data,subgroup=None):
    file=getFilefromNbr([shotnbr])
    if os.path.isfile(os.path.join(env.H5path,file[0])):
        hdf5=h5py.File(os.path.join(env.H5path,file[0]),'a')
        e = '/Process'
        if e in hdf5:
            group=hdf5[e]
        else:
            group=hdf5.create_group(e)
        if subgroup is not None:
            try:
                group2=group.create_group(subgroup[:-1])
            except:
                group2=group[subgroup[:-1]]
        if e+'/'+subgroup+item in hdf5:
            hdf5.__delitem__(e+'/'+subgroup+item)
        if subgroup is not None:
            group2.create_dataset(item,data=data)
        else:            
            group.create_dataset(item,data=data)
        hdf5.close()
        return 1
    else:
        return 0    

def readData(shotnbr,item):
    file=getFilefromNbr([shotnbr])
    hdf5=h5py.File(os.path.join(env.H5path,file[0]),'r')
    par=hdf5[item].parent.name
    if par=='/S7':
        data=np.array(hdf5[item])[-100:-1]
        time=np.array(hdf5[par[1:]+'/Time'])[-100:-1]/1000
    elif '/Process' in par:
        data=np.array(hdf5[item])
        time=np.array(hdf5[par[1:]+'/Time'])
        sampling=1/(time[1]-time[0])
            
    else:
        data=np.array(hdf5[item])
        sampling=np.abs(hdf5[item].parent.attrs['sampling'])
        time1=np.linspace(0,len(data)-1,num=len(data))/(sampling)
        offset=0
        if item=='Generator/Fpower' and shotnbr>1600 and shotnbr<1897:
            offset=2.078
            time1=np.array(hdf5['Generator/Time'])*60
        if item=='Generator/Rpower' and shotnbr>1600 and shotnbr<1897:
            offset=2.078    
            time1=np.array(hdf5['Generator/Time'])*60
        time=offset+time1
    hdf5.close()
    return pd.DataFrame(data,index=time)
       
def isData(shotnbr,item):
    file=getFilefromNbr([shotnbr])
    hdf5=h5py.File(os.path.join(env.H5path,file[0]),'r')
    e = item in hdf5
    return e
    
def isAttr(shotnbr,item):
    file=getFilefromNbr([shotnbr])
    hdf5=h5py.File(os.path.join(env.H5path,file[0]),'r')
    [groupname,attrname]=item.split('/',-1)
    try:
        group=hdf5['/'+groupname]
        e = attrname in group.attrs
    except:
        e=False
    return e
    