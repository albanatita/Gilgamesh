# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:39:19 2015

@author: admin
"""

import core.wrapper as wrapper
import core.shotManager as shotManager
import environmentGilga as env
import pickle
import numpy as np

sm=shotManager.ShotManager(wrapper.signalWrapper)

def setGas(shotList,gas):
    for x in shotList:
        print x
        #try:
        sm.changeAttr(x,'Gas',gas)
       # except Exception as e:
       #     print e
        #    pass

def setProgram(shotList,program):
    for x in shotList:
        try:
            sm.changeAttr(x,'Program',program)
        except:
            pass
        
def createProgram(Name,Description):    
    listeProg=pickle.load(open(env.DBpath+"listeProg.txt","rb"))
    listeProg[Name]=Description
    pickle.dump(listeProg,open(env.DBpath+"listeProg.txt","wb"))
    
def listProgram():
    listeProg=pickle.load(open(env.DBpath+"listeProg.txt","rb"))   
    print listeProg

def setUseful(shotList,value):
    for x in shotList:
        sm.changeAttr(x,'Usefulk',value)

def maxIC(shotList):
    for x in shotList:
        print x
        try:
            signal=sm.readSignal([x],['IC_Pinj'])
            maximum=max(signal['IC_Pinj'])
        except Exception as e:
            print e
            maximum=np.nan
        sm.changeAttr(x,'MaxIC_Pinj',maximum)

def maxH(shotList):
    for x in shotList:
        print x
        try:
            signal=sm.readSignal([x],['H_Pinj'])
            maximum=max(signal['H_Pinj'])
        except Exception as e:
            print e
            maximum=np.nan
        sm.changeAttr(x,'MaxH_Pinj',maximum)    

 
def avgpressure(shotList):
    for x in shotList:
        print x
        try:
            signal=sm.readSignal([x],['Ngas_P'])
            maximum=np.mean(signal['Ngas_P'])            
        except Exception as e:
            print e
            maximum=np.nan
        sm.changeAttr(x,'AvgNgas_P',maximum)
   
def maxCurrent(shotList):
    for x in shotList:
        print x
        try:
            signal=sm.readSignal([x],['BigCoil_I'])
            maximum=max(signal['BigCoil_I'])
        except Exception as e:
            print e
            maximum=np.nan
        sm.changeAttr(x,'MaxBigCoil_I',maximum)

def maxDensity(shotList):
    for x in shotList:
        print x
        try:
            signal=sm.readSignal([x],['Lang_dens'])
            maximum=max(signal['Lang_dens'])
        except Exception as e:
            print e
            maximum=np.nan
        sm.changeAttr(x,'Maxdensity',maximum)

def maxCurrentSmall(shotList):
    for x in shotList:
        print x
        try:
            signal=sm.readSignal([x],['SmallCoil_I'])
            maximum=max(signal['SmallCoil_I'])
        except Exception as e:
            print e
            maximum=np.nan
        sm.changeAttr(x,'MaxSmallCoil_I',maximum)