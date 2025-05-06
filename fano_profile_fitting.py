
from pathlib import Path
import os
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List
from icecream import ic
import time
from scipy.optimize import curve_fit

from chars import greek, phys


fitting_eV_max = 1.5


cwd = Path(os.getcwd())
results_dir = cwd / "WS2_Grating_Eamonn" / "Results"
results_dir.mkdir(exist_ok=True)

project_folder = results_dir / 'ASYM MoS₂, SiO₂, Si [11.9.8] γ e_max=1.7'
json_path = project_folder / 'summary_asym.json'
meta_json_path = project_folder / 'summary_asym_meta.json'

with open(json_path, 'r') as file:
    data = json.load(file)

with open(meta_json_path, 'r') as file:
    metadata = json.load(file)

print(metadata)
time.sleep(1)

# time.sleep(20)

e_max = float(metadata['e_max'])
e_min = float(metadata['e_min'])
asyms_x_labels = np.array(metadata['asyms'], dtype=float)
min_detail = float(metadata['min_detail'])
experiment_name = metadata['experiment_name']


data_df = pd.DataFrame(data)
print(data_df.head())
data_df.info()


choose: List[float] = [0.25,0.03,0.7]
choose_str = [f"{s:.4f}" for s in choose]

choose_str_1 = 'Energy vs Asym param -'
choose_str_2 = 'Line profiles eV -'
choose_str_3 = 'Line profiles um -'
for s in choose:
    choose_str_1 += f' {s}'
    choose_str_2 += f' {s}'
    choose_str_3 += f' {s}'

choose_str_1 += '.png'
choose_str_2 += '.png'
choose_str_3 += '.png'

# Extract data
alpha_layer = data[choose_str[0]][choose_str[1]][choose_str[2]]
x_axis_str = list(alpha_layer.keys())
x_axis = [float(val) for val in x_axis_str]

# Create DataFrame
try:
    y_data = np.array([alpha_layer[f'{x}'] for x in x_axis_str]).T
    df_reflectivity = pd.DataFrame(y_data, columns=x_axis)
except:
    print(f"No data found for {choose_str}")


# Set index as descending energy
df_reflectivity.index = np.linspace(1.24/e_max, 1.24/e_min, len(df_reflectivity.index))
df_reflectivity.sort_index(ascending=False)

os.makedirs(project_folder / 'asym_heatmap', exist_ok=True)
df_reflectivity.to_csv(project_folder / 'asym_heatmap' / 'energy_vs_asym_heatmap.csv',
                       header=True, index=True)


df_reflec_wave = df_reflectivity.copy()

df_reflec_energy = df_reflectivity.copy()

df_reflec_energy.index = 1.24 / df_reflectivity.index
df_reflec_energy = df_reflec_energy.sort_index(ascending=False)  # Ensure correct order


energy = df_reflec_energy.index
k_scan = df_reflec_energy.columns
signalR = df_reflec_energy.to_numpy()
# print(signalR[:5,:5])
# kmax=5
# m1 = r'$^{-1}$'
# kx0 = r'k$_x$=0'
# title_name = (f"Energy vs Asymmetry γ at {kx0}\n{experiment_name}  "
#               f"Λ={choose[0]*1000:.0f}nm t={choose[1]*1000:.0f}nm FF={choose[2]:.3f}")
#
# plt.rcParams['font.size'] = '13'
# fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
# pcm = axs.pcolor(k_scan, energy, signalR, cmap='viridis', clim=(0, 1))
# axs.set(xlabel="Asymmetry γ [arb]", ylim=(e_min, e_max),
#         ylabel='Photon Energy [eV]', title=title_name)
# # y_eV = 1.45    # reference line at 1.45eV
# # axs.plot(k_scan,y_eV*k_scan/k_scan,'m--') # reference line at 1.45eV
# cbar = fig.colorbar(pcm, location='right')
# cbar.set_label('Reflectivity contrast')
# plt.minorticks_on()
# # plt.ylim([1.2,1.7])
#
# # Save and show
# os.makedirs(project_folder / 'images', exist_ok=True)
# image_path = project_folder / 'images' / choose_str_1
# plt.tight_layout()
#
# plt.savefig(image_path, dpi=300)
# plt.show()
# print(f"SAVED IMAGE TO {image_path}")


new_cols = asyms_x_labels



fig, ax = plt.subplots()
sns.set_theme(style="whitegrid")
plt.rcParams.update({"xtick.bottom": True, "ytick.left": True})

df_reflec_energy_fano = df_reflec_energy.subtract(df_reflec_energy.iloc[:, 0], axis=0)

for col in new_cols[::40]:
    sns.lineplot(ax=ax, data=df_reflec_energy_fano, x=df_reflec_energy_fano.index, y=col,
                 label=f"{col:.2f}")

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [arb]')

ax.minorticks_on()
ax.set_xlim([e_min, e_max])
# ax.set_ylim([0,1])

# ax.axvspan(xmin=2.1, xmax=2.2, color='grey', alpha=0.3, label='exciton')

# Add legend and show the plot
ax.legend(title='γ', loc='best')
kx0 = r'k$_x$=0'
experiment_name_nonperplex = experiment_name.replace(phys.sub_2, r'$_2$')
plt.title(f"Fano shape reflectance interference at {kx0} in Energy\n{experiment_name_nonperplex}  "
          f"Λ={choose[0] * 1000:.0f}nm t={choose[1] * 1000:.0f}nm FF={choose[2]:.3f}")

# plt.xlim([1.2, 1.7])
# Save and show
image_path_c = project_folder / 'images' / 'Fano_profiles.png'
plt.savefig(image_path_c, dpi=300)
print(f"SAVED IMAGE TO {image_path_c}")

plt.show()



def fanoreflectance_energy(E:float, A:float, q:float, E0:float, Gamma:float, offset) -> float:
    """
    Fano shape reflectance fitting function. Assumes R0=0, ie lines are interference bright - dark.
    :param E: energy (x axis)
    :param A: amplitude
    :param q: Fano asymmetry
    :param E0: resonant energy
    :param Gamma: FWHM
    :return: float
    """

    ep = (2*(E-E0)) / Gamma

    return A*( ( (q + ep)**2 ) / (1 + ep**2) ) + offset

def px_to_energy(data, px_range, e_min, e_max):
    data = np.array(data)

    e_range = e_max - e_min
    scale = e_range / px_range # 1/400 for N=200 px, 1.7-1.2eV
    print(f"Scale: {scale:.4f}")

    return (data * scale) + e_min


def energy_to_px(data, px_range, e_min, e_max):
    data = np.array(data)

    e_range = e_max - e_min
    return (data - e_min) * (px_range/e_range)


px_range = len(df_reflec_energy_fano.index)
print(f"Px range: {px_range}")

df_fano_reduced = df_reflec_energy_fano.iloc[:, ::10].copy()
filtered_cols = [col for col in df_fano_reduced.columns if 0.0 < float(col) < 0.6]
filtered_rows = [row for row in df_fano_reduced.index if 1.2 < float(row) < 1.5]

df_fano_reduced = df_fano_reduced.loc[filtered_rows, filtered_cols]

print(df_fano_reduced.head())

guess = [0.1, -2, 1.3, 0.005, 0.] # A, q, E0, Gamma, offset
bounds = ([0., -3, 1.25, 0., -2.],
          [10., 0, 1.5, 0.1, 3.])
guess_loose = [0.1, -3, 1.4, 0.1, 0.]
bounds_loose = ([0., -10, 1., 0., -5.],
          [10., 0., 2., 2., 10.])


fitting_results = pd.DataFrame()
fitting_results.index = ['A', 'q', 'E0', 'Gamma', 'y_offset', 'R_squared']

print(df_fano_reduced.columns)

for col in df_fano_reduced.columns:
    time.sleep(1)
    try:
        ydata = np.array(df_fano_reduced[col])
        xdata = df_fano_reduced.index
        popt, pcov = curve_fit(f=fanoreflectance_energy, xdata=xdata, ydata=ydata,
                               p0=guess, bounds=bounds, maxfev=10000)

        x_plotting = np.linspace(1.2, fitting_eV_max, px_range)

        y_fitted = fanoreflectance_energy(x_plotting, *popt)
        plt.plot(x_plotting, y_fitted, 'b--', linewidth=2, label='Fano')
        plt.plot(xdata, ydata, 'rx', label=f'Raw, {col}')
        plt.plot(x_plotting, fanoreflectance_energy(x_plotting, *guess), 'k:', label='Guess')
        plt.plot(x_plotting, fanoreflectance_energy(x_plotting, *guess_loose), 'k:', label='Guess 2')
        plt.legend()
        plt.show()

        popt_series = pd.Series(popt)
        popt_series.index = ['A', 'q', 'E0', 'Gamma', 'y_offset']

        # Calculate fitted values and residuals
        y_fit = fanoreflectance_energy(xdata, *popt)
        residuals = ydata - y_fit
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        popt_series['R_squared'] = r_squared
        print(f"Col {col} popt: \n{popt_series}")

        if r_squared < 0.6:
            raise Exception

        fitting_results[col] = popt_series

        time.sleep(1)
    except RuntimeError:
        print("MAXFEV reached - no fit.")
        continue
    except Exception as e:
        print(e)
        try:
            print(f"{col} NOT fitted - trying again with no bounds")

            popt, pcov = curve_fit(f=fanoreflectance_energy, xdata=xdata, ydata=ydata,
                                   p0=guess_loose, bounds=bounds_loose, maxfev=10000)

            x_plotting = np.linspace(1.2, fitting_eV_max, px_range)

            y_fitted = fanoreflectance_energy(x_plotting, *popt)
            plt.plot(x_plotting, y_fitted, 'b--', linewidth=2, label='Fano')
            plt.plot(xdata, ydata, 'rx', label=f'Raw, {col}')
            plt.plot(x_plotting, fanoreflectance_energy(x_plotting, *guess_loose), 'k:', label='Guess')
            plt.legend()
            plt.show()

            popt_series = pd.Series(popt)
            popt_series.index = ['A', 'q', 'E0', 'Gamma', 'y_offset']

            # Calculate fitted values and residuals
            y_fit = fanoreflectance_energy(xdata, *popt)
            residuals = ydata - y_fit
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            popt_series['R_squared'] = r_squared
            print(f"Col {col} popt: \n{popt_series}")

            if r_squared > 0.6:
                fitting_results[col] = popt_series
        except Exception as e:
            print(f"{e}\nCannot fit")

        continue


fitting_results_processed = fitting_results.T
fitting_results_processed['Q-factor'] = fitting_results_processed['E0']/fitting_results_processed['Gamma']
print(fitting_results_processed)

cwd = Path.cwd()
save_name = cwd / 'fano_profiles' / 'fitting_results_3.csv'

fitting_results_processed.to_csv(save_name, sep=',', header=True)
