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
langmuir=cp.LangmuirProbe('lang1','cylindrical',area)
diag.add_child(langmuir)
cp.show(tb)
cp.save('Test',tb)