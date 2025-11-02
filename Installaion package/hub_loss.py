
import math
import numpy as np

def hub_loss(r, phi, Nb, r1):

    if abs(np.sin(phi)) < 1e-8:
        return 1.0
    f = (Nb / 2) * (r-r1) / (r1 * np.sin(phi))
    if f < 0:
        f = 0.0
    val = np.exp(-f)
    val = max(min(val, 1.0), -1.0)


    return (2 / np.pi) * np.arccos(val)
