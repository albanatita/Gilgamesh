# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 12:23:42 2015

@author: admin
"""

import fileManager as fm
import pandas as pd
import tables
import os

def write(name,data,fileName,io):
    store= pd.HDFStore(fileName, mode=io,driver="H5FD_CORE",driver_core_backing_store=0,complevel=9, complib='zlib')
    store[name]=data
    session=fm.session_factory()
    env=os.environ.copy()
    um=fm.userManager()
    usr=um.getUser(env["USRGILGA"],session)
    fileM=fm.fileManager(usr,session)
    image=store.returnHandle.get_file_image()
    fileM.save_file(fileName,image)
    store.close()
    
    
    
    