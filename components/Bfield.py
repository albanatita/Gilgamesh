# -*- coding: utf-8 -*-
"""
Created on Tue May 03 10:15:14 2016

@author: admin
"""
import sys
sys.path.append(r'C:\ISHTAR\\')
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy import interpolate
import gilgamesh.environmentGilga as env

class MainVessel():
    def __init__(self):
        self.L=1.1161
        self.r=0.55
        self.zstart=0.035
        
    def plot(self):
        plt.plot([self.zstart,self.zstart+self.L],[-self.r, -self.r],'k')
        plt.plot([self.zstart,self.zstart+self.L], [self.r,self.r],'k')
        plt.plot([self.zstart,self.zstart],[-self.r,self.r],'k')
        plt.plot([self.zstart+self.L, self.zstart+self.L],[-self.r,self.r],'k')
        
class PlasmaSource():
      def __init__(self):
        self.L=1.063
        self.r=0.2
        self.zstart=1.1161+ 0.035
    
      def plot(self):
        plt.plot([self.zstart, self.zstart+self.L], [-self.r,-self.r],'k')
        plt.plot([self.zstart, self.zstart+self.L], [self.r,self.r],'k')
        plt.plot([self.zstart, self.zstart],[-self.r,self.r],'k')
        plt.plot([self.zstart+self.L,self.zstart+self.L],[-self.r,self.r],'k')          

class Coil():
    def __init__(self,L,h,r,type):
        self.L=L
        self.h=h
        self.r=r
        self.zc=0
        self.type=type
        self.current=0
        
    def setZ(self,z):
        self.zc=z
        
    def setCurrent(self,I):
        self.current=I
        

class CoilSystem():
    def __init__(self,signalCurrent):
        self.listCoils=[]
        self.signalCurrent=signalCurrent
        self.path=env.DBpath+'components\\map_single_coil_1A\\'
    
    def addCoils(self,list):
        for x in list:
            self.listCoils.append(x)

    def plot(self):
        for x in self.listCoils:
            #bottom coil section
            plt.plot([x.zc-x.L/2,x.zc+x.L/2], [-(x.r+x.h), -(x.r+x.h)],'r')
            plt.plot([x.zc-x.L/2,x.zc+x.L/2], [-x.r, -x.r],'r')
            plt.plot([x.zc-x.L/2, x.zc-x.L/2], [-(x.r+x.h), -x.r],'r')
            plt.plot([x.zc+x.L/2, x.zc+x.L/2], [-(x.r+x.h), -x.r],'r')
    #% top coil section
            plt.plot([x.zc-x.L/2, x.zc+x.L/2], [x.r+x.h,x.r+x.h],'r')
            plt.plot([x.zc-x.L/2, x.zc+x.L/2], [x.r, x.r],'r')
            plt.plot([x.zc-x.L/2, x.zc-x.L/2], [x.r+x.h, x.r],'r')
            plt.plot([x.zc+x.L/2, x.zc+x.L/2], [x.r+x.h, x.r],'r')               

    def loadMapping(self,gridtype='200x200'):
            size=int(gridtype[0:3])
            fileName=self.path+'W7A_coil_1A_'+gridtype+'.txt'
            fileName2=self.path+'WEGA_coil_1A_'+gridtype+'.txt'
            w7aB = np.loadtxt(fileName,  skiprows=9)
            wegaB = np.loadtxt(fileName2,  skiprows=9)
            x=w7aB[:,1]
            self.x_w7a=x[0:size]
            self.z_w7a=w7aB[::size,2]
            self.Br_w7a=np.reshape(w7aB[:,3],(size,size))
            self.Bphi_w7a=np.reshape(w7aB[:,4],(size,size))
            self.Bz_w7a=np.reshape(w7aB[:,5],(size,size))
            x=wegaB[:,1]
            self.x_wega=x[0:size]
            self.z_wega=wegaB[::size,2]
            self.Br_wega=np.reshape(wegaB[:,3],(size,size))
            self.Bphi_wega=np.reshape(wegaB[:,4],(size,size))
            self.Bz_wega=np.reshape(wegaB[:,5],(size,size))      
    
    def calculate(self,resx=0.01,resz=0.01):
        x = np.arange(-0.5,2.5 , resx)
        z = np.arange(-0.5, 2.5, resz)
        Br=np.zeros((len(x),len(z)))
        Bphi=np.zeros((len(x),len(z)))
        Bz=np.zeros((len(x),len(z)))
        for coils in self.listCoils:        
            if coils.type==1:
                func=interpolate.interp2d(self.x_w7a,self.z_w7a+coils.zc,self.Br_w7a)
                Br=Br+func(x,z)*coils.current
                func=interpolate.interp2d(self.x_w7a,self.z_w7a+coils.zc,self.Bphi_w7a)
                Bphi=Bphi+func(x,z)*coils.current
                func=interpolate.interp2d(self.x_w7a,self.z_w7a+coils.zc,self.Bz_w7a)
                Bz=Bz+func(x,z)*coils.current
            if coils.type==2:
                func=interpolate.interp2d(self.x_wega,self.z_wega+coils.zc,self.Br_wega)
                Br=Br+func(x,z)*coils.current
                func=interpolate.interp2d(self.x_wega,self.z_wega+coils.zc,self.Bphi_wega)
                Bphi=Bphi+func(x,z)*coils.current
                func=interpolate.interp2d(self.x_wega,self.z_wega+coils.zc,self.Bz_wega)
                Bz=Bz+func(x,z)*coils.current
        return (x,z,Br,Bphi,Bz)
        

