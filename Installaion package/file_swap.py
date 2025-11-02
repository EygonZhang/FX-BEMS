
import os
import shutil

from file_split import split

def swap(n):
        if n == 0:
         print("ERROR: XFOIL failed on the first blade element (n=0).")
         print("1. Ensure 'xfoil.exe' is in the same folder as your scripts.")
         print("2. Ensure the 'Airfoil_Data' folder exists.")
         print("3. Check if the input parameters (especially root radius and RPM) are reasonable.")
         
         return [], [], []
        
        polar_n = f"./Airfoil_Data/polar{n}.txt"
        polar_prev = f"./Airfoil_Data/polar{n-1}.txt"

        if os.path.exists(polar_n):
            os.remove(polar_n)

        if os.path.exists(polar_prev):
            shutil.copy(polar_prev, polar_n)

        else:
            print(f"File Swapping Error, Check Convergence")


        AOA, CL, CD = split(n)

        return AOA, CL, CD
