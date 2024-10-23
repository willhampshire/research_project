# -*- coding: utf-8 -*-
"""
Created on Wed May 25 12:53:27 2022

@author: ph1pbx
"""

def argument_angle(kx,ky,k_inplan):
#UNTITLED2 Summary of this function goes here
# phi: value of the angle in degrees, comprise in the range [0;360[ degrees
# cos_phi: cosinus of the angle 
# sin_phi: sinus of the angle 
# Detailed explanation goes here  

    import numpy as np 

    if k_inplan==0:     
        phi=0    
    else:
        cos_phi=kx/k_inplan
        sin_phi=ky/k_inplan
        
        if abs(cos_phi**2+sin_phi**2-1)>10**-3:
            phi=555 
            print('error')
        else: 
            if sin_phi >= 0 :    
                phi=np.arccos(cos_phi)
                phi=np.degrees(phi)
            else:
                phi=np.arccos(cos_phi)
                phi=360-np.degrees(phi)
           
    return phi