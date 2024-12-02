#!/usr/bin/env python
# coding: utf-8


from typing import List
from pathlib import Path
import os
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import sobel, gaussian_filter
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

from chars import greek, phys



# N=75

cwd = Path(os.getcwd())

results_top_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 7 (alpha 0.30)'

# results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si' / 't=18.0nm Λ=500nm FF=0.84 N=75' / 'data'
# results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 4' / 't=60.0nm Λ=350nm FF=0.55 N=75' / 'data'
# results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si' / 't=38.0nm Λ=500nm FF=0.76 N=75' / 'data'
# results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 4' / 't=20.0nm Λ=550nm FF=0.55 N=75' / 'data'


savepath = cwd / 'mode_fitting'
savepath.mkdir(exist_ok=True, parents=True)



sims = sorted(os.listdir(results_top_dir))
if 'summary.json' in sims:
    sims.remove('summary.json')
print(len(sims))

# sims = [Path(cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 5' / 't=80.0nm Λ=600nm FF=0.78 N=75')]

def fit_simulation(results_dir):
    try:
        files = sorted(os.listdir(results_dir))
    except:
        return 0
    # file_R = results_dir / files[4]
    # file_R_sub = results_dir / files[5]
    # print(file_R)

    try:
        N_str = str(results_dir.parents[0]).rsplit('N=')[1]
        N = int(N_str)
    except Exception as e:
        print(f"No N present in file name - {e}")

    if not files[2].endswith('SIGNALR.csv'):
        print("Error, wrong file")
        return 0

    signalR_file = results_dir / files[2]
    df_signalR = pd.read_csv(signalR_file, header=None)
    # df_signalR.reset_index(drop=False, inplace=True)
    signalR = df_signalR.to_numpy()

    # signalR = (signalR - np.min(signalR)) / (np.max(signalR) - np.min(signalR))




    max_eV = 2.2
    min_eV = 1.2
    energy_eV = np.linspace(max_eV, min_eV, N)  # Generate wavelengths in micrometers

    N_k=N
    # k_scan=np.linspace(-6.7,6.7,N_k) #mu-1
    kmax=5
    k_scan=np.linspace(-kmax,kmax,N_k) #mu-1
    # k_scan = px_kx_convert(np.array(list(df_signalR.columns)), kmax, N_k-1)
    ky=0.000
    title_name = 'SIGNALR CSV'

    fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
    pcm = axs.pcolor(k_scan,energy_eV,signalR,cmap='viridis',clim=(0,1))
    axs.set(xlabel=f'k$_x$ [{greek.mu}m]',
            xlim=(-kmax,kmax),ylim=(min_eV, max_eV),
            ylabel='Photon Energy [eV]',
            title=title_name)
    # y_eV = 1.45    # reference line at 1.45eV
    # axs.plot(k_scan,y_eV*k_scan/k_scan,'m--') # reference line at 1.45eV
    cbar =fig.colorbar(pcm,location='right')
    cbar.set_label('Reflectivity contrast')
    plt.minorticks_on()
    plt.show()

    # plot line profile at kx=0

    print(df_signalR.head())

    kx_0_px = int(N/2) + 50
    if N % 2 == 1:
        print("Odd pixels number")
    line_profile = df_signalR.iloc[:, kx_0_px]
    line_profile.plot()
    plt.show()





def px_kx_convert(values, kmax, Nk, order:int=0):
    kmin = -kmax
    if order == 0:
        return kmin + (values * (kmax-kmin) / Nk)
    elif order == 1:
        return (values+kmax) * (Nk/(kmax-kmin))
    else:
        return










for int_loc, sim in enumerate(sims):
    sim = Path(sim)
    # print(sim / 'data')
    results_dir = results_top_dir / sim / 'data'
    # print(results_dir)
    # print(results_top_dir)
    print(f"***\nSim no. {int_loc}\n***")
    fit_simulation(results_dir)





