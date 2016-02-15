# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 18:36:46 2015

@author: rdi
"""

import sys
sys.path.append(r'C:\ISHTAR\\')
import pandas as pd
import gilgamesh.environmentGilga as env
import gilgamesh.core.hdf5Manager as h5
import gilgamesh.core.wrapper

class ShotManager():

    def __init__(self,wrap):
        self.wrapper=wrap
        self.wrapper.initShotManager(self)
        self.wrapper.loadDB()
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
                print y
                data=[]
                for x in signals:
                    try:
                        data.append(self.wrapper.wrapSignal(y,x))
                    except Exception,e:
                        print 'does not exist: ',e
                        signals.remove(x)    
                result=pd.concat(data,axis=1)
                result.fillna(method='ffill',inplace=True)
                result.columns=signals
                if criterion != None:
                    #print result
                    result=result.query(criterion)
                if sampling != None:
                	result.resample(sampling)

                results[y]=result
            result=pd.concat(results,axis=0,keys=shots)
            result.index.names=['Shot','Time']
            
            return result

    def reduceSignal(self,shots,signals,operation):
        ind=[]
        val=[]
        for yy in shots:
            for xx in signals:
                x=self.wrapper.wrapSignal(yy,xx).index.values
                y=self.wrapper.wrapSignal(yy,xx)[xx].values
                val.append(operation(y,x=x))
                ind.append(yy)
        return pd.DataFrame(val,index=ind)
                

    def isData(self,shots,signal):
        liste=[]
        for x in shots:
            #print x, signal
            res=h5.isData(x,self.wrapper.getSignalPath([signal],x)[0].values[0])
            #print x,res,self.wrapper.getSignalPath([signal],x)
            liste.append(res)
        return pd.DataFrame(liste,index=shots,columns=[signal])
            
             
    def changeAttr(self,shot,attrName,value):
#        try:
        try:
            if h5.setAttr(shot,self.wrapper.getPath([attrName],shot),value) ==1:
                df=pd.read_hdf(self.store,'shotDB')
                df[attrName][shot]=value
                df.to_hdf(self.store,'shotDB',format='table',nan_rep='nan',data_columns=True)
        except:
            return
        
    def getAttr(self,shot,attrName):
        df=pd.read_hdf(self.store,'shotDB')
        return df[attrName][shot]
            
            
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
               
      
    
