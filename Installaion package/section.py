

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def section():

    df = pd.read_excel("./Airfoil_Data/airfoil_section.xlsx")
    AOA =df["AOA"].to_numpy(dtype=float)
    CL = df["CL"].to_numpy(dtype=float)
    CD = df["CD"].to_numpy(dtype=float)


    return AOA, CL, CD
