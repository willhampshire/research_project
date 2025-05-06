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



cwd = Path.cwd()
fpath = cwd / 'fano_profiles' / 'fitting_results_3.csv'

df = pd.read_csv(fpath, index_col=0)
ic(df)

# df['Gamma'].plot(marker='x')
# plt.ylim([0., 0.04])
# plt.title('Gamma')
# plt.show()
#
# df['E0'].plot(marker='x')
# plt.title('E0')
# plt.show()

# df['Q-factor'].plot(marker='x')
# plt.title('Q-factor')
# plt.show()



# line profile plot




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
print(signalR[:5,:5])
kmax=5
m1 = r'$^{-1}$'
kx0 = r'k$_x$=0'

plt.clf()

# sns.set_theme(style="whitegrid")
sns.set_context("notebook")
fig, ax = plt.subplots(figsize=(7, 5))
plt.rcParams.update({"xtick.bottom": True, "ytick.left": True})

df_reflec_energy_fano = df_reflec_energy.subtract(df_reflec_energy.iloc[:, 0], axis=0)

new_cols = asyms_x_labels
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
plt.title(f"Reflectivity profiles relative to {greek.gamma}=0 at {kx0} in Energy\n{experiment_name_nonperplex}  "
          f"Λ={choose[0] * 1000:.0f}nm t={choose[1] * 1000:.0f}nm FF={choose[2]:.3f}")

# plt.xlim([1.2, 1.7])
# Save and show
image_path_c = project_folder / 'images' / 'Fano_profiles.png'
plt.savefig(image_path_c, dpi=300)
print(f"SAVED IMAGE TO {image_path_c}")

plt.show()



sns.set_context("notebook")
fig, ax = plt.subplots(figsize=(7, 5))
plt.plot(df.index, df['Q-factor'], 'rx')
plt.title(f'Q-factor of fitted Fano resonances against Asymmetry {greek.gamma}')
plt.minorticks_on()
plt.ylim([0, 400])
# plt.xlim([0,0.3])

plt.ylabel(f'E{phys.sub_0}/{greek.Gamma} [arb]')
plt.xlabel(f'Asymmetry {greek.gamma} [arb]')
image_path_d = project_folder / 'images' / 'Fano_profile_Qfactor.png'
plt.savefig(image_path_d, dpi=300)

plt.show()



def inverse(x, a, b, c):
    return a / (x-c) + b

x_data = df.index.to_numpy(dtype=float)
y_data = df['Q-factor'].to_numpy(dtype=float)

params, _ = curve_fit(inverse, x_data, y_data, p0=(1, 0, 0))
x_fit = np.linspace(0., max(x_data), 500)
y_fit = inverse(x_fit, *params)

m1 = r"^{-1}"
sns.set_context("notebook")
fig, ax = plt.subplots(figsize=(7, 5))
plt.plot(x_data, y_data, 'rx', label='Q-factor from Fano fitting')
plt.plot(x_fit, y_fit, 'k--', label=rf'E{phys.sub_0}/{greek.Gamma} = {params[0]:.0f} $\times$ 1/({greek.gamma}+{-params[2]:.2f}) - {-params[1]:.0f}')
plt.ylabel(f'E{phys.sub_0}/{greek.Gamma} [arb]')
plt.xlabel(f'Asymmetry {greek.gamma} [arb]')
plt.title(f'Q-factor of fitted Fano resonances against Asymmetry {greek.gamma}')
plt.xlim([0,0.6])
plt.ylim([0.,400])
plt.legend()
plt.minorticks_on()
plt.tight_layout()

image_path_e = project_folder / 'images' / 'Fano_profile_Qfactor_fitted.png'
plt.savefig(image_path_e, dpi=300)

plt.show()

