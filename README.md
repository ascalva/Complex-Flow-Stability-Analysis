# Capstone 2 Code #
#### Alberto Serrano ####

## Description ##
+ Worked as a Research Assistant for Dr. Michael Cromer in computational fluid dynamics research.
+ Explored the role of shear banding in complex flows using open source tools such as OpenFOAM and RheoTool.
+ Built framework to perform linear stability analysis on 2D complex flows of non-Newtonian fluids, specifically ones described by the Oldroyd-B and VCM equations.
+ Goal was to perturb system and observe if it will reach the same steady state, or a new one.
+ Implemented the algorithm outlined in the Goussis and Pearlstein paper: "Removal of Infinite Eigenvalues in the Generalized Matrix Eigenvalue Problem".


## Abstract ##
It has been shown experimentally that a shear banding flow along a 90 degree microfluidic bend exhibits complex behaviours such as a fluctuating vortex size, which is absent in 2D computational flows. To understand if the complex behavior is only a 3D effect, the 2D stable flow is perturbed sinusoidally in the z-direction and perturbed exponentially in time to determine if there exists an instability. The Oldroyd-B model was used to simulate the flow in a cross slot geometry to simplify the system and benchmark the approach, since it is known both experimentally and computationally that there exists an asymmetric instability along the geometry.

## Pipeline ##
+ Run OpenFOAM simulation
+ Convert VTK data to CSV using ParaView
+ Preprocess data
+ Build coefficient matrices
+ Remove infinite eigenvalues
+ Calculate largest eigenvalues

## Run ##
`python3 run.py [-h] [-f FILE] [-v] [-up]`
