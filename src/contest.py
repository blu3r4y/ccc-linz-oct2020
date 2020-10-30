import numpy as np


def solve(data):
    return str(np.argmin(data["price"]))
