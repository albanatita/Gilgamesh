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
from ipywidgets import DOMWidget
from traitlets import Unicode, Int,List
import StringIO
import numpy as np
import pandas as pd
import json
import IPython.display as display
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

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
            ax1=data.xs(z)[::size][x].plot(ax=axs[k],figsize=(6,8),legend=True)
            shotplot.append(z)
        lines, labels = ax1.get_legend_handles_labels()
        ax1.legend(lines, shotplot, loc='best')     
        #plt.legend(handles=shotplot)
        #plt.xlabel('Time')
        #sns.tsplot(time="Time", value=x, condition="Shot", data=data[::size],ax=axs[k])
        k=k+1
    
def _overview(shot,fig):
    listSignal=['H_Pinj','IC_Pinj','BigCoil_I','SmallCoil_I','Ngas_P']
    s=getSignal([shot],listSignal)
    axes=wrapper.signalWrapper.getSignalAxes(listSignal)
    size=int(len(s.index)/1000)+1
    #fig=plt.figure()    
    ax0=fig.add_subplot(231)
    try:
        ax0.plot(s.xs(shot)[::size].index.values,s.xs(shot)[::size]['H_Pinj'])
        ax0.set_xlabel(axes.loc['H_Pinj']['Xaxis'])
        ax0.set_ylabel(axes.loc['H_Pinj']['Yaxis'])
    except:
        pass
    ax=fig.add_subplot(232,sharex=ax0)
    try:
        ax.plot(s.xs(shot)[::size].index.values,s.xs(shot)[::size]['IC_Pinj'])
        ax.set_xlabel(axes.loc['IC_Pinj']['Xaxis'])
        ax.set_ylabel(axes.loc['IC_Pinj']['Yaxis'])
    except:
        pass
    ax=fig.add_subplot(233,sharex=ax0)
    try:
        ax.plot(s.xs(shot)[::size].index.values,s.xs(shot)[::size]['BigCoil_I'])
        ax.set_xlabel(axes.loc['BigCoil_I']['Xaxis'])
        ax.set_ylabel(axes.loc['BigCoil_I']['Yaxis'])
    except:
        pass
    ax=fig.add_subplot(234,sharex=ax0)
    try:    
        ax.plot(s.xs(shot)[::size].index.values,s.xs(shot)[::size]['SmallCoil_I'])    
        ax.set_xlabel(axes.loc['SmallCoil_I']['Xaxis'])
        ax.set_ylabel(axes.loc['SmallCoil_I']['Yaxis'])
    except:
        pass  
    ax=fig.add_subplot(235,sharex=ax0)
    try:
        ax.plot(s.xs(shot)[::size].index.values,s.xs(shot)[::size]['Ngas_P'])    
        ax.set_xlabel(axes.loc['Ngas_P']['Xaxis'])
        ax.set_ylabel(axes.loc['Ngas_P']['Yaxis'])
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))

    except:
        pass
    fig.suptitle("Shot :"+str(shot), fontsize=14)
    fig.tight_layout()
#    fig.add_subplot(236)
#    plt.plot(s.xs(shot)[::size]['Lang_dens'])

def overview(shot,fig):
    return _overview(shot,fig)

def view(shot):
    fig=plt.figure(figsize=(8, 6))
    overview(shot,fig)
 
class overviewWidget(HasTraits):
    shot=Int()
    
    def __init__(self):
        self.fig=plt.figure()
        super(HasTraits,self).__init__
    
    def _shot_changed(self, name,value):
        self.fig.clf()
        _overview(value,self.fig)
        self.fig.canvas.draw()



class MyWidget(DOMWidget):
    _view_module = Unicode('nbextensions/SGWidget').tag(sync=True)
    _view_name = Unicode('MyWidgetView').tag(sync=True)
    value= Unicode().tag(sync=True)
    columns=Unicode().tag(sync=True)
    selection=List().tag(sync=True)

class HandsonDataFrame(object):
    def __init__(self, df):
        self._df = df
        self._selection=[]
        self._widget = MyWidget()
        self._widget.on_trait_change(self._on_data_changed, 'selection')
        self._widget.on_displayed(self._on_displayed)
        
    def _on_displayed(self, e):
        # DataFrame ==> Widget (upon initialization only)
        json1 = self._df.to_json(orient='records')
        self._widget.value = json1
        col = list(self._df.columns.values)
        columns=[]
        for x in col:
            columns.append({'id':x,'name':x,'field':x})
        self._widget.columns = json.dumps(columns)
        self._widget.selection=[]
        
    def _on_data_changed(self, e, val):
        self._selection=val
    
    def get_selection(self):
        print self._widget.selection
    
    def to_dataframe(self):
        return self._df
        
    def show(self):
        display(self._widget)     
    
   
def listProgram():
    pass    