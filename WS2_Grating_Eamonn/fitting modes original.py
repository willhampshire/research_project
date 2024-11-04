# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:50:09 2023

@author: ph1pbx
"""
# import matlab.engine
import math
import time
time_run = time.time()
import os
from math import pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from Functions.argument_angle import argument_angle
from Functions.Strong_coupling_model import Strong_coupling_model
from Functions.RCWA_spectrum import RCWA_spectrum
from Functions.Plot_refractive_indices import Plot_refractive_indices
from Functions.epsilon2n import epsilon2n
from Functions.Lorentz_oscillator import Lorentz_oscillator

Project_name="Grating project"

N=50

# %% Grating modes model

k_model=np.linspace(-5,5,200) 

v1=0.034 # eV.um
v2=0.027 # eV.um
U=0.090 # eV
E0=1.47 # eV

E1=E0-np.sqrt(U**2+(v1*k_model)**2)
E2=E0+np.sqrt(U**2+(v2*k_model)**2)
# %% Spectral range of the starting point    
N_lambda=N 

lbda_min=1240/2.20
lbda_max=1240/1.00
     
lbda = np.linspace(lbda_min/1000,lbda_max/1000,N_lambda) 
E=1.23987/lbda
# %% Wave_vector
# N_k=701
N_k=N
# k_scan=np.linspace(-6.7,6.7,N_k) #mu-1
kmax=5
k_scan=np.linspace(-kmax,kmax,N_k) #mu-1
ky=0.000 #mu-1

# %% Common parameters
N_ord=7 #Choice of the number of orders taken into account during simulation, recommendation: 7 for 1D, 50 for 2D
polar=2 #Polarization of incident wave: 1-> x, 2-> y, 3->L, 4->R, 5->s, 6->p, 7->45°, 8->-45°, 0-> All 6 polarizations (H,V,D,A,L,R) for the Stoke parameter
# %% Materials definition(two ways: 1/ Location for a dispersive material; 2/[n,k] for a non-dispersive material
material=[]
material.append([1,0]) # superstrate air

# TMD
material.append('Materials/WS2_Munkhbat2022.txt') # 

########################## Subtrate #############################################

#Si02
# material.append([1.46,0]) # Substrate 2 SiO2
# material.append('Materials/cSi_Green_2008.txt') # Substrate 1 Si
# t_substrate_2=0.28 # micron SiO2
# t_substrate_1=2 #micron Si

#Au
material.append('Materials/Au_Johnson.txt') # Substrate 2 SiO2
material.append('Materials/cSi_Green_2008.txt') # Substrate 1 Si
t_substrate_2=0.150 # micron Au
t_substrate_1=2 #micron Si

#Si
# material.append('Materials/cSi_Green_2008.txt') # Substrate 2 SiO2
# material.append('Materials/cSi_Green_2008.txt') # Substrate 1 Si
# t_substrate_2=1 #micron Si
# t_substrate_1=1 # micron Si

# Bragg
# material.append([1.46,0]) # Substrate 2 SiO2
# material.append('Materials/cSi_Green_2008.txt') # Substrate 1 Si
# t_substrate_2=0.280# micron SiO2
# t_substrate_1=2 #micron Si


# Plot_refractive_indices(lbda,material) #f9 to plot refractive indices
# %% Structure definition 

t=0.085
ax=0.360
FF=0.80

w=FF*ax

# %% Layer definition (from top to bottom of the stack): each layer is defined by
    # [THICKNESS, MATERIAL] with 
    # thickness: in um 
    # material: the material is given by its order defined in the list of material definition
layer=[] 
layer.append([0,1])             # Superstrate 
layer.append([t,2])         # Grating
layer.append([t_substrate_2,3]) # Subtrate 2
layer.append([t_substrate_1,4]) # Subtrate 1

layer_sub=[] 
layer_sub.append([0,1])             # Superstrate
layer_sub.append([0,2])             # Grating
layer_sub.append([t_substrate_2,3]) # Subtrate 2
layer_sub.append([t_substrate_1,4]) # Subtrate 1
# %% Pattern definition: each pattern is defined by
   # [pattern location, pattern material, form, [x pos, y pos], [x size, y size], angle] with
   # pattern location: the location in the stack of the pattern is defined by the orde of the corresponding layer in the Layer list
   # pattern material: the material is given by its order defined in the list of material definition
   # form: 1->grating 2->circular 3->rectangular 4->ellipse 
   # (x pos,y pos): position of the centre of the pattern in xy plan --> um
   # (x size,y size): size of the pattern along x and y axis --> um
   # angle : rotated angle of the x-axis of the pattern with the X-axis of the lattice --> degrees
   # NOTE 1: if one pattern is a 1D grating, the other patterns cannot be 2D patterns
   # NOTE 2: for 1D grating, only x size is taken into account
   # NOTE 3: for ciruclar pattern, the diameter is gven by x size, and y size is not taken into account
   # NOTE 4: angle is not taken into account for grating and circular pattern
   # NOTE 5: For planar simulation: pattern={}; u=[0.1,0] v=[0,0] N_ord=1
pattern=[]
pattern.append([2,1,1,[0,0],[ax-w,0],0])

pattern_layer=[]
# %% Lattices (two unit vectors of the Bravais lattice), defined with
    # u=[u_x,u_y] and v=[v_x,v_y]
    # NOTE: for 1D grating, the simulation will be calculated with u=(ux,0) and v=(0,0)
u=[ax,0]
v=[0,0]
# %% For loop
A=np.zeros((lbda.size,k_scan.size),dtype=float)
R=np.zeros((lbda.size,k_scan.size),dtype=float)
T=np.zeros((lbda.size,k_scan.size),dtype=float)
A_sub=np.zeros((lbda.size,k_scan.size),dtype=float)
R_sub=np.zeros((lbda.size,k_scan.size),dtype=float)
T_sub=np.zeros((lbda.size,k_scan.size),dtype=float)
for i_k in range(0,k_scan.size):
    kx=k_scan[i_k]  
    k_inplan=math.sqrt(kx**2+ky**2)
    ## Conic angle (in degrees)
    phi=argument_angle(kx,ky,k_inplan)
    # phi=argument_angle(ky,kx,k_inplan)
    ## Incident angles (in degrees)
    theta=np.arcsin(k_inplan/2/pi*lbda)
    theta=np.degrees(theta)    
    remove_lambda=(abs(theta.imag)>0).nonzero()
    theta[remove_lambda]=0 
    ## Run S4 simulation for each wavelength
    lbda,R[:,i_k],T[:,i_k],A[:,i_k]=RCWA_spectrum(lbda,material,layer,pattern,u,v,phi,theta,polar,N_ord)
    lbda,R_sub[:,i_k],T_sub[:,i_k],A_sub[:,i_k]=RCWA_spectrum(lbda,material,layer_sub,pattern_layer,u,v,phi,theta,polar,N_ord)
    # lbda,R_sub[:,i_k],T_sub[:,i_k],A_sub[:,i_k]=RCWA_spectrum(lbda,material,layer,pattern,u,v,phi,theta,8,N_ord)
    E=1.23984/lbda

    A[remove_lambda,i_k]=np.nan
    R[remove_lambda,i_k]=np.nan
    T[remove_lambda,i_k]=np.nan    
    
    A_sub[remove_lambda,i_k]=np.nan
    R_sub[remove_lambda,i_k]=np.nan
    T_sub[remove_lambda,i_k]=np.nan 

# %%
elapsed = time.time() - time_run
print('elapsed time '+str("%.1f" % elapsed)+'s')
 
# %% Plot result
signalR=(R-R_sub)/R_sub
# signalR=(R-R_sub)
signalR=(signalR-np.min(signalR))/(np.max(signalR)-np.min(signalR))
# signalR=R

signalA=(A-A_sub)/A_sub
signalA=(signalA-np.min(signalA))/(np.max(signalA)-np.min(signalA))
# signalA=A

plt.rcParams['font.size'] = '16'

saving_name='t'+str("%.0f" % np.multiply(1e3,t))+'nm a='+str("%.0f" % np.multiply(1e3,ax))+'nm FF='+str("%.2f" % FF)
title_name=Project_name+'\n'+saving_name

fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
pcm=axs.pcolor(k_scan,1.240/lbda,signalR,cmap='viridis',clim=(0,1))  
axs.set(xlabel='k$_x$($\mu$m)',xlim=(-kmax,kmax),ylim=(1240/lbda_max, 1240/lbda_min), ylabel='Photon Energy(eV)',title=title_name)
axs.plot(k_model,E1,'r--') 
axs.plot(k_model,E2,'r--') 
cbar =fig.colorbar(pcm,location='right')
cbar.set_label('Reflectivity contrast') 

# %% Save DATA

# R_data=np.column_stack([lbda, R])
# R_data=np.row_stack([np.concatenate([[np.nan],k_scan]), R_data])
# A_data=np.column_stack([lbda, A])
# A_data=np.row_stack([np.concatenate([[np.nan],k_scan]), A_data])
# T_data=np.column_stack([lbda, T])
# T_data=np.row_stack([np.concatenate([[np.nan],k_scan]), T_data])

# R_sub_data=np.column_stack([lbda, R_sub])
# R_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), R_sub_data])
# A_sub_data=np.column_stack([lbda, A_sub])
# A_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), A_sub_data])
# T_sub_data=np.column_stack([lbda, T_sub])
# T_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), T_sub_data])

# np.savetxt('Results/'+saving_name+"_R.txt", R_data)
# np.savetxt("Results/"+saving_name+"_A.txt", A_data) 
# np.savetxt("Results/"+saving_name+"_T.txt", T_data)   
# np.savetxt('Results/'+saving_name+"_R_sub.txt", R_sub_data)
# np.savetxt('Results/'+saving_name+"_A_sub.txt", A_sub_data) 
# np.savetxt('Results/'+saving_name+"_T_sub.txt", T_sub_data) 
