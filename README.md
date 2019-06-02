# Capstone 2 Code #
#### Alberto Serrano ####

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
