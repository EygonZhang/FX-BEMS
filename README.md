# FX-BEMS^©
This patent describes a Python-based integrated system that utilizes an enhanced twist-blade BEM (Blade Element Momentum) algorithm coupled with XFoil to achieve refined modeling of blade forces. The design process involves: FX-BEMS_0. Dividing the blade into elements; FX-BEMS_1. Inputting XFoil parameters to obtain 2D airfoil data; FX-BEMS_2. Performing BEM iteration to calculate rotation correction; FX-BEMS_3. Setting the tip loss factor and conducting convergence checks

# Quick Start
## 0. Blade Element Division
This section of the code divides the blade into user-defined elements and outputs the geometric parameters for each element, including:
radius, chord length, and twist angle.
 
## 1. XFoil Parameter Input for 2D Airfoil Data
Since each blade element has a unique shape, the Reynolds number (Re) varies significantly (up to ~2x) from the tip to the root. Additionally, the initial angle of attack (AoA) changes due to the twist design.

**Steps for Engineers:**

 1. Refer to Section 0 for blade geometry parameters.
 2. Calculate the corresponding Re and twist angle for each element.
 3. Input these values into **XFoil.exe** (see ```XFoil_input/Readme_XFoil``` for details).
 4. **Ncrit (transition criteria)** – Refer to Table 1 for recommended fluid transition values.

For detailed instructions, see XFoil input/Readme_XFoil.

## 2. BEM Iteration for Rotation Correction
This code takes the XFoil output (2D CL and CD for each blade element) from Section 1 as input and performs BEM iteration to compute:

 1. Axial induction factor (**a**)
 2. Tangential induction factor (**a'**)

## 3. Tip Loss Factor Setting and Convergence Check
The Prandtl tip loss function model yields a singularity solution at r = R (blade tip). In industrial applications, this result is often assumed to be a value between 0.25 and 0.5. However, this can lead to convergence issues. This section of the code independently calculates whether the engineer-specified F value produces a convergent result at the blade tip. If convergence fails, the induction factors may diverge (a → 1.000, a' → -1.000).

**Note**: After running this section and selecting an appropriate F value, it is necessary to rerun the code from Section 2.


For commercial cooperation of the full version codes or technical support, contact: industry@yourcompany.com

**License**: Custom academic use (patent pending). Commercial applications require a license.
**Citation**: If used in research, cite:
Zhang, Y. & Ng, E.Y.K. (2023). FX-BEMS Solver. NTU Singapore. Patent Pending.  
