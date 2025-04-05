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

project_name='test'
experiment_summary = f"N: {75}"
cwd = Path(os.getcwd())
results_dir = cwd / "Results"
results_dir.mkdir(exist_ok=True)

experiment_summary_dir = results_dir / project_name
experiment_summary_dir.mkdir(exist_ok=True)

experiment_summary_fname = results_dir / project_name / 'experiment_info.txt'

np.savetxt(experiment_summary_fname, [experiment_summary], fmt='%s', delimiter='\t')
print(experiment_summary_dir)