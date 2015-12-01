# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 14:16:49 2015

@author: admin
"""

import pandas as pd
import ..environmentGilga as env
import hdf5Manager as hm
import numpy as np
import signals

def addCalib(row):
    if row['Type']=='1D':    
        return row['Calibration']+';'+row['Processing']
    else:
        return row['Processing']

class SignalWrapper():
      
    def __init__(self):
        self.store = env.DBpath+'store.h5'
        self.tableSignal='Signals'
        self.tableMapping='mapping'
        #self.loadDB()
        self.shotManager=None
        
    def initShotManager(self,sm):
        self.shotManager=sm
    
    def importSignalDB(self)
    	signalTable=pd.read_csv(env.DBpath+'signals.csv',sep=';')
    	signalTable.to_hdf(self.store,self.tableSignal,format='table',data_columns=True)
    	
    def exportSignalDB(self):
    	
    def editSignalDB(self,signalDesc):
    	
    
    def loadDB(self):
        self.signalTable=pd.read_hdf(self.store,self.tableSignal)
        process=self.signalTable.apply(addCalib, axis=1)
        self.signalTable['Processing']=process
        self.mapping=pd.read_hdf(self.store,self.tableMapping)
        
    def initMapping(self):
        liste=hm.getNbrfromFile(hm.listFiles())
        liste2=self.signalTable['Name'].unique()
        mapping=pd.DataFrame({'Shotnbr':liste})
        for x in liste2:
            mapping[x]=pd.Series(np.ones(len(liste)),index=mapping.index)
        mapping.to_hdf(self.store,'mapping',format='table',data_columns=True)
 
	def changemapping(signal, version,shotList): 
		
	def addShotToMapping(shot):
		
	def addSignalToMapping(signal):
		
		
 
    def signalforShot(self,name,shot):
        return self.mapping.loc[self.mapping['Shotnbr']==shot,name].iloc[0]
        
    def getSignalList(self,detail=None):
        if detail==None:
            return self.signalTable.loc[self.signalTable['Type']=='1D',['Name','Description']].drop_duplicates(subset='Name')
        if detail=='all':
            return self.signalTable.loc[self.signalTable['Type']=='1D']
        if detail=='name':
            return self.signalTable.loc[self.signalTable['Type']=='1D',['Name']].drop_duplicates(subset='Name')
 
    def getAttrList(self,detail=None):
        if detail==None:
            return self.signalTable.loc[self.signalTable['Type']=='0D',['Name','Description']].drop_duplicates(subset='Name')
        if detail=='all':
            return self.signalTable.loc[self.signalTable['Type']=='0D']         
        if detail=='name':
            return self.signalTable.loc[self.signalTable['Type']=='0D',['Name']].drop_duplicates(subset='Name')
            
    def getPath(self,signalNames,shot):
        liste=[]        
        for x in signalNames:
            version=self.signalforShot(x,shot)
            liste.append(self.signalTable.loc[(self.signalTable['Name']==x) & (self.signalTable['Version']==version)&(self.signalTable['Type']=='0D')]['Path'])
        return liste

    def getSignalPath(self,signalNames,shot):
        liste=[]      
        for x in signalNames:
            version=self.signalforShot(x,shot)
            liste.append(self.signalTable.loc[(self.signalTable['Name']==x) & (self.signalTable['Version']==version)&(self.signalTable['Type']=='1D')]['Path'])
        return liste

    def getProcessing(self,signalNames,shot):
        liste=[]        
        for x in signalNames:
            version=self.signalforShot(x,shot)
            liste.append(self.signalTable.loc[(self.signalTable['Name']==x) & (self.signalTable['Version']==version)&(self.signalTable['Type']=='1D')]['Processing'])
        return liste

    def wrapSignal(self,shot, signal):
     #   add title and axes legend
        path=self.getSignalPath([signal],shot)[0].values[0]
        if path=="Calculate":
            process=self.getProcessing([signal],shot)[0].values[0].split(";")[-1]
            data=getattr(signals,process)(shot,self.shotManager)
        else:
            data=hm.readData(shot,path)
            process=self.getProcessing([signal],shot)[0].values[0].split(";")
            for x in process:
                if x=="none":
                    pass
                else:
                    data=getattr(signals,x)(data)
        return data
        
    def getCalibration(signal,shot=None):
        pass
    
signalWrapper=SignalWrapper()

def initWrapper():
    signalWrapper.initShotSignalMap()

