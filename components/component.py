# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:11:02 2015

@author: admin
"""
import shelve
import gilgamesh.gilgamesh as gil
import gilgamesh.core.wrapper as wrapper
import gilgamesh.environmentGilga as env
import gilgamesh.core.shotManager as shotManager
import numpy as np
import gilgamesh.core.hdf5Manager as h5m
import pickle
#import seaborn as sns
import pandas as pd
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import math
import seaborn as sns
import pyqtgraph as pg




sm=shotManager.ShotManager(wrapper.signalWrapper)

class Component(object):
    def __init__(self,name):
        self.children = []
        self.name=name

    def add_child(self, obj):
        self.children.append(obj)
        
    def getData(self):
        return [self.name]
    
    def findElement(self,liste,typeel):
        if self.children==[]:
            return liste
        else:
            for x in self.children:
                if isinstance(x,typeel):
                    liste.append(x)
                x.findElement(liste,typeel)
            return liste

    def findByName(self,name):
        if self.name==name:
            return self
        if self.children==[]:
            return 0
        for x in self.children:
            result=x.findByName(name)
            if result is not 0:
                return result
                break
        
class Diagnostics(Component):
    def __init__(self,name):
        Component.__init__(self,name)

class Manipulator(Component)        :
    def __init__(self,name,signal,manual,position):
         Component.__init__(self,name)
         self.signal=signal
         self.manual=manual
         self.position=position

    def getData(self):
        list=super.getData()
        list.append([self.signal,self.manual,self.position])
    
    def convertPos(self,shot):
        try:
            position=max(np.array(gil.getSignal(shot,self.signal)[self.signal].values))
        except:
            try:
                position=gil.sm.getAttr(shot,self.manual)
                fit = np.polyfit(self.getCalibration()[0],self.getCalibration()[1],1)
                fit_fn = np.poly1d(fit)
                position=fit_fn(position)
                
            except Exception,e:
                print e
                position=np.nan
        return position
           
    def getCalibration(self):
        datax=[1444,1341,1252,1162,1068,974,914,868,805,729,660,600,548,446]
        datay=[55.3,49.4,44.7,39.9,35,30.1,26.9,24.45,21.1,17.1,13.35,10.15,7.6,2.2]        
        return [datax,datay]
    
class LangmuirProbe(Component):
     def __init__(self,name,typ,surface,position,Usignal,Isignal):
        self.type=typ
        self.surface=surface
        self.position=position
        self.Usignal=Usignal
        self.Isignal=Isignal
        Component.__init__(self,name)
     
     def getData(self)     :
        return {'Type':self.type,'Surface':self.surface,'Position':self.position,'Voltage':self.Usignal,'Current':self.Isignal}
     
     def loadData(self,shot):
        self.UI=sm.readSignal([shot],[self.Usignal,self.Isignal]).xs(shot)
        
     def plotUI(self,shot,time,figure):
        IV=self.getrawIV(shot,time,self.UI,param={'ramp':10,'typ':'down','sweep':100,'backgnd':False,'process':'smooth'})
        plt.figure(figsize=(30, 10))        
        plt.scatter(IV.U.values,IV.I.values)
        
     
     def getUI(self,shot):
         return sm.readSignal([shot],[self.Usignal,self.Isignal]).xs(shot)
     
     def calculateTime(self,shot,start,stop,step,param={'ramp':10,'typ':'down','sweep':1e3,'backgnd':False,'process':'smooth'},UI=None):
         #nb=int(duration/step)
         timearray=np.arange(start,stop,step)
         liste=[]
         if UI==None:
             UI=sm.readSignal([shot],[self.Usignal,self.Isignal]).xs(shot)
         for x in timearray:
             print x
             liste.append(self.calculatePlasma(shot,x,UI))
         result=np.vstack(liste)
         return pd.DataFrame(result,columns=['time','Vfloat','n','T','Vplasma'])
      
     def calculateSingle(self,shot,time,show=False,showData=False,param={'ramp':10,'typ':'down','sweep':1e3,'backgnd':False,'process':'smooth'}):
         UI=sm.readSignal([shot],[self.Usignal,self.Isignal]).xs(shot)
         return self.calculatePlasma(shot,time,UI,show=show,showData=showData,param=param)
     
     def calculatePlasma(self,shot,time,UI,show=False,showData=False,param={'ramp':10,'typ':'down','sweep':1e3,'backgnd':False,'process':'smooth'}):
#         try:         
             IV=self.getrawIV(shot,time,UI,param=param)
             #axi=IV.plot(x='U',y='I',kind='scatter')
             if show:
                 if showData==False:
                     plt.figure()
                     plt.scatter(IV.U.values,IV.I.values)
                 else:
                     pl1=showData[0]
                     pl1.clear()
                     pl1.plot(IV.U.values,IV.I.values,pen=None,symbol='o',symbolSize=1)

                 #pl.draw()
                 #ax=fig.add_subplot(211)
                 #plt.scatter(IV.U,IV.I)
             result=self.getIVsmooth(IV)
             if show:
                 if showData==False:
                     plt.plot(result.index.values,result['I'].values)
                 else:
                     pl1.plot(result.index.values,result['I'].values,pen=(0,255,0))
                 #pl1.plot(result+result2,pen=(255,0,0))
                 #print IV.groupby('I').mean()
                 #sns.tsplot(IV.grouby('I').mean()['U'].values,IV.grouby('I').mean().index.values,ax=ax)
             #result.plot(ax=axi)
             Isat, Vfloat, result2=self.currentCorrection(result)
             if show:
                 pass
                 #plt.plot(result2)
             #print 'Isat',Isat
             if math.isnan(Isat):
                 print 'current too small'
                 return [time,np.nan,np.nan,np.nan,np.nan]
             #result2.plot(ax=axi)
             Vplasma,T=self.T(result2,Vfloat)
             #print Vplasma,T
             n=self.n(Isat,T,shot)
             print  n
             return [time,Vfloat,n,T,Vplasma]
#         except Exception,e:
#             print e
#             return [time,np.nan,np.nan,np.nan,np.nan]
     	 
     def getrawIV(self,shot,time,UI,param={'ramp':20,'typ':'down','sweep':1e3,'backgnd':False,'process':'smooth'}):
         ramp=param['ramp']
         typ=param['typ']
         sweep=param['sweep']
         query='index>'+str(time)+'&index<'+str(time+1/sweep*(ramp+1))

         UIdataslice=UI.query(query)
         #print UIdataslice
         Udataslice=UIdataslice[self.Usignal].values        
         Idataslice=UIdataslice[self.Isignal].values
         if typ=='down':         
             maxi=argrelextrema(Udataslice, np.greater,order=ramp)
             mini=argrelextrema(Udataslice, np.less,order=ramp)
             indx=np.sort(np.hstack((maxi,mini)))[0]
             temp=np.split(Udataslice,indx)
             Udatadown=np.concatenate(temp[::2])
             Idatadown=np.concatenate(np.split(Idataslice,indx)[::2])
         if typ=='all':
             Udatadown=Udataslice
             Idatadown=Idataslice
         return pd.DataFrame({'U':Udatadown,'I':Idatadown}).sort_values('I')
     
     def getIVsmooth(self,UI,dev=False):
         res1=UI.groupby(['U']).mean()
         result=pd.rolling_mean(res1,10)
         if dev:
             result2=pd.rolling_std(res1,10)
             return result2,result
         else:
             return result
     
     
     def currentCorrection(self,IVsmooth):
        try:
            Vfloat=max(IVsmooth[IVsmooth.I<=0].index.values)
        except:
            Vfloat=0
        #print 'Vfloat : '+str(Vfloat)
        deltarangeini=IVsmooth.index.values[0]+10
        dataI=IVsmooth[deltarangeini:Vfloat-10].I.values
        dataV=IVsmooth[deltarangeini:Vfloat-10].index.values
        fit = np.polyfit(dataV,dataI,1)
        fit_fn = np.poly1d(fit)
        Ifitcorr=np.subtract(IVsmooth.I.values,fit_fn(IVsmooth.index.values))
        Isat=fit_fn(Vfloat)

        if fit_fn(20)>=0:
            Isat=np.nan
            Vfloat=np.nan
        return Isat,Vfloat,pd.DataFrame({'I':Ifitcorr},index=IVsmooth.index.values)
        
     def T(self,IVcorr,Vfloat):
        diffI=np.diff(IVcorr[Vfloat:].I.values)
        diffU=np.diff(IVcorr[Vfloat:].index.values)
        idxmax=np.argmax(diffI/diffU)
        Vplasma=(IVcorr[Vfloat:].index.values)[idxmax-1]
        Vdelta=Vplasma-Vfloat
        #rangea=[Vfloat+Vdelta/4,Vfloat+Vdelta/2]
        rangea=[Vfloat,Vfloat+Vdelta/2]
        IVfit=IVcorr[rangea[0]:rangea[1]]
        Ufit=IVfit.index.values
        Ilogfit=np.log(IVfit.I.values)
        fit = np.polyfit(Ufit,Ilogfit,1)
        #plt.figure()
        #IVfit.plot()
#        fit_fn = np.poly1d(fit)
        T=1/fit[0]
        return Vplasma,T
		
     def n(self,Isat,T,shot):
          e_electron=1.6022e-19
          gas=sm.getAttr(shot,'Gas')
          #print gas
          if gas=='Argon':
              Mi = 40*1.6726e-27
          if gas=='Helium': 
              Mi = 4*1.6726e-27
          k_b = 1.3807e-23
          area=2*np.pi*1e-3*10e-3+np.pi*(1e-3)**2            
          dens = -Isat * np.sqrt(Mi)/(0.6 * e_electron * area * np.sqrt(k_b*T*11604))
          return dens

class Testbed(Component):
    def __init__(self,name):
        Component.__init__(self,name)
        
def show(component,prefix=''):
    print prefix+component.name
    for x in component.children:
        show(x,prefix+'-')

def save(version,component):
    filename=env.DBpath+'ComponentStore'
    d = shelve.open(filename)
    d[version]=component
    d.close()
    
def load(version):
    filename=env.DBpath+'ComponentStore'
    d = shelve.open(filename)  
    return d[version]

def initComponentDB():
	defaultcomponent='empty'
	liste=h5m.getNbrfromFile(h5m.listFiles())
	DB=dict()
	for x in liste:
		DB[x]=defaultcomponent
	pickle.dump( DB, open( env.DBpath+"ComponentDB.bin", "wb" ) )

def attachShot(version,shotList):
    DB=pickle.load( open( env.DBpath+"ComponentDB.bin", "rb" ) )
    for x in shotList:
    	DB[x]=version
    pickle.dump( DB, open( env.DBpath+"ComponentDB.bin", "wb" ) )

def componentShot():
	DB=pickle.load( open( env.DBpath+"ComponentDB.bin", "rb" ) )
	print DB


def loadFromShot(shot):
	DB=pickle.load( open( env.DBpath+"ComponentDB.bin", "rb" ) )
	version=DB[shot]
	return load(version)