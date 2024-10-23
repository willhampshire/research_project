# -*- coding: utf-8 -*-
"""
Created on Fri May 27 12:37:36 2022

@author: ph1pbx
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 25 16:32:02 2022

@author: ph1pbx
"""

def get_sp_Amplitude_Phase(polar,phi):
    
    import math
    import numpy as np
                                      
    # Excitation polarization x
    A_s_H=math.sin(phi*math.pi/180)
    A_p_H=math.cos(phi*math.pi/180)
    phase_s_H=180
    phase_p_H=0
    # Excitation polarization y
    A_s_V=math.cos(phi*math.pi/180)
    A_p_V=math.sin(phi*math.pi/180)
    phase_s_V=0
    phase_p_V=0
    # Excitation polarization 45°
    A_s_D=math.sin(math.pi/4 - phi*math.pi/180)
    A_p_D=math.sin(math.pi/4 + phi*math.pi/180)
    phase_s_D=0
    phase_p_D=0
    # Excitation polarization -45°
    A_s_A=math.sin(math.pi/4 + phi*math.pi/180)
    A_p_A=math.sin(math.pi/4 - phi*math.pi/180)
    phase_s_A=180
    phase_p_A=0
    # Excitation polarization L
    A_s_L=1/math.sqrt(2)
    A_p_L=1/math.sqrt(2)
    phase_s_L=90+phi
    phase_p_L=phi
    # Excitation polarization R			
    A_s_R=1/math.sqrt(2)
    A_p_R=1/math.sqrt(2)
    phase_s_R=270-phi
    phase_p_R=-phi
           
    if (polar>0):  # Single polarization
        if (polar==1): # polar x
            A_s=A_s_H
            A_p=A_p_H
            phase_s=phase_s_H
            phase_p=phase_p_H
        elif (polar==2): # polar y		
            A_s=A_s_V
            A_p=A_p_V
            phase_s=phase_s_V
            phase_p=phase_p_V
        elif (polar==3): # polar L
            A_s=A_s_L
            A_p=A_p_L
            phase_s=phase_s_L
            phase_p=phase_p_L
        elif (polar==4): # polar R
            A_s=A_s_R
            A_p=A_p_R
            phase_s=phase_s_R
            phase_p=phase_p_R
        elif (polar==5): # polar s
            A_s=1
            A_p=0
            phase_s=0
            phase_p=0
        elif (polar==6): # polar p
            A_s=0
            A_p=1
            phase_s=0
            phase_p=0
        elif (polar==7): # polar 45°
            A_s=A_s_D
            A_p=A_p_D
            phase_s=phase_s_D
            phase_p=phase_p_D
        elif (polar==8): # polar -45°
            A_s=A_s_A
            A_p=A_p_A
            phase_s=phase_s_A
            phase_p=phase_p_A
        else:
            print("invalid polarization")
        phase_s=phase_s*(np.pi/180)
        phase_p=phase_p*(np.pi/180)    
 
    return A_p,A_s,phase_p,phase_s