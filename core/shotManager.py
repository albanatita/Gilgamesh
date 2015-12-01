# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 18:36:46 2015

@author: rdi
"""

import pandas as pd
import environmentGilga as env
import hdf5Manager as h5
import wrapper

class ShotManager():

    def __init__(self,wrap):
        self.wrapper=wrap
        self.wrapper.initSM(self)
        self.store=env.DBpath+'store.h5'
        #self.shotDB=self.store.select('shotDB')
    
    def listShots(self,criterion=None,attrList=None):
        
        if criterion==None:
            liste=pd.read_hdf(self.store,'shotDB')
        else:
            try:
                liste=pd.read_hdf(self.store,'shotDB',where=[criterion])
            except:
                print "Not found"
                liste=[]
        return liste

    def readSignal(self,shots,signals,criterion=None,sampling=None):
            results=dict()
            for y in shots:
                data=[]
                for x in signals:
                    data.append(self.wrapper.wrapSignal(y,x))
                result=pd.concat(data,axis=1)
                if criterion not None:
                	result=result.query(criterion)
                if sampling not None:
                	result.resample(sampling)
                result.columns=signals
                results[y]=result
            result=pd.concat(results,keys=shots)
            result.fillna()
            return result
    
             
    def changeAttr(self,shot,attrName,value):
#        try:
        try:
            if h5.setAttr(shot,self.wrapper.getPath([attrName],shot),value) ==1:
                df=pd.read_hdf(self.store,'shotDB')
                df[attrName][shot]=value
                df.to_hdf(self.store,'shotDB',format='table',nan_rep='nan',data_columns=True)
        except:
            return
        
             
            
            
    def initializeDB(self):
         listAttr=self.wrapper.getAttrList(detail='all')
         headers=listAttr['Name'].tolist()
         listshot=h5.getNbrfromFile(h5.listFiles())
         listattrs=[]
         for shot in listshot:   
             print shot
             paths=self.wrapper.getPath(headers,shot)
             #print paths
             #print h5.listAttrs(shot,paths)
             attrs=h5.listAttrs(shot,paths)
             listattrs.append(attrs)
         df=pd.DataFrame(listattrs,index=listshot,columns=headers) 
         #print listAttr['Name']
         for x in listAttr.Name.values:
             attr=listAttr.Processing.values[listAttr.Name.values==x][0]
             if attr=='datetime':
                 df[x]=pd.to_datetime(df[x])               
             if attr=='str':
                 df[x]=df[x].astype('S32')
             if attr=='float':
                 df[x]=df[x].astype(float)                 
             if attr=='bool':
                 df[x]=df[x].astype(bool)         
         #df.convert_objects()
         df.to_hdf(self.store,'shotDB',format='table',nan_rep='nan',data_columns=True)
               
      
    
