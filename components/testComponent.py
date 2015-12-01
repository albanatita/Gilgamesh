# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:51:05 2015

@author: admin
"""

import component as cp

tb=cp.Testbed('IShTAR')
diag=cp.Diagnostics('Diagnostics')
tb.add_child(diag)
langmuir=cp.LangmuirProbe('lang1','cylindrical',1e-2)
diag.add_child(langmuir)
cp.show(tb)
cp.save('Test',tb)