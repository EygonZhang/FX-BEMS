
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def Main_Pitch_Fn(radial_pos, Linear_or_Not,  Pitch_Intercept, Pitch_Slope):

  def L_Pitch(r, pitch_intercept, pitch_slope):

   Pitch = pitch_intercept- r * pitch_slope
   return Pitch

  def NL_Pitch(rad):

    file_path = "./Airfoil_Data/Pitch_Distribution.xlsx"
    df = pd.read_excel(file_path)
    df.columns = [col.strip().lower() for col in df.columns]

    radial_col = "radial position"
    pitch_col = "pitch distribution"
    radial_array = df[radial_col].to_numpy()
    pitch_array = df[pitch_col].to_numpy()

    pitch_interp = interp1d(radial_array,pitch_array,kind='cubic',fill_value='extrapolate')

    return pitch_interp(rad)



  if Linear_or_Not:
    
    return L_Pitch(radial_pos, Pitch_Intercept, Pitch_Slope)
  else:
    return NL_Pitch(radial_pos)

