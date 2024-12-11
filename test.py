import math
import time
from typing import List
from pathlib import Path
import os
import sys
from math import pi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns

from chars import greek, phys # a list of useful unicode chars


cwd = Path(os.getcwd())

signalr_csv = cwd / Path(r'WS2_Grating_Eamonn\Results\WS₂, SiO₂, Si 8 (alpha 0.00)\t=100.0nm Λ=300nm FF=0.50 N=125\data\WS₂, SiO₂, Si 8 (alpha 0.00) - t=100.0nm Λ=300nm FF=0.50 SIGNALR.csv')

signalr_arr = pd.read_csv(signalr_csv, index_col=0)

print(signalr_arr.head())
signalr_arr.info()



N=5

lbda_min = 1240 / 2.2 # y limits
lbda_max = 1240 / 1.2
lbda = np.linspace(lbda_min/1000,lbda_max/1000,N)

max_eV = 2.2
min_eV = 1.2
energy_eV = np.linspace(max_eV, min_eV, N)


print(f"\n\n1.24/LBDA: {1.24/lbda}\nEV: {energy_eV}")