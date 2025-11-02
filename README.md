# FX-BEMS©-v2.0: The GUI-based version
# (Fast XFoil-integrated Blade Element Momentum Solver) 

### Intellectual Property Notice
This plug-in code was developed by researcher **Vaishnavi Gowrishankar** at **Nanyang Technological University (NTU), Singapore**, and is the intellectual property of NTU. Licensing and commercialization are managed by **NTUitive Pte Ltd**, a wholly owned subsidiary of NTU responsible for the protection and licensing of the university's intellectual property. It forms part of a Python-based integrated system that utilizes an enhanced twist-blade Blade Element Momentum (BEM) algorithm coupled with XFoil to enable refined aerodynamic modeling of blade forces. v2.0 also allows an aproximate modelling of blade forces using Lifting Line Theory (LLT).

This v2.0 is released under the NTUitive Dual License Agreement and is made available strictly for non-commercial use, such as academic research, education, or personal learning. **Commercial use, redistribution, or derivative development for commercial purposes** is **not** permitted without prior written permission from NTU via NTUitive.

To inquire about commercial licensing or technical support, please contact:

📧 [vaishnavig2721@gmail.com](mailto:vaishnavig2721@gmail.com) (technical support) | 📧 [linda.howe@ntu.edu.sg](mailto:linda.howe@ntu.edu.sg) (commercial licensing)

**Copyright © 2025 Nanyang Technological University (NTU). All rights reserved. Licensing managed by NTUitive Pte Ltd.**

## Citation
If this code is used in academic work or publications, please cite as:

Vaishnavi G, Zhang, Yixiao, and Ng, Eddie Yin Kwee. 2025. Fast XFoil-integrated Blade Element Momentum Solver (FX-BEMS). Nanyang Technological University (NTU), Singapore. Licensing managed by NTUitive. Issued April 7, 2025. Available at: https://github.com/EygonZhang/FX-BEMS.git

# **BEMT-LLT Solver**

The **BEMT-LLT Solver** is a numerical tool designed for rapid computation of aerodynamic forces and moments of wind and tidal turbines. It supports both **Blade Element Momentum Theory (BEMT)** and **Lifting Line Theory (LLT)**, with the flexibility to modify geometry, flow conditions, and airfoil aerodynamic data with ease. The code comes with an easy to use **GUI**. By making modifications to the source code the analysis tool could potentially become an automated design tool, to help generate geometries that meet the required design conditions. 

**The READ ME Covers:**

* General usage instructions  
* Solver settings and options  
* Error handling guidance  
* Required file format   
* Verification of Code

**Running the code** 
Ensure the .exe file and all folders located in the installation folder are downloaded and located in the same folder.
    
**Computational Time**
* C18/Section file - <1 min
* Xfoil - <5 min
* LLT Solver - <15-20 min

  
**General Instructions** 

**Geometrical Properties Page:**

* Enter all geometric details as asked  
* ***Radius as root:*** The distance from the center (in m) from which the blade starts

**Surrounding Flow Page:**

* Input flow parameters.  
* The default fluid is **water**.  
* ***Inlet Velocity:*** Free-stream velocity of the incoming fluid.

**General Setting:**

| Setting | Description |
| ----- | ----- |
| *Tip Loss* | Enable Prandtl’s tip loss correction |
| *Hub Loss* | Enable hub loss correction |
| *Linear Twist Distribution* | Twist defined as `a - b*r` (r in m, a in degrees, b in deg/m), or upload custom data if ***no*** is chosen |
| *Linear Chord Distribution* | Chord defined as `a - b*r` (r in m, a in meters, b nondimensional), or upload custom data if ***no*** is chosen |
| Airfoil Data Options (Choose one): |  |
| *XFoil Coupling* | Automatically extracts airfoil data from XFoil; recommended when Re/Mach varies significantly along the blade. |
| *C18 Table* | Upload CL and CD tables in Excel format (details below). |
| *0.75R Airfoil Properties* | Uses a single airfoil dataset for the entire blade; best for near-uniform airfoil behavior along the blade. |
| *LLT Coupling (Optional)* | Runs LLT alongside BEMT. Requires an **airfoil section file**. Provides a baseline verification for BEMT. Is not as accurate, provides a reference. |

**BEMT Output Page:**

* Click **Run** to start the solver.  
* Depending on selected options:  
  * You will be prompted to enter linear parameters `a` and `b` for chord and/or pitch distribution.  
  * If using XFoil, specify start and end angle of attack (AOA). Start by setting starting AOA to \-ve values and increase to 0 if convergence issues in Xfoil occur. Ending AOA should be less than or equal to the maximum pitch angle of the blade.
  * The path of xfoil.exe must be pasted when prompted 
* Parameters can be edited before or after running via the ***Back*** button and rerun.

**Error Handling:**

* File and sheet names **must match exactly**, including case sensitivity as given at the end.  
* If XFoil fails to converge try:  
  * Increase starting AOA  
  * Decrease ending AOA  
  * Smooth coordinate data or switch to C18 data/Section data  
* Blade sections that fail to converge will show `0` at that location, values can be approximated in the resultant excel file.  
* Spikes in plots indicate poor local convergence. Increase blade sections to reduce impact.  
* **The message** *RuntimeWarning: divide by zero encountered in scalar divide phi \= np.arctan(((1-a)\*U\_inf)/((1+a\_prime)\*(w\*r)))* **will not affect the results** and is a part of the iteration.

**Required File Formats**

**Xfoil Non-NACA Airfoil File:**

* Must be a `.txt` file containing airfoil coordinates compatible with XFoil.  
* Filename must exactly match the name entered in the GUI (.txt must be entered)

**Chord Distribution File:**

* Filename: `Chord_Distribution.xlsx`  
* Columns:  
   | radial position | chord distribution |  
* Stored in: `Airfoil_Data` folder  
* Radial position denotes the radius in meters along the blade.  
* Chord distribution is the chord length at that radial position in meters  
* Sheet name non-consequential 

**Pitch (or Twist) Distribution File:**

* Filename: `Pitch_Distribution.xlsx`  
* Columns:  
   | radial position | pitch distribution |  
* Stored in: `Airfoil_Data` folder  
* Radial position denotes the radius in meters along the blade.  
* Pitch distribution is the pitch at that radial position in degrees  
* Sheet name non-consequential 

**C18 File:**

* AOA in degrees  
* Filename: `C18_data.xlsx`  
* Sheets: `CL` and `CD`  
* Format:  
   | AOA | 0.001 | 0.01 | 0.1 | ... |  
* Stored in: `Airfoil_Data` folder


**Airfoil Section File:**

* Must be located in the Airfoil\_Data folder  
* Filename: `airfoil_section.xlsx`  
* Columns: `AOA`, `CL`, `CD`  
* Sheet name inconsequential 


## Verification

The solver has been verified against established data, as shown in the plot below [1].

![Verification Plot](https://github.com/VaishnaviG2721/BEM-LLT-Solver/blob/main/Verification/Verification.png)


**References:**
* [1] Grogan, D. M., et al. ‘Design of Composite Tidal Turbine Blades’. Renewable Energy, vol. 57, 2013, pp. 151–162, https://doi.org/10.1016/j.renene.2013.01.021.
 



