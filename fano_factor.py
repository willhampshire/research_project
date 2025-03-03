#!/usr/bin/env python
# coding: utf-8


from typing import List
from pathlib import Path
import os
import re
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


class NpyFileManager:
    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def __enter__(self):
        if os.path.exists(self.filename):
            try:
                # Load the dataset
                self.data = np.load(self.filename, allow_pickle=True).item()
                self.data = dict(self.data)
                print(type(self.data), np.shape(self.data))
                print("Data loaded.")
            except:
                print("Data NOT loaded!")
                time.sleep(2)
                self.data: dict = {}
        else:
            # Initialize
            self.data :dict = {}
        return self

    def add_data(self, alpha, period, thickness, filling, energy_reflectivity):
        """
        Add a new dataset to the file.

        Args:
            alpha (float): Value of alpha (1st dimension).
            period (float): Value of period (2nd dimension).
            thickness (float): Value of thickness (3rd dimension).
            filling (float): Value of filling (4th dimension).
            energy_reflectivity (np.ndarray): Array of shape (125, 2), pairing energy and reflectivity.
        """
        if energy_reflectivity.shape != (2, 125):
            raise ValueError("Energy-reflectivity data must have shape (2, 125) - ie N needs to be 125.")

        self.data.setdefault(alpha, {}) \
            .setdefault(period, {}) \
            .setdefault(thickness, {}) \
            .setdefault(filling, energy_reflectivity)


        # Construct a key using the category values
        category_key = (alpha, period, thickness, filling)

        print(category_key, type(self.data))
        # Add the paired data to the dictionary
        self.data[alpha][period][thickness][filling] = energy_reflectivity

    def get_data(self, alpha, period, thickness, filling):
        """
        Retrieve the paired data for specific category values.

        Args:
            alpha (float): Value of alpha.
            period (float): Value of period.
            thickness (float): Value of thickness.
            filling (float): Value of filling.

        Returns:
            np.ndarray or None: The corresponding paired data (125, 2), or None if not found.
        """
        category_key = (alpha, period, thickness, filling)
        return self.data.get(category_key, None)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Save the dataset as a dictionary
        if self.data is not None:
            np.save(self.filename, self.data)



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
        print(files)
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

    N_k = N
    # k_scan=np.linspace(-6.7,6.7,N_k) #mu-1
    kmax = 5
    k_scan = np.linspace(-kmax, kmax, N_k)  # mu-1
    # k_scan = px_kx_convert(np.array(list(df_signalR.columns)), kmax, N_k-1)
    ky = 0.000
    title_name = f'SIGNALR CSV - {results_dir.parents[0].name}'

    fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
    pcm = axs.pcolor(k_scan, energy_eV, signalR, cmap='viridis', clim=(0, 1))
    axs.set(xlabel=f'k$_x$ [{greek.mu}m]',
            xlim=(-kmax, kmax), ylim=(min_eV, max_eV),
            ylabel='Photon Energy [eV]',
            title=title_name)
    # y_eV = 1.45    # reference line at 1.45eV
    # axs.plot(k_scan,y_eV*k_scan/k_scan,'m--') # reference line at 1.45eV
    cbar = fig.colorbar(pcm, location='right')
    cbar.set_label('Reflectivity contrast')
    plt.minorticks_on()
    plt.show()

    # plot line profile at kx=0

    # print(df_signalR.head())

    kx_0_px = int(N / 2)
    if N % 2 == 1:
        print("Odd pixels number")
    line_profile = df_signalR.iloc[:, kx_0_px]

    index_eV = np.linspace(2.2, 1.2, len(line_profile))
    assert len(index_eV) == len(line_profile)

    line_profile.index = index_eV

    # print(line_profile)

    line_profile.plot()

    plt.title(f"Line profile at k$_x$=0 "
              f"[{greek.mu}m{phys.sup_minus}{phys.sup_1}]"
              f"\n{results_dir.parents[0].name}")
    plt.xlabel(f"Energy [eV]")
    plt.ylabel("Reflectivity (normalised)")
    plt.axvline(1.4, color='red', lw=1, linestyle='--', label='1.4 eV')
    plt.axvline(1.6, color='green', lw=1, linestyle='--', label='1.6 eV')
    plt.axvline(1.8, color='blue', lw=1, linestyle='--', label='1.8 eV')

    image_save_path = results_dir.parents[0] / 'images' / 'line_profile.png'
    plt.savefig(image_save_path, dpi=300)
    plt.show()

    return line_profile, results_dir.parents[0].name


def px_kx_convert(values, kmax, Nk, order: int = 0):
    kmin = -kmax
    if order == 0:
        return kmin + (values * (kmax - kmin) / Nk)
    elif order == 1:
        return (values + kmax) * (Nk / (kmax - kmin))
    else:
        return



# N=75

cwd = Path(os.getcwd())

results_top_dir = [cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 9 (alpha 0.00)',
                   cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 9 (alpha 0.10)',
                   cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 9 (alpha 0.20)',
                   cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 9 (alpha 0.30)']

# results_top_dir = [cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 8 (alpha 0.00)']

full_dataset_fname = cwd / 'fano_profiles' / 'fano_npy_6D_sim9.npy' # np file format supports saving 6d array as is


if __name__ == '__main__':
    for result_dir in results_top_dir:
        with NpyFileManager(full_dataset_fname) as full_dataset:
            # print("Numpy file:", full_dataset)
            print(f"Full dataset shape: {np.shape(full_dataset)}")

            exp_name = result_dir.name.rsplit(' (')[0]
            pattern_alpha = r'\(alpha\s+(.*)\)'
            match = re.search(pattern_alpha, result_dir.name)
            if match:
                alpha = match.group(1)
            else:
                print("No value for alpha.")
                time.sleep(2)
                continue

            save_dir = cwd / "fano_profiles"
            save_dir.mkdir(exist_ok=True, parents=True)



            # results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si' / 't=18.0nm Λ=500nm FF=0.84 N=75' / 'data'
            # results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 4' / 't=60.0nm Λ=350nm FF=0.55 N=75' / 'data'
            # results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si' / 't=38.0nm Λ=500nm FF=0.76 N=75' / 'data'
            # results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 4' / 't=20.0nm Λ=550nm FF=0.55 N=75' / 'data'



            sims = sorted(os.listdir(result_dir))
            if 'summary.json' in sims:
                sims.remove('summary.json')
            print(len(sims))

            # sims = [Path(cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 5' / 't=80.0nm Λ=600nm FF=0.78 N=75')]

            for int_loc, sim in enumerate(sims):
                sim = Path(sim)
                # print(sim / 'data')
                results_dir = result_dir / sim / 'data'
                # print(results_dir)
                # print(results_top_dir)
                print(f"***\nSim no. {int_loc}\n***")
                df_line_profile, name_full_str = fit_simulation(results_dir)

                get_details_pattern = r'.*t=([\d.]+)nm.*=([\d.]+)nm.*?FF=([\d.]+)'
                match_details = re.search(get_details_pattern, name_full_str)
                # print(name_full_str, match_details.group(0))
                thickness = float(match_details.group(1))
                period = int(match_details.group(2))
                filling = float(match_details.group(3))

                energy_reflectivity = np.array([df_line_profile.index, df_line_profile.values])

                print(np.shape(energy_reflectivity))
                full_dataset.add_data(str(alpha), str(period), str(thickness), str(filling), energy_reflectivity)

                # time.sleep(10)

