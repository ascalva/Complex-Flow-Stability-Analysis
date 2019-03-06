import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, identity, vstack, hstack, issparse

#
# filename: eigs.py
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Prepares the A and B matrices for eigenvalue computation in Matlab.
#          Utilizes the GoussisPearlstein_1989 paper algorithm and permutation
#          matrices.
#

def save_matrix_to_ml(F, G_B):
    """
    Saves F and G_B matrices to matlab file for later eigenvalue computation.
    The sparse form of the matries is preserved to keep the data memory
    efficient.
    """
    from scipy.io import savemat

    savemat("sparse_matrices", {"G_B": G_B, "F": F})


def create_permutation_matrix(B, shift_up):

    # Check if supplied matrix is sparse, if not, make it so.
    if not issparse(B):
        B = csr_matrix(B)

    # Permutation matrix is initialized as an identity matrix.
    # A lil_matrix is used for its flexible indexing
    n, _ = B.shape
    pr   = identity(n, format='lil', dtype=np.cfloat)

    # Invert the list of indecies, or find the indeces of the zero-rows
    all_cols   = np.arange(n)
    shift_down = np.where(np.logical_not(np.in1d(all_cols, shift_up)))[0]

    # Combine both index arrays, which holds the positions of the rows.
    # The values are the old indeces, and their position in the list are
    # their new position in the permutation matrix.
    index = np.append(shift_up, shift_down)

    # Use the array of indeces to permute rows in permutation matrix and
    # convert the matrix to CSR form before return for efficient arithmetic.
    return (pr[index,:]).tocsr()


def remove_inf_eigs(A, B, save_matrix):
    """
    Implements the algo found in GoussisPearlstein_1989. Uses sparse scipy
    matrices so it's memory and time efficient. Saves the sparse matrices
    in a matlab file. Egienvalue function from scipy for sparse matrices
    doesn't have full functionality.
    """

    # Find dimensions of B matrix, disregard second value (# of cols)
    n,_ = B.shape

    # Find non-zero rows, or rows that aren't completely populated by 0's
    shift_up = np.array(np.nonzero(B)[0])
    shift_up = np.unique(shift_up)

    # Find permutation matrix
    pr = create_permutation_matrix(B, shift_up)

    # Permute matrices A and B by multiplying them by pr to move 0-rows in B
    # to the bottom and by the transpose of pr to permute the columns
    # (preserves eigenvalues). The same operations are applied to the A
    # matrix.
    B = pr * B * pr.T
    A = pr * A * pr.T

    # Define k, the number of zero rows in B, used to form the B prime matrix.
    n_    = shift_up.size
    k     = n - n_

    # Initialize a diagonal matrix with random values.
    E_k   = identity(k, format='csr', dtype=np.cfloat)
    E_k    .setdiag(-np.random.rand(k))

    # Split A matrix to form the H and P matrices
    H     = A[:n_,:]
    P     = A[n_:,:]

    # Form the F and (G - B) matrices, which we will take the eigen values of.
    # Doing so results in no infinite eigen values.
    F     = vstack([H, E_k * P])
    G_B   = vstack([-B[:n_,:], P])

    # Save sparse matrices to matlab file for later computation of eigenvalues
    if save_matrix: save_matrix_to_ml(F, G_B)


def init_AB():
    """
    Initialize A and B matrices.
    Currently returns precoded matrices, may change later to a file read.
    Used for testing.
    """
    A = np.array([ 1, 0, 1, 0,
                   0, 1, 0,-1,
                  -1, 0, 0, 1,
                   0,-1, 1, 0]).reshape(4,4)

    B = np.array([ 1, 0, 0, 0,
                   0, 0, 0, 0,
                   0, 0, 1, 0,
                   0, 0, 0, 0]).reshape(4,4)

    return A, B


def main():
    A_ex, B_ex = init_AB()
    A_ex = csr_matrix(A_ex)
    B_ex = csr_matrix(B_ex)
    # remove_inf_eigs_sparse(A,B, True)

    # shift_up   = np.array(np.nonzero(B_ex)[0])
    # create_permutation_matrix(B_ex, shift_up)

    remove_inf_eigs(A_ex, B_ex, False)

if __name__ == "__main__":
    main()
