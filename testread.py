# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 13:58:17 2015

@author: admin
"""

import pandas as pd

table=pd.read_csv('map2D_normB_Ib=6kA.txt',skiprows=9,sep=r"\s+",lineterminator='\n',header=0)
#table.to_hdf('test.h5','table',append=False,compression='zlib')
store=pd.HDFStore('test.h5',complib='zlib')
store['data']=table
store.close()



