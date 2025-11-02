

import math
import numpy as np

def prandtl_tip_loss(r, phi, Nb, Radius):

    if abs(np.sin(phi)) < 1e-8:
        return 1.0
    f = (Nb / 2) * (Radius - r) / (r * np.sin(phi))
    if f < 0:
        f = 0.0
    val = np.exp(-f)
    val = max(min(val, 1.0), -1.0)


    return (2 / np.pi) * np.arccos(val)
