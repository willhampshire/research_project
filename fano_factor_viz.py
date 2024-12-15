from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from chars import greek, phys

# Define file paths
cwd = Path(os.getcwd())
fano_profiles = cwd / 'fano_profiles/fano_npy_6D.npy'

# Load data
data = dict(np.load(fano_profiles, allow_pickle=True).item())

# Define period, thickness, and filling
period = '300'
thickness = '100.0'
filling = '0.6'

# Prepare data for the heatmap
heatmap_data = []

# Loop through data
for alpha in data:
    try:
        energy_reflectivity = data[alpha][period][thickness][filling]
    except KeyError:
        print(f"SKIPPING alpha {alpha}")
        continue

    # Extract y-values (first column) and reflectivity (second column)
    y_values = energy_reflectivity[0]  # First column
    reflectivity = energy_reflectivity[1]  # Second column

    # Append the data for the heatmap
    for i in range(len(y_values)):
        heatmap_data.append([float(alpha), y_values[i], reflectivity[i]])

# Convert to DataFrame
df = pd.DataFrame(heatmap_data, columns=['alpha', 'energy', 'reflectivity'])
df['wavelength'] = 1240 / df['energy']

# Pivot the DataFrame for plotting
heatmap_matrix = df.pivot(index="wavelength", columns="alpha", values="reflectivity")

# Create the plot using Matplotlib
plt.figure(figsize=(10, 6))

# Plot the heatmap using pcolormesh
cax = plt.pcolormesh(heatmap_matrix.columns, heatmap_matrix.index, heatmap_matrix, cmap="viridis", shading='auto')

# Add colorbar
cbar = plt.colorbar(cax)
cbar.set_label('Energy Reflectivity')

# Customize the plot
plt.title(f'Map of reflectivity at $k_x=0$ as a function of {greek.alpha}\np={period} t={thickness} ff={filling}')
plt.xlabel(f'Asymmetry {greek.alpha}')
plt.ylabel('Wavelength [nm]')

# Set the y-axis ticks and labels
# plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=10))
# wavelength_ticks = np.linspace(df['wavelength'].min(), df['wavelength'].max(), 10)
wavelength_ticks = np.linspace(500, 1000, 11)
plt.yticks(wavelength_ticks, [f"{tick:.1f}" for tick in wavelength_ticks])

# Set the x-axis ticks
alpha_ticks = np.linspace(df['alpha'].min(), df['alpha'].max(), 5)
plt.xticks(alpha_ticks, [f"{tick:.2f}" for tick in alpha_ticks])

plt.ylim(df['wavelength'].min(), df['wavelength'].max())

# Display the plot
plt.show()
