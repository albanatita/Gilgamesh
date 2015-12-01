# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:11:02 2015

@author: admin
"""
import shelve
import environment as env
import shotManager as sm
import numpy as np

class Component(object):
    def __init__(self,name):
        self.children = []
        self.name=name

    def add_child(self, obj):
        self.children.append(obj)
        
class Diagnostics(Component):
    def __init__(self,name):
        self.signals=[]
        Component.__init__(self,name)
        
    def connectSignal(self,signalName):
        self.signals=signalName
    
class LangmuirProbe(Component):
     def __init__(self,name,typ,surface,position,Usignal,Isignal):
        self.type=typ
        self.surface=surface
        self.position=position
        self.Usignal=Usignal
        self.Isignal=Isignal
        Component.__init__(self,name)
        
     def getIV(self,shot,time,param={ramp:20,typ:'up',sweep:1e3}):
     	 Udataslice=sm.getSignal(shot,self.Usignal,criterion='index>'+str(time)+'&index<'+str(time+1/sweep*(ramp+1)))
     	 Idataslice=sm.getSignal(shot,self.Isignal,criterion='index>'+str(time)+'&index<'+str(time+1/sweep*(ramp+1)))
     	 maxi=argrelextrema(Udataslice, np.greater,order=ramp)
     	 mini=argrelextrema(Udataslice, np.less,order=ramp)
     	 indx=np.sort(np.hstack((maxi,mini)))[0]
     	 temp=np.split(Udataslice,indx)
     	 Udatadown=np.concatenate(temp[::2])
     	 Idatadown=np.concatenate(np.split(Idataslice,indx)[::2])
     	 idxsorted=np.argsort(Udatadown)
     	 Udatadown=Udatadown[idxsorted]
     	 Idatadown=Idatadown[idxsorted]   
     	 Udatadown=self.movingaverage(Udatadown,100) #check to modify here
     	 Udatauniq=np.unique(Udatadown)
     	 Idatauniq=np.zeros(len(self.Udatauniq))
     	 i=0
     	 while i<len(self.Udatauniq):
     	 	 self.Idatauniq[i]=np.mean(Idatadown[Udatadown==self.Udatauniq[i]])
             i=i+1
         self.Idatauniq=self.movingaverage(self.Idatauniq,100)
         return Udatauniq,Idatauniq # should actually return a dataframe
     
    def Vfloat(IV):
     
    def currentCorrection(IV):
    	indexsat=np.where(Idatauniq<=0)[0][-1]
        Vfloat=Udatauniq[indexsat]
        deltarange=(Vfloat-Udatauniq[0])
        rangea=[Vfloat-deltarange/2,Vfloat-deltarange/4]
        Ufit=
        Ifit=
    	fit = np.polyfit(Ufit,Ifit,1)
        fit_fn = np.poly1d(fit)
        Ifitcorr=np.subtract(Idatauniq,fit_fn(Udatauniq))
        Isat=fit_fn(Udatauniq)[indexsat]
        
    def T(IV):
    	diffI=np.diff(self.movingaverage(Ifitcorr[indexsat:-10],30))
		diffU=np.diff(Udatauniq[indexsat:-10])
		idxmax=np.argmax(diffI/diffU)
		Vplasma=(Udatauniq[indexsat:-10])[idxmax-1]
		Vdelta=Vplasma-Vfloat
		rangea=[Vfloat+Vdelta/4,Vfloat+Vdelta/2]
		Ufit=Udatauniq[(Udatauniq>=rangea[0])&(Udatauniq<=rangea[1])]
		Ilogfit=np.log(Ifitcorr[(Udatauniq>=rangea[0])&(Udatauniq<=rangea[1])])
		fit = np.polyfit(Ufit,Ilogfit,1)
		fit_fn = np.poly1d(fit)
		T=1/fit[0]
		
	def n(IV):
		e_electron=1.6022e-19
		if self.gas.text()=='Argon':
			Mi = 40*1.6726e-27
		if self.gas.text()=='Helium': 
			Mi = 4*1.6726e-27
		k_b = 1.3807e-23
		area=2*np.pi*1e-3*10e-3+np.pi*(1e-3)**2            
		dens = -Isat * np.sqrt(Mi)/(0.6 * e_electron * area * np.sqrt(k_b*T*11604))

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
            
def attachShot(version):
	
def loadFromShot(shot):
	