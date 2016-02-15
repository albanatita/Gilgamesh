# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 13:53:19 2015

@author: admin
"""
#import os
import core.wrapper as wrapper
import core.shotManager as shotManager
import qgrid
import matplotlib.pyplot as plt
import seaborn as sns
from traitlets import HasTraits, Int

sm=shotManager.ShotManager(wrapper.signalWrapper)
qgrid.nbinstall(overwrite=True)
qgrid.set_defaults(remote_js=True, precision=4)

def listShots(criterion=None,attrList=None,gui=False):
    """Display the list of discharges with the associated parameters

    criterion: String to select discharges based on the value of the parameters
    attrList: list of parameters to display
    
    Returns: pandas DataFrame
    """    
    
    result=sm.listShots(criterion,attrList)    
    if gui==True:
        qgrid.show_grid(result)     
    return result
        
    
def listSignals(shot=None):
    """Display list of signals available
    Returns pandas DataFrame    
    """
    if shot==None:
        return wrapper.signalWrapper.getSignalList()
    
def listAttrs(shot=None):
    """Display list
        Returns pandas DataFrame
    """
    if shot==None:
        return wrapper.signalWrapper.getAttrList()
    
def getSignal(shot,signal,criterion=None):
    """Load one or several signals
    
    shot=list of shots 
    signal: list of signals to load
    criterion: select values for which the signal is loaded
    
    returns: pandas DataFrame
    """
    return sm.readSignal(shot,signal,criterion)
    
def reduceSignal(shot,signal,operation,criterion=None):
    pass
 
def plot(data,gui=False):
    n=len(data.columns)
    size=int(len(data.index)/1000)+1
    fig, axs = plt.subplots(nrows=n)
    k=0
    for x in data.columns:
        shotplot=[]
        for z in data.index.get_level_values('Shot').unique():
            data.xs(z)[::size][x].plot(ax=axs[k],figsize=(6,8),legend=True)
            #shotplot.append(axs[k])
        #plt.legend(handles=shotplot)
        #plt.xlabel('Time')
        #sns.tsplot(time="Time", value=x, condition="Shot", data=data[::size],ax=axs[k])
        k=k+1
        
    
def _overview(shot,fig):
    s=getSignal([shot],['H_Pinj','IC_Pinj','BigCoil_I','SmallCoil_I','Ngas_P'])
    size=int(len(s.index)/1000)+1
    #fig=plt.figure()    
    ax0=fig.add_subplot(231)
    ax0.plot(s.xs(shot)[::size]['H_Pinj'])
    ax=fig.add_subplot(232,sharex=ax0)
    ax.plot(s.xs(shot)[::size]['IC_Pinj'])
    ax=fig.add_subplot(233,sharex=ax0)
    ax.plot(s.xs(shot)[::size]['BigCoil_I'])
    ax=fig.add_subplot(234,sharex=ax0)
    ax.plot(s.xs(shot)[::size]['SmallCoil_I'])    
    ax=fig.add_subplot(235,sharex=ax0)
    ax.plot(s.xs(shot)[::size]['Ngas_P'])    
#    fig.add_subplot(236)
#    plt.plot(s.xs(shot)[::size]['Lang_dens'])
 
class overviewWidget(HasTraits):
    shot=Int()
    
    def __init__(self):
        self.fig=plt.figure()
        super(HasTraits,self).__init__
    
    def _shot_changed(self, name,value):
        self.fig.clf()
        _overview(value,self.fig)
        self.fig.canvas.draw()
   
def listProgram():
    pass    