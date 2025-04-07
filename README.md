# FX-BEMS ©
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
 4. ***Ncrit*** (transition criteria) – Refer to Table 1 for recommended fluid transition values.
![Typical Ncrit values and their meanings](https://raw.githubusercontent.com/EygonZhang/FX-BEMS/main/figures/Ncrit%20reference%20table.png)

For detailed instructions, see XFoil input/Readme_XFoil.

## 2. BEM Iteration for Rotation Correction
This code takes the XFoil output (2D CL and CD for each blade element) from Module 1 as input and performs BEM iteration to compute:

 1. Axial induction factor (***a***)
 2. Tangential induction factor (***a'***)

## 3. Tip Loss Factor Setting and Convergence Check
The Prandtl tip loss function model yields a singularity solution at r = R (blade tip). In industrial applications, this result is often assumed to be between 0.25 and 0.5. However, this can lead to convergence issues. This section of the code independently calculates whether the engineer-specified F value produces a convergent result at the blade tip. If convergence fails, the induction factors may diverge (a → 1.000, a' → -1.000).
**Note**: After running this section and selecting an appropriate F value, it is necessary to rerun the code from Section 2.

The complete code includes Modules 3 to 5 for calculating: 
 1. Relative velocity (***Urel***)
 2. Flow angle (***φ***)
 3. Updated CL and CD after blade rotational correction
 4. Tangential force (***F_tan***) and axial force (***F_axial***) results
 5. 
,which supports one-click CSV export functionality. Comparative results plotted against Hassan's study are shown below.
！[Force result comparison with Hassan w/o BEM correction!]([https://github.com/user-attachments/assets/45ce3d64-b671-48f1-9596-fefec45e4287](https://github.com/EygonZhang/FX-BEMS/blob/main/results/Example%20blade_results.png))

Note that our blade design features (1) Linear twist distribution at the root section and (2) No blade thickening (unlike industrial blade designs in Hassan's reference model). This validation confirms that our code can also serve as a reference tool for geometric corrections in industrial blade design/manufacturing and an academic benchmark for BEM theory implementation.



For commercial cooperation of the full version codes or technical support, contact: linda.howe@ntu.edu.sg and clang@ntu.edu.sg

**License**: Custom academic use (patent pending). Commercial applications require a license.

**Citation**: If used in research, kindly cite it as:

[1] Y. Zhang and N. Eddie Yin Kwee, “Fast XFoil-integrated Blade Element Momentum Solver (FX-BEMS)” Apr. 07, 2025 Accessed: Jun. 27, 2025. [Online]. Available: https://github.com/EygonZhang/FX-BEMS (Patent Pending).  
