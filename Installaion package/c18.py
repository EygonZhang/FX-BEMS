

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def c18_table(M):


    data_CL = pd.read_excel("./Airfoil_Data/C18_data.xlsx", sheet_name="CL", index_col=0)
    data_CD = pd.read_excel("./Airfoil_Data/C18_data.xlsx", sheet_name="CD", index_col=0)

 
    mach_list = np.array(data_CL.columns, dtype=float)

    M_closest = mach_list[np.argmin(np.abs(mach_list - M))]
    
  
    AOA = data_CL.index.to_numpy(dtype=float)
    CL = data_CL[M_closest].to_numpy(dtype=float)
    CD = data_CD[M_closest].to_numpy(dtype=float)
     


    return AOA, CL, CD
