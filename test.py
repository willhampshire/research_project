import numpy as np
from typing import List


def range_in(start:float, stop:float, step:float) -> List[float]:
    """
    Inclusive range generator
    Output rounded to 6dp
    :return: np.array
    """
    n_points = round(((stop-start)/step),0) +1
    linspace = list(np.linspace(start, stop, int(n_points)))
    return [round(num, 6) for num in linspace]

range = range_in(0.25, 0.60, 0.05)
print(range)
