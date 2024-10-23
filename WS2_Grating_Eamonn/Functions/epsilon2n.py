# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:54:42 2022

@author: ph1pbx
"""

def epsilon2n(epsilonxx_r,epsilonxx_i,epsilonyy_r,epsilonyy_i,epsilonzz_r,epsilonzz_i):
    
    import numpy as np
    
    nxx=np.sqrt(0.5*(np.sqrt(epsilonxx_r**2+epsilonxx_i**2)+epsilonxx_r))
    kxx=np.sqrt(0.5*(np.sqrt(epsilonxx_r**2+epsilonxx_i**2)-epsilonxx_r))
    nyy=np.sqrt(0.5*(np.sqrt(epsilonyy_r**2+epsilonyy_i**2)+epsilonyy_r))
    kyy=np.sqrt(0.5*(np.sqrt(epsilonyy_r**2+epsilonyy_i**2)-epsilonyy_r))
    nzz=np.sqrt(0.5*(np.sqrt(epsilonzz_r**2+epsilonzz_i**2)+epsilonzz_r))
    kzz=np.sqrt(0.5*(np.sqrt(epsilonzz_r**2+epsilonzz_i**2)-epsilonzz_r))
    
    return nxx,kxx,nyy,kyy,nzz,kzz