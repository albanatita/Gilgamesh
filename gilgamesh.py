# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 13:53:19 2015

@author: admin
"""
import os
import .wrapper as wrapper
import .shotManager as shotManager

sm=shotManager.ShotManager(wrapper.signalWrapper)

def listShots(criterion=None,attrList=None):
    return sm.listShots(criterion,attrList)
        
    
def listSignals(shot=None):
    if shot==None:
        return wrapper.signalWrapper.getSignalList()
    
def listAttrs(shot=None):
    if shot==None:
        return wrapper.signalWrapper.getAttrList()
    
def getSignal(shot,signal,criterion=None):
    return sm.readSignal(shot,signal,criterion)
    
def reduceSignal(shot,signal,operation,criterion=None):
	
def plot(data):
	
def overview(shot):
	
    
def listProgram():
    pass    