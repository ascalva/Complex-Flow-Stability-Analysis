import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, identity, vstack, hstack

def save_matrix_to_ml(F, G_B):
    from scipy.io import savemat

    # Save matlab file with sparse matrices for later computation
    savemat("sparse_matrices", {"G_B": G_B, "F": F})


def remove_inf_eigs_sparse(A, B, save_matrix):
    """
    Implements the algo found in GoussisPearlstein_1989. Uses sparse scipy
    matrices so it's memory and time efficient. Saves the sparse matrices
    in a matlab file. Egienvalue function from scipy for sparse matrices
    doesn't have full functionality.
    """

    # Find dimensions of B matrix
    n, m  = B.shape

    # Remove rows with all zero entries
    keep_cols = sorted(set(np.nonzero(B)[0]))
    all_cols  = np.arange(n)
    move_cols = np.where(np.logical_not(np.in1d(all_cols, keep_cols)))[0]

    # Remove rows with all zero entries
    B_    = B[keep_cols,:]
    B     = vstack([B_, B[move_cols,:]])
    A     = vstack([A[keep_cols,:], A[move_cols,:]])

    n_,m_ = B_.shape
    k     = n - n_

    E_k   = identity(k, format='csr')
    E_k    .setdiag(np.random.rand(k))

    H     = A[:n - k,:]
    P     = A[n - k:,:]

    F     = vstack([H, E_k * P])
    G_B   = vstack([-B_, P])

    if save_matrix: save_matrix_to_ml(F, G_B)


def remove_inf_eigs_np(A, B, save_matrix):
    """
    Implements the algo found in GoussisPearlstein_1989. Uses numpy matrices
    so it's not memory efficient, but easy to follow. Returns the eigenvalues
    and eigenvectors found from the generalized eivenvalue problem.

    :param verbose: prints out eigenvalues if True, does nothing otherwise
    """

    n, m  = B.shape
    B_    = B[~np.all(B == 0, axis = 1)]
    n_,m_ = B_.shape
    k     = n - n_

    O_2   = np.zeros((k, m))
    E_k   = np.identity(k) * np.random.rand(k).reshape(k, 1)
    B     = np.vstack([B_, O_2])

    H     = A[:n - k,:]
    P     = A[n - k:,:]

    F     = np.vstack([H, np.dot(E_k, P)])
    G_B   = np.vstack([-B_, P])

    if save_matrix: save_matrix_to_ml(F, G_B)


def remove_inf_eigs(A, B, sparse = True, save_matrix = True):
    if sparse == True:
        remove_inf_eigs_sparse(A, B, save_matrix)

    else:
        remove_inf_eigs_np(A, B, save_matrix)


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
    remove_inf_eigs_sparse(A,B, True)


if __name__ == "__main__":
    main()
