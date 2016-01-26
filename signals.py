# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 13:00:52 2015

@author: admin
"""

def picinj(shot,sm):
    signal1=sm.readSignal([shot],'IC_Pfwd')
    signal2=sm.readSignal([shot],'IC_Pref')
    return signal1-signal2
    
def mapping(signal,liste):
    resliste=[]
    for x in liste:
        resliste.append(1)
    return resliste