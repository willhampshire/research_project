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

data = dict(np.load('/Users/williamhampshire/Desktop/pycharm/research_project/fano_profiles/fano_npy_6D.npy', allow_pickle=True).item())
print(np.ndim(data))

# alpha = '0.00'
period = '300'
thickness = '100.0'
filling = '0.6'


# print(data)

heatmap_data = []

for alpha in data:
    print(alpha)
    try:
        energy_reflectivity = data[alpha][period][thickness][filling]
        print(energy_reflectivity)
    except:
        print(f"SKIPPING alpha {alpha}")
        continue
    print(energy_reflectivity)
    # Assuming you want the first column for the y-values (data[alpha][0])
    y_values = energy_reflectivity[0]  # First column (you may need to adjust depending on your data structure)

    # The energy reflectivity (color intensity) is taken from the second column (data[alpha][1])
    reflectivity = energy_reflectivity[1]  # Second column (adjust based on your data)

    # Append the data in the format [alpha, y_value, reflectivity]
    for i in range(len(y_values)):
        heatmap_data.append([float(alpha), y_values[i], reflectivity[i]])

    # Convert the data to a Pandas DataFrame
df = pd.DataFrame(heatmap_data, columns=['alpha', 'y_value', 'reflectivity'])

# Pivot the DataFrame to create a matrix suitable for a heatmap
heatmap_matrix = df.pivot(index="y_value", columns="alpha", values="reflectivity")


# Plot the heatmap using seaborn
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_matrix, cmap="viridis", cbar_kws={'label': 'Energy Reflectivity'}, annot=False)
plt.title('Heatmap of Energy Reflectivity vs Alpha and Y-Value')
plt.xlabel('Alpha')
plt.ylabel('Y-Value')
plt.show()