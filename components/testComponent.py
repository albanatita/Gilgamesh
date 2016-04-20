# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:51:05 2015

@author: admin
"""
import numpy as np

import component as cp

tb=cp.Testbed('IShTAR')
diag=cp.Diagnostics('Diagnostics')
tb.add_child(diag)
area=2*np.pi*1e-3*10e-3+np.pi*(1e-3)**2
langmuir=cp.LangmuirProbe('lang2','cylNC',area,'Lang_U2','Lang_I2')
diag.add_child(langmuir)
manipulator=cp.Manipulator('Manipulator','Manip_U','AvgManip_posRaw','AvgManip_pos')
tb.add_child(manipulator)
cp.show(tb)
cp.save('Centralv1',tb)