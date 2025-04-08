# Fast XFoil-embedded - Blade Element Momentum Solver (FX-BEMS©)

### Intellectual Property Notice
This code was developed by researchers **Yixiao Zhang** and **Eddie Yin Kwee Ng** at **Nanyang Technological University (NTU), Singapore**, and is the intellectual property of NTU. Licensing and commercialization are managed by **NTUitive Pte Ltd**, a wholly owned subsidiary of NTU responsible for the protection and licensing of the university's intellectual property. It forms part of a Python-based integrated system that utilizes an enhanced twist-blade Blade Element Momentum (BEM) algorithm coupled with XFoil to enable refined aerodynamic modeling of blade forces.

The current **Educational Version** includes the following modules:
| Module | Functionality |
|--------|--------------|
| `FX-BEMS_0` | Blade discretization |
| `FX-BEMS_1` | XFoil parameters input & 2D airfoil data generation |
| `FX-BEMS_2` | BEM iterative computation of induction factors (***a*** and ***a'***) |
| `FX-BEMS_3` | Tip loss factor inclusion and convergence checking |

> **Proprietary Modules Not Included**:  
> `FX-BEMS_4` to `FX-BEMS_6` (flow angle $φ$ calculation, blade-rotation-corrected $C_L$ and $C_D$, tangential and axial force: $F_t$, $F_a$ computations)

This educational version is released under the **NTUitive Dual License Agreement** and is made available strictly for **non-commercial use**, such as academic research, education, or personal learning. **Commercial use, redistribution, or derivative development for commercial purposes** is not permitted without prior written permission from NTU via NTUitive.

To inquire about commercial licensing or technical support, please contact:

📧 [yixiao002@e.ntu.edu.sg](mailto:yixiao002@e.ntu.edu.sg) (technical support) | 📧 [linda.howe@ntu.edu.sg](mailto:linda.howe@ntu.edu.sg) (commercial licensing)

**Copyright © 2025 Nanyang Technological University (NTU). All rights reserved. Licensing managed by NTUitive Pte Ltd.**

## Citation
If this code is used in academic work or publications, please cite as:

Zhang, Yixiao, and Ng, Eddie Yin Kwee. 2025. Fast XFoil-integrated Blade Element Momentum Solver (FX-BEMS). Nanyang Technological University (NTU), Singapore. Licensing managed by NTUitive. Issued April 7, 2025. Available at: https://github.com/EygonZhang/FX-BEMS.git

## Quick Start
### 0. Blade Element Division
This section of the code divides the blade into user-defined elements and outputs the geometric parameters for each element, including:
radius, chord length, and twist angle.
 
### 1. XFoil Parameter Input for 2D Airfoil Data
Since each blade element has a unique shape, the Reynolds number (***Re***) varies significantly (up to ~2x) from the tip to the root. Additionally, the initial angle of attack (***AoA***) changes due to the twist design.

**Steps for Engineers:**
 1. Refer to Section 0 for blade geometry parameters.
 2. Calculate the corresponding ***Re*** and twist angle ***θ*** for each element.
 3. Input these values into **XFoil.exe** (see ```XFoil_input/Readme_XFoil``` for details).
 4. **$N_{crit}$** (transition criteria) – Refer to Table 1 for recommended fluid transition values.
![Typical Ncrit values and their meanings](https://raw.githubusercontent.com/EygonZhang/FX-BEMS/main/figures/Ncrit%20reference%20table.png)

For detailed instructions, see XFoil input/Readme_XFoil.

### 2.  Performing BEM iteration to get the induction factor ***a*** and ***a'***
This code takes the XFoil output (2D CL and CD for each blade element) from Module 1 as input and performs BEM iteration to compute:

 1. Axial induction factor (***a***)
 2. Tangential induction factor (***a'***)

### 3. Tip Loss Factor Setting and Convergence Check
The Prandtl tip loss function model yields a singularity solution at r = R (blade tip). In industrial applications, this result is often assumed to be between 0.25 and 0.5. However, this can lead to convergence issues. This section of the code independently calculates whether the engineer-specified F value produces a convergent result at the blade tip. If convergence fails, the induction factors may diverge (a → 1.000, a' → -1.000).
**Note**: After running this section and selecting an appropriate F value, it is necessary to rerun the code from Section 2.

The complete code includes Modules 4 to 6 for calculating: 
 1. Relative velocity (***Urel***)
 2. Flow angle (***φ***)
 3. Updated CL and CD after blade rotational correction
 4. Tangential force (***F_tan***) and axial force (***F_axial***) results

,which supports one-click CSV export functionality. Comparative results plotted against Hassan's study are shown below:
![Force result comparison with Hassan w/o BEM correction!](https://github.com/EygonZhang/FX-BEMS/blob/main/results/Example%20blade_results.png)

Note that our blade design features (1) Linear twist distribution at the root section and (2) No blade thickening (unlike industrial blade designs in Hassan's reference model). This validation confirms that our code can also serve as a reference tool for geometric corrections in industrial blade design/manufacturing and an academic benchmark for BEM theory implementation.




