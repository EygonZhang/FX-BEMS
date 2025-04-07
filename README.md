# FX-BEMS ©
This patented code was created by researchers Yixiao Zhang and Eddie Yin Kwee Ng from Nanyang Technological University (NTU), Singapore. It describes a Python-based integrated system that utilizes an enhanced twist-blade BEM (Blade Element Momentum) algorithm coupled with XFoil to achieve refined modeling of blade forces. The portion of the code includes the following design process modules: 

**FX-BEMS_0**. Dividing the blade into elements;

**FX-BEMS_1**. Inputting XFoil parameters to obtain 2D airfoil data; 

**FX-BEMS_2**. Performing BEM iteration to calculate rotation correction; 

**FX-BEMS_3**. Setting the tip loss factor and conducting convergence checks; 

**FX-BEMS_4**. Relative Velocity & Flow Angle Calculation; 

**FX-BEMS_5**. Blade-Rotation-Corrected CL/CD Update; 

**FX-BEMS_6**. Tangential/Axial Force Computation (with rotational-corrected CL/CD).

This code contains the FX-BEMS_0-FX-BEMS_3 modules only to get the induction factors a and a' under BEM iteration, released as an Educational Version under open-source license for any non-commercial use. For commercial cooperation of the full version codes or technical support, contact: linda.howe@ntu.edu.sg and clang@ntu.edu.sg

**Citation**: If used in research, kindly cite it as:

[1] Zhang, Yixiao, and Ng Eddie Yin Kwee. 2025. Fast XFoil-integrated Blade Element Momentum Solver Abbreviation: FX-BEMS. NTUitive, the Innovation and Enterprise (I&E) Company of Nanyang Technological University, Singapore (NTU Singapore), issued April 7, 2025. https://github.com/EygonZhang/FX-BEMS.git (Patent Pending).  

## Quick Start
### 0. Blade Element Division
This section of the code divides the blade into user-defined elements and outputs the geometric parameters for each element, including:
radius, chord length, and twist angle.
 
### 1. XFoil Parameter Input for 2D Airfoil Data
Since each blade element has a unique shape, the Reynolds number (***Re***) varies significantly (up to ~2x) from the tip to the root. Additionally, the initial angle of attack (***AoA***) changes due to the twist design.

**Steps for Engineers:**
 1. Refer to Section 0 for blade geometry parameters.
 2. Calculate the corresponding Re and twist angle for each element.
 3. Input these values into **XFoil.exe** (see ```XFoil_input/Readme_XFoil``` for details).
 4. ***Ncrit*** (transition criteria) – Refer to Table 1 for recommended fluid transition values.
![Typical Ncrit values and their meanings](https://raw.githubusercontent.com/EygonZhang/FX-BEMS/main/figures/Ncrit%20reference%20table.png)

For detailed instructions, see XFoil input/Readme_XFoil.

### 2. BEM Iteration for Rotation Correction
This code takes the XFoil output (2D CL and CD for each blade element) from Module 1 as input and performs BEM iteration to compute:

 1. Axial induction factor (***a***)
 2. Tangential induction factor (***a'***)

### 3. Tip Loss Factor Setting and Convergence Check
The Prandtl tip loss function model yields a singularity solution at r = R (blade tip). In industrial applications, this result is often assumed to be between 0.25 and 0.5. However, this can lead to convergence issues. This section of the code independently calculates whether the engineer-specified F value produces a convergent result at the blade tip. If convergence fails, the induction factors may diverge (a → 1.000, a' → -1.000).
**Note**: After running this section and selecting an appropriate F value, it is necessary to rerun the code from Section 2.

The complete code includes Part 4 to 6 for calculating: 
 1. Relative velocity (***Urel***)
 2. Flow angle (***φ***)
 3. Updated CL and CD after blade rotational correction
 4. Tangential force (***F_tan***) and axial force (***F_axial***) results

,which supports one-click CSV export functionality. Comparative results plotted against Hassan's study are shown below:
![Force result comparison with Hassan w/o BEM correction!](https://github.com/EygonZhang/FX-BEMS/blob/main/results/Example%20blade_results.png)

Note that our blade design features (1) Linear twist distribution at the root section and (2) No blade thickening (unlike industrial blade designs in Hassan's reference model). This validation confirms that our code can also serve as a reference tool for geometric corrections in industrial blade design/manufacturing and an academic benchmark for BEM theory implementation.




