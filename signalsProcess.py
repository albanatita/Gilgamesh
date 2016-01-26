# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 13:00:52 2015

@author: admin
"""
import pandas as pd
import numpy as np

def picinj(shot,sm):
    signal1=sm.readSignal([shot],['IC_Pfwd'])
    signal2=sm.readSignal([shot],['IC_Pref'])
    res=pd.DataFrame(signal1.values-signal2.values,index=signal1.xs(shot).index.values,columns=['IC_Pinj'])
    return res

def picratio(shot,sm):
    signal1=sm.readSignal([shot],['IC_Pfwd'])
    signal2=sm.readSignal([shot],['IC_Pref'])
    return pd.DataFrame(np.true_divide(signal2.values,signal1.values),index=signal1.xs(shot).index.values,columns=['IC_ratio'])
    
def phinj(shot,sm):
    signal1=sm.readSignal([shot],['H_Pfwd'])
    signal2=sm.readSignal([shot],['H_Pref'])
    res=pd.DataFrame(signal1.values-signal2.values,index=signal1.xs(shot).index.values,columns=['H_Pinj'])

    return res

def hratio(shot,sm):
    signal1=sm.readSignal([shot],['H_Pfwd'])
    signal2=sm.readSignal([shot],['H_Pref'])
    return pd.DataFrame(np.true_divide(signal2.values,signal1.values),index=signal1.xs(shot).index.values,columns=['H_ratio'])
    
def mapping(signal,liste):
    resliste=[]
    for x in liste:
        resliste.append(1)
    return resliste
    
def bdotcalib1(data):
    res=data.applymap(lambda x:10**(((x-0.02- 2.2503)/0.0520+10)/10))
    return res

def langu(data):
    res=data.applymap(lambda x:x*20)
    return res

def langi(data):
    res=data.applymap(lambda x:-0.01*x)
    return res
        