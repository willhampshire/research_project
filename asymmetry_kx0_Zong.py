
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

from chars import greek, phys


cwd = Path(os.getcwd())
results_dir = cwd / "WS2_Grating_Eamonn" / "Results"
results_dir.mkdir(exist_ok=True)

project_folder = results_dir / 'ASYM WS₂ Zong Lorentzian, SiO₂, Si [5.3.2] β'
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


# period, thickness, filling
# choose: List[float] = [0.3, 0.01, 0.8]

# choose_str = [f"{s:.4f}" for s in choose]
# print(choose_str)

# alpha_layer = data[choose_str[0]][choose_str[1]][choose_str[2]]
# print(len(alpha_layer))
#
# x_axis_str = list(alpha_layer.keys())
#
# x_axis = [float(val) for val in x_axis_str]
# print(x_axis)
# y_data = np.array([alpha_layer[f'{x}'] for x in x_axis_str]).T
#
#
# df_reflectivity = pd.DataFrame(y_data)
# df_reflectivity.columns = x_axis
# df_reflectivity.index = np.linspace(e_max, e_min, len(df_reflectivity.index))
# print(df_reflectivity.head())

def range_in(start:float, stop:float, step:float) -> List[float]:
    """
    Inclusive range generator
    Output rounded to 6dp
    :return: np.array
    """
    n_points = round(((stop-start)/step),0) +1
    linspace = list(np.linspace(start, stop, int(n_points)))
    return [round(num, 6) for num in linspace]


# periods = range_in(0.15, 0.5, 0.05)
# thicknesses = range_in(0.01, 0.04, 0.01)
# filling = range_in(0.7, 0.9, 0.05)

periods = [0.175]
thicknesses = [0.01]
filling = [0.714]


for p in periods:
    for t in thicknesses:
        for f in filling:

            choose: List[float] = [p,t,f]
            choose_str = [f"{s:.4f}" for s in choose]

            choose_str_1 = 'Energy vs Asym param -'
            choose_str_2 = 'Line profiles eV -'
            choose_str_3 = 'Line profiles wav -'
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
                continue

            # Set index as descending energy
            df_reflectivity.index = np.linspace(1.24/e_max, 1.24/e_min, len(df_reflectivity.index))
            df_reflectivity.sort_index(ascending=False)

            os.makedirs(project_folder / 'asym_heatmap', exist_ok=True)
            df_reflectivity.to_csv(project_folder / 'asym_heatmap' / 'energy_vs_asym_heatmap.csv',
                                   header=True, index=True)


            df_reflec_wave = df_reflectivity.copy()

            df_reflec_energy = df_reflectivity.copy()

            df_reflec_energy.index = 1.24 / df_reflectivity.index.astype(float)
            df_reflec_energy = df_reflec_energy.sort_index(ascending=False)  # Ensure correct order

            df_reflec_wave.columns = df_reflec_wave.columns.astype(float) * 1000
            df_reflec_wave.index = df_reflec_wave.index.astype(float) * 1000
            df_plot = df_reflec_wave

            print(df_plot.head(20))

            energy = df_plot.index
            k_scan = df_plot.columns
            signalR = df_plot.to_numpy()
            print(signalR[:5,:5])
            kmax=5
            m1 = r'$^{-1}$'
            kx0 = r'k$_x$=0'
            title_name = (f"Wavelength vs Asymmetry β at {kx0}, Zong et al. "
                          f"\nreplication  Λ={choose[0]*1000:.0f}nm t={choose[1]*1000:.0f}nm FF={choose[2]:.3f}")

            plt.rcParams['font.size'] = '13'
            fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
            pcm = axs.pcolor(k_scan, energy, signalR, cmap='viridis', clim=(0, 1))
            axs.set(xlabel="Asymmetry β [nm]", # ylim=(500, 700),
                    ylabel='Wavelength [nm]', title=title_name)
            # y_eV = 1.45    # reference line at 1.45eV
            # axs.plot(k_scan,y_eV*k_scan/k_scan,'m--') # reference line at 1.45eV
            cbar = fig.colorbar(pcm, location='right')
            cbar.set_label('Reflectivity contrast')
            plt.minorticks_on()


            # Save and show
            os.makedirs(project_folder / 'images', exist_ok=True)
            image_path = project_folder / 'images' / choose_str_1
            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.show()
            print(f"SAVED IMAGE TO {image_path}")


            new_cols = asyms_x_labels * 1000

            # ic(new_cols)
            energy_or_wavelength_profile = 'wavelength'

            if energy_or_wavelength_profile == 'wavelength':

                print(df_plot.index)

                fig, ax = plt.subplots()
                sns.set_theme(style="whitegrid")
                plt.rcParams.update({"xtick.bottom": True, "ytick.left": True})

                for col in new_cols[::50]:
                    sns.lineplot(ax=ax, data=df_plot, x=df_plot.index, y=col,
                                 label=f"{col:.1f}")

                ax.set_xlabel('Wavelength [nm]')
                ax.set_ylabel('Reflectivity [arb]')

                ax.minorticks_on()
                ax.set_xlim([500, 700])
                # ax.set_ylim([0,1])

                # ax.axvspan(xmin=2.1, xmax=2.2, color='grey', alpha=0.3, label='exciton')

                # Add legend and show the plot
                ax.legend(title='β [nm]', loc='best')
                kx0 = r'k$_x$=0'
                experiment_name_nonperplex = experiment_name.replace(phys.sub_2, r'$_2$')
                plt.title(
                    f"Reflectivity contrast vs Wavelength at {kx0}, Zong et al. replication\nΛ={choose[0]*1000:.0f}nm "
                    f"t={choose[1]*1000:.0f}nm FF={choose[2]:.3f}")
                # Save and show
                image_path_b = project_folder / 'images' / choose_str_3
                plt.savefig(image_path_b, dpi=300)
                print(f"SAVED IMAGE TO {image_path_b}")

                plt.show()

            elif energy_or_wavelength_profile == 'energy':

                # plotting
                fig, ax = plt.subplots()
                sns.set_theme(style="whitegrid")
                plt.rcParams.update({"xtick.bottom": True, "ytick.left": True})

                for col in new_cols[::20]:
                    sns.lineplot(ax=ax, data=df_reflec_energy, x=df_reflec_energy.index, y=col,
                                 label=f"{col:.1f}")

                ax.set_xlabel('Energy [eV]')
                ax.set_ylabel('Reflectivity [arb]')

                ax.minorticks_on()
                # ax.set_xlim([e_min, e_max])
                # ax.set_ylim([0,1])

                ax.axvspan(xmin=2.1, xmax=2.2, color='grey', alpha=0.3, label='exciton')

                # Add legend and show the plot
                ax.legend(title='β', loc='best')
                kx0 = r'k$_x$=0'
                experiment_name_nonperplex = experiment_name.replace(phys.sub_2, r'$_2$')
                plt.title(f"Normal incidence {kx0} line profiles in Energy\n{experiment_name_nonperplex} Λ={choose[0]:.3f} t={choose[1]:.3f} FF={choose[2]:.2f}")
                # Save and show
                image_path_b = project_folder / 'images' / choose_str_2
                plt.savefig(image_path_b, dpi=300)
                print(f"SAVED IMAGE TO {image_path_b}")

                plt.show()


