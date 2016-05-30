# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 12:15:13 2016

@author: admin
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, c, m_e, m_p,epsilon_0, k, N_A

Troom=0.025 # Temperature  in eV 293K

class Gas():
    def __init__(self):
        self.Kiz0=0
        self.Kexc0=0
        self.sigmael=0
        self.sigmai=0
        self.epsiz=0
        self.epsexc=0
        self.m_i=0
        self.q=0

    def Kexc(self,Te):
        return self.Kexc0*np.exp(-e*self.epsexc/e/Te)
    
    def Kiz(self,Te):
        return self.Kiz0*np.exp(-e*self.epsiz/e/Te)

    def nuiz(self,Te,ng):
        return self.Kiz(Te)*ng
        
    def nuexc(self,Te,ng):
        return self.Kexc(Te)*ng

    def v_e(self,Te):
        return np.sqrt(8*e*Te/np.pi/m_e)

    def v_i(self,Ti):
        return np.sqrt(8*e*Ti/np.pi/self.m_i)        
        
    def nu_e(self,Te,ng):
        return ng*self.sigmael*self.v_e(Te)
    
    def lambda_e(self,Te,ng)    :
        return 1/self.nu_e(Te,ng)*self.v_e(Te)

    def nu_i(self,Ti,ng):
        return ng*self.sigmai*self.v_i(Ti)
    
    def lambda_i(self,Ti,ng)    :
        return 1/self.nu_i(Ti,ng)*self.v_i(Ti)
 
    def omegac_e(self,B):
        return e*B/m_e

    def omegap_e(self,ne):
        return np.sqrt(e**2.*ne/epsilon_0/m_e)

    def omegap_i(self,ni):
        return np.sqrt(self.q**2.*ni/epsilon_0/self.m_i)
        
    def omegac_i(self,B):
        return self.q*B/self.m_i
        
    def larmor_radius_e(self,B,Te):
        return self.v_e(Te)/self.omegac_e(B)
        
    def larmor_radius_i(self,B,Ti):
        return self.v_i(Ti)/self.omegac_i(B)
 
    def ng(self,Pg,Tg)       :  # Neutral density in function of pressure and temperature
        return Pg/k/Tg

def mbartoP(p):
    return p*100
   
class Argon(Gas):
    def __init__(self):
        self.Kiz0=5e-14
        self.Kexc0=0.16e-18
        self.sigmael=10e-19
        self.sigmai=10e-18
        self.epsiz=17.44
        self.epsexc=12.38
        self.m_i=40*m_p
        self.q=e
        
argon=Argon()
#print argon.omegac_i(0.2)
#print argon.omegac_e(0.2)
#print argon.larmor_radius_e(0.2,10)
print argon.nu_i(Troom,argon.ng(mbartoP(1e-4),293))
print argon.omegac_i(0.2)
#print argon.nu_e(10,argon.ng(13.3,293))
#print argon.v_i(Troom)

#Te=np.linspace(1e-2,1e2,100)
#plt.plot(Te,argon.Kexc(Te))

