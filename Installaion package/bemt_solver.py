
import numpy as np
import math
import os
import subprocess
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.optimize import root

from airfoil import get_xfoil_inputs
from xfoil_calling import xf
from file_split import split
from file_swap import swap
from c18 import c18_table
from section import section
from pitch_details import get_pitch_inputs
from chord_details import get_chord_inputs
from chord import Main_Chord_Fn
from pitch import Main_Pitch_Fn
from losses import Losses

def BEMT_Solver( Radius, Nb, rpm, r1, N, dvisc, rho, M, U_inf, Linear_Pitch, Linear_Chord, Tip_Loss, Hub_Loss, Xfoil, C18, Section ):


 if Xfoil:
        inputs_xfoil = get_xfoil_inputs()
        AOAInitial = inputs_xfoil["aoa_initial"]
        AOAFinal = inputs_xfoil["aoa_final"]
        AirfoilType = inputs_xfoil["airfoil_type"]
        AirfoilValue = inputs_xfoil["airfoil_value"]
        Xfoil_Path = inputs_xfoil["xfoil_path"]

 if Linear_Pitch:
        inputs_pitch = get_pitch_inputs()
        if inputs_pitch is None:
            print("Pitch input cancelled. Aborting solver.")
        pitch_intercept = inputs_pitch["pitch_intercept"]
        pitch_slope = inputs_pitch["pitch_slope"]

 else:
        pitch_intercept = 0
        pitch_slope = 0

 if Linear_Chord:
        inputs_chord = get_chord_inputs()
        if inputs_chord is None:
            print("Chord input cancelled. Aborting solver.")
        chord_intercept = inputs_chord["chord_intercept"]
        chord_slope = inputs_chord["chord_slope"]

 else:
        chord_intercept = 0
        chord_slope = 0



 Fn_Values=[]
 Ft_Values=[]
 AOA_values=[]
 a_values=[]
 a_prime_values=[]
 radius_values=[]
 p_values=[]
 phi_values=[]
 Cl_values=[]
 Cd_values=[]
 Cn_values=[]
 U_rel_values=[]
 Ct_values=[]
 c_values=[]
 Thrust_values=[]
 Torque_values=[]

 visc = dvisc / rho
 w= 2 * 3.14 * rpm / 60
 dr= ( Radius - r1 ) / N


 r = r1

 for n in range(N):

   

   c = Main_Chord_Fn( r, Linear_Chord, chord_intercept, chord_slope )
   p = np.radians(Main_Pitch_Fn( r, Linear_Pitch, pitch_intercept, pitch_slope))

   s = ( Nb * c ) / ( 2*3.14 * (r) )

   Re =( w * r )* c / visc

   if Xfoil:

     xf( Re, r, p, n, w, M, AOAInitial, AOAFinal, AirfoilType, AirfoilValue, Xfoil_Path)

     AOA, CL, CD = split(n)

     if len(AOA)<= 3:
        AOA, CL, CD = swap(n)

     cl_interp = interp1d(AOA, CL, kind='cubic',fill_value="extrapolate")
     cd_interp = interp1d(AOA, CD, kind='cubic',fill_value="extrapolate")

   elif C18:
     AOA,CL,CD = c18_table(M)
     AOA=np.radians(AOA)
     
     cl_interp = interp1d(AOA, CL, kind='cubic',fill_value="extrapolate")
     cd_interp = interp1d(AOA, CD, kind='cubic',fill_value="extrapolate")

   elif Section:
     AOA,CL,CD = section()
     AOA=np.radians(AOA)
     cl_interp = interp1d(AOA, CL, kind='cubic',fill_value="extrapolate")
     cd_interp = interp1d(AOA, CD, kind='cubic',fill_value="extrapolate")

   else:
    print("Error in Airfoil data type choice")

   a_initial_guess = [0.3,0]

   def equations(induction):

      phi = np.arctan(((1 - induction[0]) * U_inf) / ((1 + induction[1]) * (w * r)))
      aoa = phi - p

      Cl = cl_interp(aoa)
      Cd = cd_interp(aoa)

      Cn = Cl * np.cos(phi) + Cd * np.sin(phi)
      Ct = Cl * np.sin(phi) - Cd * np.cos(phi)

      F= Losses(Tip_Loss, Hub_Loss, r, phi, Nb, Radius, r1)

      a1 = (F * 4 * np.sin(phi) * np.sin(phi)) / (s * Cn)
      a2 = (F * 4 * np.cos(phi) * np.sin(phi)) / (s * Ct)

      if induction[0] < 0.2:
         a3 = 1 / (a1 + 1)
      else:
         
         a3 = 0.5 * (2 + a1 * (1 - 0.4) - np.sqrt(np.maximum(0, (a1 * (1 - 0.4) + 2)**2 + 4 * (a1 * 0.04 - 1))))
      a4 = 1 / (a2 - 1)

      a_eqn = induction[0] - a3
      a_eqn2 = induction[1] - a4

      return [a_eqn, a_eqn2]


   # Solve with root

   sol = root(equations, a_initial_guess, method='hybr')  

   if sol.success:
     a = sol.x[0]
     a_prime = sol.x[1]
   else:
     r=r+dr
     continue

   phi = np.arctan(((1-a)*U_inf)/((1+a_prime)*(w*r)))

   F= Losses(Tip_Loss, Hub_Loss, r, phi, Nb, Radius, r1)

   Cl = cl_interp(phi-p)
   Cd = cd_interp(phi-p)

   Urel= (U_inf*(1-a))/np.sin(phi)


   Cn = Cl*np.cos(phi)+Cd*np.sin(phi)
   Ct = Cl*np.sin(phi)-Cd*np.cos(phi)

   Fn=0.5*rho*Urel*Urel*dr*c*Cn/1000
   Ft=0.5*rho*Urel*Urel*dr*c*Ct/1000

   Fn_Values.append(Fn)
   Ft_Values.append(Ft)
   AOA_values.append(np.degrees(phi-p))
   a_values.append(a)
   a_prime_values.append(a_prime)
   p_values.append(p)
   phi_values.append(phi)
   Cl_values.append(Cl)
   Cd_values.append(Cd)
   Cn_values.append(Cn)
   Ct_values.append(Ct)
   U_rel_values.append(Urel)
   c_values.append(c)
   Thrust_values.append(Fn*Nb)
   Torque_values.append(r*Ft*Nb)
   radius_values.append(r)
   r= r + dr
 Thrust=np.sum(Thrust_values)
 Torque=np.sum(Torque_values)
 Power=Torque*w
 results = {
    "dFn Normal Force (kN)": Fn_Values,
    "dFt Tangential Force (kN)": Ft_Values,
    "AOA_values (Degrees)": AOA_values,
    "a axial induction factor": a_values,
    "a' tangential induction factor": a_prime_values,
    "radius_values": radius_values,
    "phi (Degrees)": np.degrees(phi_values),
    "Cl": Cl_values,
    "Cd": Cd_values,
    "U_rel (m/s)": U_rel_values,
    "Thrust (kN)": Thrust,
    "Torque (kNm)": Torque,
    "Power (kW)": Power
 }

 return results
