
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

project_folder = results_dir / 'ASYM MoS₂, SiO₂, Si [11.9.7] γ e_max=2.2'
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

periods = [0.250]
thicknesses = [0.030]
filling = [0.7]


for p in periods:
    for t in thicknesses:
        for f in filling:

            choose: List[float] = [p,t,f]
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
                continue

            # Set index as descending energy
            df_reflectivity.index = np.linspace(e_max, e_min, len(df_reflectivity.index))
            df_reflectivity.sort_index(ascending=False)

            os.makedirs(project_folder / 'asym_heatmap', exist_ok=True)
            df_reflectivity.to_csv(project_folder / 'asym_heatmap' / 'energy_vs_asym_heatmap.csv',
                                   header=True, index=True)


            df_reflec_wave = df_reflectivity.copy()

            df_reflec_wave.index = 1.24 / df_reflectivity.index
            df_reflec_wave = df_reflec_wave.sort_index(ascending=False)  # Ensure correct order


            # plt.figure(figsize=(10, 8))
            # ax = sns.heatmap(
            #     df_reflectivity, # df_reflec_wave
            #     cmap="viridis",
            #     xticklabels=5,
            #     yticklabels=False,  # Prevent default overlapping
            #     cbar_kws={'label': 'Reflectivity'},
            # )
            #
            # num_ticks = 20
            # yticks = np.linspace(0, len(df_reflectivity) - 1, num_ticks)
            #
            # ytick_labels = np.linspace(df_reflectivity.index.max(), df_reflectivity.index.min(), num_ticks)
            # ytick_labels = [f"{y:.3f}" for y in ytick_labels]  # Format to 2 decimal places
            #
            # ax.set_yticks(yticks)
            # ax.set_yticklabels(ytick_labels)
            #
            #
            # # Labels & title
            # plt.xlabel("Asym")
            # plt.ylabel("Energy [eV]")
            # plt.title(f"Wavelength vs Asym - ax={choose[0]:.2f} t={choose[1]:.2f} ff={choose[2]:.2f}")
            #
            # # Save and show
            # os.makedirs(project_folder / 'images', exist_ok=True)
            # image_path = project_folder / 'images' / choose_str_1
            # plt.savefig(image_path, dpi=300)
            # print(f"SAVED IMAGE TO {image_path}")

            plt.figure(figsize=(10, 8))

            # Plot heatmap using imshow
            im = plt.imshow(
                df_reflectivity.values,
                aspect='auto',
                cmap='viridis',
                interpolation='nearest',
                origin='lower',
            )

            # Colorbar
            cbar = plt.colorbar(im)
            cbar.set_label('Reflectivity')

            # Y-axis ticks
            num_ticks = 21
            yticks = np.linspace(0, len(df_reflectivity) - 1, num_ticks)
            ytick_labels = np.linspace(df_reflectivity.index.max(), df_reflectivity.index.min(), num_ticks)
            ytick_labels = [f"{y:.3f}" for y in ytick_labels]

            plt.yticks(yticks, ytick_labels)
            plt.ylabel("Energy [eV]")

            # X-axis ticks
            plt.xticks(ticks=np.arange(0, len(df_reflectivity.columns), 5), labels=df_reflectivity.columns[::5], rotation=45)
            plt.xlabel("γ [arb]")

            # Title
            plt.title(f"Energy vs γ, {experiment_name}\nΛ={choose[0]:.3f} t={choose[1]:.3f} FF={choose[2]:.2f}")

            # Save and show
            os.makedirs(project_folder / 'images', exist_ok=True)
            image_path = project_folder / 'images' / choose_str_1
            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.show()
            print(f"SAVED IMAGE TO {image_path}")

            plt.show()


            new_cols = asyms_x_labels

            # ic(new_cols)
            energy_or_wavelength_profile = 'energy'

            if energy_or_wavelength_profile == 'wavelength':

                fig, ax = plt.subplots()
                sns.set_theme(style="whitegrid")
                plt.rcParams.update({"xtick.bottom": True, "ytick.left": True})

                for col in new_cols[::10]:
                    sns.lineplot(ax=ax, data=df_reflec_wave, x=df_reflec_wave.index, y=col,
                                 label=f"{col:.3f}")

                ax.set_xlabel('Wavelength [um]')
                ax.set_ylabel('Reflectivity [arb]')

                ax.minorticks_on()
                # ax.set_xlim([0.5, 0.7])
                # ax.set_ylim([0,1])

                # ax.axvspan(xmin=2.1, xmax=2.2, color='grey', alpha=0.3, label='exciton')

                # Add legend and show the plot
                ax.legend()

                plt.title(f"kx=0 line profiles of alpha (key) - {choose} [ax, t, ff]")
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
                    sns.lineplot(ax=ax, data=df_reflectivity, x=df_reflectivity.index, y=col,
                                 label=f"{col:.3f}")

                ax.set_xlabel('Energy [eV]')
                ax.set_ylabel('Reflectivity [arb]')

                ax.minorticks_on()
                ax.set_xlim([e_min, e_max])
                # ax.set_ylim([0,1])

                ax.axvspan(xmin=2.1, xmax=2.2, color='grey', alpha=0.3, label='exciton')

                # Add legend and show the plot
                ax.legend(title='γ', loc='best')
                kx0 = r'k$_x$=0'
                experiment_name_nonperplex = experiment_name.replace(phys.sub_2, r'$_2$')
                plt.title(f"Normal incidence {kx0} line profiles in Energy\n{experiment_name_nonperplex} Λ={choose[0]:.3f} t={choose[1]:.3f} FF={choose[2]:.2f}")
                # Save and show
                image_path_b = project_folder / 'images' / choose_str_2
                plt.savefig(image_path_b, dpi=300)
                print(f"SAVED IMAGE TO {image_path_b}")

                plt.show()


