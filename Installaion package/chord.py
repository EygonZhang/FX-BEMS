
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def Main_Chord_Fn(radial_pos, Linear_or_Not, Chord_Intercept, Chord_Slope):


  def L_Chord(r, chord_intercept, chord_slope):

   Chord = chord_intercept - r * chord_slope
   return Chord

  def NL_Chord(r):
    file_path = "./Airfoil_Data/Chord_Distribution.xlsx"
    df = pd.read_excel(file_path)
    df.columns = [col.strip().lower() for col in df.columns]

    radial_dist = "radial position"
    chord_dist = "chord distribution"
    radial_array = df[radial_dist].to_numpy()
    chord_array = df[chord_dist].to_numpy()

    chord_interp = interp1d(radial_array,chord_array,kind='cubic',fill_value='extrapolate')
    return chord_interp(r)


  if Linear_or_Not:
    return L_Chord(radial_pos, Chord_Intercept, Chord_Slope)
  else:
    return NL_Chord(radial_pos)
