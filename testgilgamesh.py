# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:02:38 2015

@author: admin
"""


import sys
sys.path.append(r'C:\ISHTAR\\')
import gilgamesh.core.wrapper as wrapper
import gilgamesh.core.shotManager as shotManager
import gilgamesh as gil
#import hdf5Manager as h5
import shotTools
import numpy as np

s=gil.listShots(criterion='index<=1672&index>=1471')
liste=s.index.values
#shotTools.maxIC(liste)

#sm=shotManager.ShotManager(wrapper.signalWrapper)
#res=sm.isData(liste,'H_Pfwd')

#s=gil.listShots(criterion='index>1386')
#liste=s.index.values
#shotTools.maxCurrent(liste)

#wrapper.initWrapper()

#============ validation initialization wrapper
#w=wrapper.signalWrapper
#w.importSignalDB()
#w.initMapping()
#w.loadDB()
#===end


#s=gil.getSignal(1010,['IC_Pfwd','IC_Pref','IC_Pinj'])
#s.plot()
#print wrapper.signalWrapper.mapping

#=============== initialzation signalManager
#sm=shotManager.ShotManager(wrapper.signalWrapper)
#sm.initializeDB()
#================ end initialization

sm=shotManager.ShotManager(wrapper.signalWrapper)
wrapper.signalWrapper.saveMappingtoCSV()
#sm.readSignal([1505],['Ngas_P'])

#print sm.listShots()
#print sm.listShots(criterion='Date.date==Timestamp("2015-01-10")')

#listAttr=wrapper.signalWrapper.getAttrList(detail='all')
#listattrs=[]
#for shot in [1671]:
#     paths=wrapper.signalWrapper.getPath(listAttr,shot)
#     #print paths
#     #print h5.listAttrs(shot,paths)
#     attrs=[shot]+h5.listAttrs(shot,paths)
#     listattrs.append(attrs)
#print listattrs
#s=sm.readSignal([1000,1001],['Ngas_P','Lang_U'])