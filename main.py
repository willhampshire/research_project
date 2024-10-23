import pandas as pd
import seaborn as sns
from pathlib import Path
import os
import matplotlib.pyplot as plt


cwd = Path(os.getcwd())

results_dir = (cwd / "WS2_Grating_Eamonn" / "Results"
               / "WS₂ grating, Au, Si sub - t=70nm a=360nm FF=0.80 N=75" / "data")

fname = results_dir / "WS₂ grating, Au, Si sub - t=70nm a=360nm FF=0.80_R.csv"

data = pd.read_csv(fname, delimiter=',')

plt.figure(figsize=(8, 6))  # Optional: Set the figure size
sns.heatmap(data, cmap='viridis', annot=True)  # annot=True to display the data values in each cell
#plt.title('Viridis Heatmap')
plt.show()