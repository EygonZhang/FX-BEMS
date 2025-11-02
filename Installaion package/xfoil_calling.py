
import os
import subprocess

def xf( Re, radial_position, pitch, section_count, w, speed_of_sound, AOAInitial, AOAFinal, AirfoilType, AirfoilValue,xfoil_exe_path):

    AOA_initial_value = AOAInitial
    AOA_final_value =  AOAFinal
    AOA_step = 0.25

    iter_count = 100

    if AirfoilType=='NACA':
     airfoil = f"{AirfoilType}{AirfoilValue}"
    else:
     airfoil = f"{AirfoilValue}"
    

    with open("./input.in", "w") as f:


        if AirfoilType=='NACA':
         f.write(f"{airfoil}\n\n")

        else:
         f.write(f"LOAD ./Airfoil_Data/{airfoil}\n\n")

        f.write("PANE\n")
        f.write("OPER\n")
        f.write(f"Visc {Re}\n")
        f.write(f"m {w * radial_position/speed_of_sound}\n")
        f.write("PACC\n")
        f.write(f"./Airfoil_Data/polar{section_count}.txt \n\n")
        f.write(f"ITER {iter_count}\n")
        f.write(f"ASeq {AOA_initial_value} {AOA_final_value} {AOA_step}\n")
        f.write("\n\n")
        f.write("quit\n")

    #subprocess.call("./xfoil.exe < ./input.in", shell=True)
    with open('./input.in', "r") as input_file:
        try:
            subprocess.run(
                [xfoil_exe_path],  # Use the path from the function argument
                stdin=input_file, 
                shell=False, 
                check=True,
                capture_output=True # Hides the console
            )
        except FileNotFoundError:
            # This error will be shown to the user by the main GUI
            raise FileNotFoundError(f"XFOIL not found. Please check Settings. Path: {xfoil_exe_path}")
        except Exception as e:
            raise RuntimeError(f"XFOIL failed to run. Error: {e}")

  

    return
