

import numpy as np
import math


def split(n):
 with open(f'./Airfoil_Data/polar{n}.txt', 'r') as fil:
      lines = fil.readlines()

 AA=lines[12:]

 AOA=[]
 CL=[]
 CD=[]

 for j in range(len(AA)):
       pp = AA[j].split()
       AOA.append(np.radians(float(pp[0])))
       CL.append(float(pp[1]))
       CD.append(float(pp[2]))

 AOA=np.asarray(AOA)
 CL=np.asarray(CL)
 CD=np.asarray(CD)

 return AOA,CL,CD
