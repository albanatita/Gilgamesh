# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 12:23:42 2015

@author: admin
"""


import pandas as pd
import os
import StringIO

import pgcontents.query as pgquery
from sqlalchemy import create_engine
#from base64 import (
#    b64encode,
#)

#def writes_base64(fileContent):
#    """
#    Write a notebook as base64.
#    """
#    return b64encode(fileContent.encode('utf-8'))

class Export():
    
    def __init__(self,fileName):
        self.store=pd.HDFStore(fileName, mode='w',driver="H5FD_CORE",driver_core_backing_store=0,complevel=9, complib='zlib')
        self.fileName='/'+fileName
        
    def close(self):
        image=self.store.returnHandle().get_file_image().encode('base64','strict')
        env=os.environ.copy()
        usr=env["USRGILGA"]
        with create_engine('postgresql://postgres:ishtar@localhost/ishtar').begin() as db:
            pgquery.save_file(db, usr, '/export/'+self.fileName, image, 0)     
        self.store.close()

    def addData(self,name,data):
        self.store[name]=data      

def loadFile(filename,shared=False)   :
    if shared:
        usr="share"
    else:
        env=os.environ.copy()
        usr=env["USRGILGA"]
    db=create_engine('postgresql://postgres:ishtar@localhost/ishtar')
    binarycontent=pgquery.get_file(db, usr, filename, include_content=True)['content']   
    db.dispose()
    return StringIO.StringIO(binarycontent.decode('base64'))
        
    
    
    