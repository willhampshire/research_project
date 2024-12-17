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

N=75


def graph_to_fitted(array: list | float, N: int = N) -> list | float:
    """
    Inverse of the fitted_to_graph function.
    Converts energy values back to pixel coordinates.

    :param array: list or single number (eV values)
    :param N: Square dimension array length (same N as in fitted_to_graph)
    :return: Original pixel coordinates corresponding to input eV values
    """
    max_energy, min_energy = 1.24/2.2, 1.24/1.2
    min_pixel, max_pixel = 0, N
    values = 1.24/array
    pixel = min_pixel + (max_pixel - min_pixel) * (max_energy - values) / (max_energy - min_energy)
    return pixel


def fitted_to_graph(array: list | float, N: int = N) -> list | float:
    """
    Convert pixel coords/positions to eV given 1.2, 2.2 range, with N length square dimension array
    :param array: list or single number
    :return: new list or number
    """
    max_energy, min_energy = 1.24/2.2, 1.24/1.2
    min_pixel, max_pixel = 0, N
    values = max_energy - (array - min_pixel) * (max_energy - min_energy) / (max_pixel - min_pixel)
    return 1.24/values



num = np.array([97, 95, 90, 71])
print(num)
print(fitted_to_graph(num))
print(graph_to_fitted(num))
print()
print(graph_to_fitted(fitted_to_graph(num)))
print(fitted_to_graph(graph_to_fitted(num)))
