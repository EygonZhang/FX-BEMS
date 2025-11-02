
import numpy as np
import math
import os
import subprocess
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.optimize import root
from scipy.integrate import quad

from section import section
from pitch_details import get_pitch_inputs
from chord_details import get_chord_inputs
from chord import Main_Chord_Fn
from pitch import Main_Pitch_Fn

def LLT_Solver( Radius, Nb, rpm, r1, N_BEMT, dvisc, rho, M, U_in, Linear_Pitch, Linear_Chord):

 N=15

 if Linear_Pitch == 'True':
        inputs_pitch = get_pitch_inputs()
        pitch_intercept = inputs_pitch["pitch_intercept"]
        pitch_slope = inputs_pitch["pitch_slope"]

 else:
        pitch_intercept = 0
        pitch_slope = 0

 if Linear_Chord == 'True':
        inputs_chord = get_chord_inputs()
        chord_intercept = inputs_chord["chord_intercept"]
        chord_slope = inputs_chord["chord_slope"]

 else:
        chord_intercept = 0
        chord_slope = 0



 visc = dvisc / rho
 w= 2 * 3.14 * rpm / 60

 eps = 1e-8
 theta_max = 10 * np.pi

 xj = np.linspace(r1 , Radius , N + 1) #radial position
 xi = (xj[:-1] + xj[1:]) / 2    #control points
 chord_i=[]
 beta_i=[]
 for b in xi:
   chord_i.append(Main_Chord_Fn( b, Linear_Chord, chord_intercept, chord_slope ))
   beta_i.append(np.radians(Main_Pitch_Fn( b , Linear_Pitch, pitch_intercept, pitch_slope)))

 dxi = xj[1:] - xj[:-1]

 AOA,CL,CD = section()
 AOA=np.radians(AOA)
 cl_interp = interp1d(AOA, CL, kind='cubic',fill_value="extrapolate")
 cd_interp = interp1d(AOA, CD, kind='cubic',fill_value="extrapolate")


 def eqn1(induction_flat):


      vi = induction_flat[:N].copy()
      wi = induction_flat[N:].copy()

      V_ij = np.zeros((N, N))
      W_ij = np.zeros((N, N))

      rbar=xi/Radius
      eta=xj/Radius

      
      for i in range(N):
          for j in range(N):
             ri=rbar[i]

             def v_integrand(theta, j_val):
                integrand = 0
                for n in range(1, Nb + 1):
                    etaj=eta[j_val]
                    theta_prime = theta + 2 * np.pi * (n - 1) / Nb
                    v_adv= (U_in + wi[j_val]) / ( Radius * ( w + ( vi[j_val] / xi[j_val] )) )

                    den = ( (v_adv**2 * theta**2 ) + etaj**2 + ri**2 - 2 * ri * etaj * np.cos(theta_prime) )**1.5
                    num = v_adv * (-etaj * ( np.cos(theta_prime) + theta * np.sin(theta_prime ) + ri))

                    integrand += num / (den+eps)
                return integrand

             def w_integrand(theta, j_val):
                integrand = 0
                for n in range(1, Nb + 1):
                    etaj=eta[j_val]
                    theta_prime = theta + 2 * np.pi * (n - 1) / Nb
                    v_adv=( U_in + wi[j_val] ) / ( Radius * (w + ( vi[j_val] / xi[j_val])) )

                    den = ( (v_adv**2 * theta**2 ) + etaj**2 + ri**2 - 2 * ri * etaj * np.cos(theta_prime) )**1.5
                    num = etaj**2 - ( ri * etaj * np.cos(theta_prime) )

                    integrand += num / (den+eps)
                return integrand


             v_int_start, _ = quad(v_integrand, 0, theta_max, args=(j,))
             w_int_start, _ = quad(w_integrand, 0, theta_max, args=(j,))

             if j==N-1:
               v_int_end, _ = quad(v_integrand, 0, theta_max, args=(j,))
               w_int_end, _ = quad(w_integrand, 0, theta_max, args=(j,)) #its ok if Vi,n-1 is 0
             else:
               v_int_end, _ = quad(v_integrand, 0, theta_max, args=(j+1,))
               w_int_end, _ = quad(w_integrand, 0, theta_max, args=(j+1,))


             V_ij[i, j] = (v_int_end - v_int_start) / (4 * np.pi * Radius)
             W_ij[i, j] = (w_int_end - w_int_start) / (4 * np.pi * Radius)


      def eqn2(Fj):


        vi_new = V_ij @ Fj
        wi_new = W_ij @ Fj

        Vtan = w*xi + vi_new
        Vax = U_in + wi_new

        Wi = np.sqrt( Vtan**2+Vax**2 )
        phi = np.arctan2(Vax, Vtan)

        aoa = phi - beta_i
        Cl = cl_interp(aoa)
        Fj_new = 0.5*Wi*chord_i*Cl

        return Fj-Fj_new

      Fj_initial = np.zeros(N)
      Fsol = root(eqn2, Fj_initial, method='hybr',tol=1e-4)

      Fj_final=Fsol.x

      vi_recal = V_ij @ Fj_final
      wi_recal = W_ij @ Fj_final

      v_eqn = vi_recal - vi
      w_eqn = wi_recal - wi
      
      return np.concatenate([v_eqn, w_eqn])

      
 initial_guess = np.zeros(2 * N)
 vwsol = root(eqn1, initial_guess, method='hybr',tol=1e-4, options={'maxfev': 2000})

 if not vwsol.success:
        print("Outer solver did not converge:", vwsol.message)

 vi_final = vwsol.x[:N]
 wi_final = vwsol.x[N:]

 Vtan_final = w * xi + vi_final
 Vax_final = U_in + wi_final
 Wi_final = np.sqrt( Vtan_final**2+Vax_final**2 )
 phi_final = np.arctan2(Vax_final,Vtan_final)
 aoa_final = phi_final - beta_i
 Cl_final = cl_interp(aoa_final)
 Cd_final = cd_interp(aoa_final)
 Fj_final_final =0.5 * Wi_final * chord_i * Cl_final

 L_i = 0.5 * rho * Wi_final**2 * chord_i * Cl_final
 D_i = 0.5 * rho * Wi_final**2 * chord_i * Cd_final

 dThrust_i = L_i * np.cos(phi_final) + D_i * np.sin(phi_final)
 dTorque_i = (L_i * np.sin(phi_final) - D_i * np.cos(phi_final)) * xi


 Total_Thrust = Nb * np.sum(dThrust_i * dxi)/1000
 Total_Torque = Nb * np.sum(dTorque_i * dxi)/1000
 Total_Power = Total_Torque * w




 results = {
    "tangential induced velocity vi m/s": vi_final,
    "axial induced velocity wi m/s": wi_final,
    "xi": xi,
    "Sectional Circulation (m^2/s) ": Fj_final_final,
    "AOA (Degrees)": np.degrees(aoa_final),
    "Thrust (kN)": Total_Thrust,
    "Torque (kNm)": Total_Torque,
    "Power (kW)": Total_Power }

 return results
