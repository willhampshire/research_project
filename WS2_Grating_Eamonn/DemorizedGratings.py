# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:24:46 2024

@author: php23ojp
demorized gratings to obtain quasi-BIC gratings
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:50:09 2023

@author: ph1pbx
quasi-BIC with 2-layer gratings  
"""
# import matlab.engine
import math
import time
t = time.time()
import os
from math import pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from Functions.argument_angle import argument_angle
from Functions.RCWA_spectrum import RCWA_spectrum
from Functions.Plot_refractive_indices import Plot_refractive_indices

Project_name="Demorized Gratings"
# %% Materials definition(two ways: 1/ Location for a dispersive material; 2/[n,k] for a non-dispersive material
material=[]
material.append([1,0]) # superstrate air

# material.append('Materials/WSe2_1L_Gu2019.txt') #WSe2_1L_Gu2019 WSe2_5L_Gu2019 MoS2_1L_Islam2021 TMD2 WSe2_Hsu2019 MoSe2_Hsu2019
material.append('Materials/WS2_Munkhbat2022.txt') #WSe2_1L_Gu2019 WSe2_5L_Gu2019 MoS2_1L_Islam2021 TMD2 WSe2_Hsu2019 MoSe2_Hsu2019
# material.append('Materials/hBN_Zotev.txt') # TMD etched
# material.append('Materials/WSe2_Zotev.txt')

#material.append('Materials/WS2_Munkhbat2022.txt') # TMD etched   WS2_Zotev
#material.append('Materials/WS2_Munkhbat2022.txt') # TMD1  #WS2_Munkhbat2022 WS2_Zotev
#material.append('Materials/GaAs_Rakic.txt')
#material.append([2.2,0])
#material.append('Materials/PMMA950.txt')
#material.append('Materials/hBN_Zotev.txt') # 
#material.append('Materials/hBN_Zotev.txt') # 

########################## Subtrate #############################################

#Si02
material.append([1.46,0]) # Substrate 2 SiO2
material.append('Materials/cSi_Green_2008.txt') # Substrate 1 Si
t_substrate_2=0.290 # micron SiO2
t_substrate_1=2 #micron Si

#Au
# material.append('Materials/Au_Johnson.txt') # Substrate 2 SiO2
# material.append('Materials/cSi_Green_2008.txt') # Substrate 1 Si
# t_substrate_2=0.150 # micron Au
# t_substrate_1=2 #micron Si

# #Au/SiO2/Si
# material.append('Materials/Au_Johnson.txt') # Substrate 2 SiO2
# material.append([1.46,0]) # Substrate 2 SiO2
# material.append('Materials/cSi_Green_2008.txt') # Substrate 1 Si
# t_substrate_2=0.010 # micron Au
# t_substrate_1=0.150 #micron  SiO2
# t_substrate_0=2 # micron  Si

#Si
# material.append('Materials/cSi_Green_2008.txt') # Substrate 2 SiO2
# material.append('Materials/cSi_Green_2008.txt') # Substrate 1 Si
# t_substrate_2=1 #micron Si
# t_substrate_1=1 # micron Si
####################################################################################

t_TMD2=0.00
t_hBN1 = 0.035
t_WS2_monolayer = 0.001
t_hBN2 = 0.095
# t_PMMA = 0.600
t_PMMA = 0.0


t_tot=0.0
etha=1
t_TMD1=etha*t_tot
t_WS2_unetched=t_tot-t_TMD1

ax=0.42 #um
FF=0.73
wg=FF*ax #hole size
wh=(1-FF)*ax #groove size
alpha=0.6  #Double period perturbation

N=100

# Plot_refractive_indices(lbda,material) #f9 to plot refractive indices
# %% Spectral range of the starting point    
# N_lambda=300; 
N_lambda=N 
# lbda_min=1240/3
# lbda_max=1240/1.49 

lbda_min=1240/2.2
lbda_max=1240/1.2

# lbda_min=1240/2.48
# lbda_max=1240/1.54
# lbda_max=1240/1.4


# lbda_min=1240/3
# lbda_max=1240/1.25

# lbda_min=1240/2.2
# lbda_max=1240/1.25
         
lbda = np.linspace(lbda_min/1000,lbda_max/1000,N_lambda) 
E=1.23987/lbda
# %% Wave_vector
# N_k=701
N_k=N
k_scan=np.linspace(-6.7,6.7,N_k) #mu-1
ky=0.000 #mu-1
kmax=5.1
# %% Common parameters
N_ord=15 #Choice of the number of orders taken into account during simulation, recommendation: 7 for 1D, 50 for 2D
polar=2 #Polarization of incident wave: 1-> x, 2-> y, 3->L, 4->R, 5->s, 6->p, 7->45°, 8->-45°, 0-> All 6 polarizations (H,V,D,A,L,R) for the Stoke parameter
# %% Layer definition (from top to bottom of the stack): each layer is defined by
    # [THICKNESS, MATERIAL] with 
    # thickness: in um 
    # material: the material is given by its order defined in the list of material definition
layer=[] 
layer.append([0,1])             # Superstrate
#layer.append([t_hBN2,2])
#layer.append([0,2])
# layer.append([t_WS2_monolayer,3])
layer.append([t_hBN1,2])        # Monolayer 
#layer.append([t_TMD1,5])         # Grating
#layer.append([t_WS2_unetched,4])   # unetched WS2
layer.append([t_substrate_2,3]) # Subtrate 2
layer.append([t_substrate_1,4]) # Subtrate 1
# layer.append([t_substrate_0,7]) # Subtrate 0   # Substrate Au/SiO2/Si

layer_sub=[] 
layer_sub.append([0,1])
layer_sub.append([0,2])             # Superstrate
# layer_sub.append([0,5])
# layer_sub.append([0,3])
# layer_sub.append([0,5])             # Monolayer 
# #layer_sub.append([0,3])             # Spacer layer
# layer_sub.append([0,2])             # Grating
layer_sub.append([t_substrate_2,3]) # Subtrate 2
layer_sub.append([t_substrate_1,4]) # Subtrate 1
# layer_sub.append([t_substrate_0,7]) # Subtrate 0  # Substrate Au/SiO2/Si
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

# One period
# pattern=[]
# pattern.append([2,1,1,[0,0],[ax-wg,0],0])  #
# u=[ax,0]
# v=[0,0] 


# Double period with alpha=0
pattern=[]
pattern.append([2,1,1,[wh*(1+alpha)/2,0],[wh*(1+alpha),0],0])
pattern.append([2,1,1,[wh*(1-alpha)/2+ax*(1+alpha),0],[wh*(1-alpha),0],0])
u=[2*ax,0] # Lattices (two unit vectors of the Bravais lattice), defined with u=[u_x,u_y] and v=[v_x,v_y]  NOTE: for 1D grating, the simulation will be calculated with u=(ux,0) and v=(0,0)
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
    ## Incident angles (in degrees)
    theta=np.arcsin(k_inplan/2/pi*lbda)
    theta=np.degrees(theta)    
    remove_lambda=(abs(theta.imag)>0).nonzero()
    theta[remove_lambda]=0 
    ## Run S4 simulation for each wavelength
    lbda,R[:,i_k],T[:,i_k],A[:,i_k]=RCWA_spectrum(lbda,material,layer,pattern,u,v,phi,theta,polar,N_ord)
    lbda,R_sub[:,i_k],T_sub[:,i_k],A_sub[:,i_k]=RCWA_spectrum(lbda,material,layer_sub,pattern,u,v,phi,theta,polar,N_ord)
    E=1.23984/lbda

    A[remove_lambda,i_k]=np.nan
    R[remove_lambda,i_k]=np.nan
    T[remove_lambda,i_k]=np.nan    
    
    A_sub[remove_lambda,i_k]=np.nan
    R_sub[remove_lambda,i_k]=np.nan
    T_sub[remove_lambda,i_k]=np.nan 

# %%
elapsed = time.time() - t
print('elapsed time '+str("%.1f" % elapsed)+'s')

# %% Save DATA
R_data=np.column_stack([lbda, R])
R_data=np.row_stack([np.concatenate([[np.nan],k_scan]), R_data])
A_data=np.column_stack([lbda, A])
A_data=np.row_stack([np.concatenate([[np.nan],k_scan]), A_data])
T_data=np.column_stack([lbda, T])
T_data=np.row_stack([np.concatenate([[np.nan],k_scan]), T_data])

R_sub_data=np.column_stack([lbda, R_sub])
R_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), R_sub_data])
A_sub_data=np.column_stack([lbda, A_sub])
A_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), A_sub_data])
T_sub_data=np.column_stack([lbda, T_sub])
T_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), T_sub_data])

sample_parameters=[ax,t_tot,etha,FF]

# np.savetxt("Preliminary_results\R1_7_1.txt", R_data)
# # np.savetxt("Preliminary_results\A1_7.txt", A_data) 
# # np.savetxt("Preliminary_results\hbn_qbic\T1_5.txt", T_data)   
# np.savetxt("Preliminary_results\R1_sub_7_1.txt", R_sub_data)
# # np.savetxt("Preliminary_results\hbn_qbic\A1_sub_5.txt", A_sub_data) 
# # np.savetxt("Preliminary_results\hbn_qbic\T1_sub_5.txt", T_sub_data) 
# np.savetxt("Preliminary_results\sample_parameters_0.txt", sample_parameters)   
# %% Plot result
signalR=(R-R_sub)/R_sub
# signalR=(signalR-np.min(signalR))/(np.max(signalR)-np.min(signalR))
# signalR=R

signalA=(A-A_sub)/A_sub
signalA=(signalA-np.min(signalA))/(np.max(signalA)-np.min(signalA))
signalA=A

plt.rcParams['font.size'] = '16'

saving_name='t$_{TMD1}=$'+str("%.0f" % np.multiply(1e3,t_TMD1))+'nm t$_{TMD2}=$'+str("%.0f" % np.multiply(1e3,t_TMD2))+'nm t$_{hBN}=$'+str("%.0f" % np.multiply(1e3,t_WS2_unetched))+'nm a='+str("%.0f" % np.multiply(1e3,ax))+'nm FF='+str("%.2f" % FF)
title_name='t$_{TMD1}=$'+str("%.0f" % np.multiply(1e3,t_TMD1))+'nm t$_{TMD2}=$'+str("%.0f" % np.multiply(1e3,t_TMD2))+'nm t$_{hBN}=$'+str("%.0f" % np.multiply(1e3,t_WS2_unetched))+'nm a='+str("%.0f" % np.multiply(1e3,ax))+'nm FF='+str("%.2f" % FF)

results_name=Project_name+" a="+str("%.3f" % ax)+" t$_{PMMA}=$"+str("%.3f" % t_PMMA)+" etha="+str("%.3f" % etha)+" FF="+str("%.3f" % FF)
title_name=Project_name+"\n"+" a="+str("%.3f" % ax)+" t$_{hBN}=$"+str("%.3f" % t_hBN1)+" t$_{slab}=$"+str("%.3f" % t_hBN2)+" FF="+str("%.3f" % FF)

# title_name=Project_name+"\n"+" t$_{Au}$="+str("%.3f" % t_substrate_2)


fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
pcm=axs.pcolor(k_scan,1.240/lbda,signalR,cmap='viridis',clim=(0,1))  
axs.set(xlabel='k$_x$($\mu$m)',xlim=(-kmax,kmax),ylim=(1240/lbda_max, 1240/lbda_min), ylabel='Photon Energy(eV)',title=title_name)
axs.plot(k_scan,1.67*k_scan/k_scan,'w--') 
cbar =fig.colorbar(pcm)
cbar.set_label('Reflectivity contrast') 

# fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
# pcm=axs.pcolor(k_scan,1.240/lbda,signalR,cmap='viridis',norm=LogNorm(vmin=signalR.min()+0.01, vmax=signalR.max()))  #,clim=(0,1)
# axs.set(xlabel='k$_x$($\mu$m)',xlim=(-kmax,kmax),ylim=(1240/lbda_max, 1240/lbda_min), ylabel='Photon Energy(eV)')
# cbar =fig.colorbar(pcm,location='right')
# cbar.set_label('Reflectivity contrast') 



# plt.text(0.66, 0.86, 'Sim', ha='left', va='top', transform=fig.transFigure, fontsize=18,color='#FFFFFF')

# fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
# pcm=axs.pcolor(k_scan,1.240/lbda,A,cmap='turbo',clim=(0,1))
# axs.set(xlabel='k$_x$($\mu$m)',xlim=(-kmax,kmax),ylim=(1240/lbda_max, 1240/lbda_min), ylabel='Photon Energy(eV)')
# # axs.plot(kx,E1,'w--',kx,E2,'w--')
# # axs.plot(kx,EX1,'b--')
# # axs.plot(kx,EX2,'b--')
# # axs.plot(kx,Eup1,'r--',kx,Elo1,'r--')
# # axs.plot(kx,Eup2,'r--',kx,Elo2,'r--')
# cbar =fig.colorbar(pcm,location='right')
# cbar.set_label('Absorption') 

plt.show()