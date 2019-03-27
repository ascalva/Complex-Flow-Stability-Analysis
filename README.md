# Capstone 2 Code #
#### author: Alberto Serrano ####

## Description ##
+ Clean and filter simulation data from either a bend- or crosslot-flow generated from OpenFOAM simulations.
+ Studies the stability of the simulation by perturbing the 2D system in 3D.
+ Generates a sparse, coefficient matrix using SciPy and maps all infinite eigenvalues to non-infinite values using the outlined algorithm in the paper "Removal of Infinite Eigenvalues in the Generalized Matrix Eigenvalue Problem" by D. A. Goussis and A. J. Pearlstein.
+ Generates a Matlab file containing the computed, sparse matrices for every combination of k-values in a specified range.
