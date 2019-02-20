import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, identity, vstack, hstack

#
# filename: ing_eig.py
#
# @author: Alberto Serrano (axs4986)
#
# description: Algorithm implementation of GoussisPearlstein_1989 paper
#              using sparse matrices from scipy
#
# run: python3 inf_eig
#

# def init_AB():
#     """
#     Initialize A and B matrices.
#     Currently returns precoded matrices, may change later to a file read.
#     """
#     A = np.array([ 1, 0, 1, 0,
#                    0, 1, 0,-1,
#                   -1, 0, 0, 1,
#                    0,-1, 1, 0]).reshape(4,4)
#
#     B = np.array([ 1, 0, 0, 0,
#                    0, 0, 0, 0,
#                    0, 0, 1, 0,
#                    0, 0, 0, 0]).reshape(4,4)
#
#     return A, B


# def create_matrix_ex(df, k = 1):
#
#     # Create all the components of the A matrix (in this case, 4 diagonal
#     # matrices).
#     m     = df.size
#     ueq_u = identity(m, format='csr', dtype=np.cfloat)
#     ueq_v = identity(m, format='csr', dtype=np.cfloat)
#     veq_u = identity(m, format='csr', dtype=np.cfloat)
#     veq_v = identity(m, format='csr', dtype=np.cfloat)
#
#     # Data used from data frame
#     u_0   = "U:0"
#     v_0   = "A:0"
#
#     # Populate all matrices along their diagonal
#     indx  = 0
#     for u, v in zip(df[u_0], df[v_0]):
#         ueq_u[indx, indx] = v - k**2
#         ueq_v[indx, indx] = u
#         veq_u[indx, indx] = - 1j * k
#         veq_v[indx, indx] = 2 * v
#
#         indx += 1
#
#     # Make the first and last elements of the ueq_v diagonal matrix equal
#     # to 0.
#     ueq_v[0, 0]  = 0.0
#     ueq_v[m - 1, m - 1] = 0.0
#
#     # Stack all matrices to form the A matrix, such that the it follows the
#     # format:
#     #             u         v
#     # U_eqn  [ ueq_u[]   ueq_v[] ]
#     # V_eqn  [ veq_u[]   veq_v[] ]
#     #
#     A_top = hstack([ueq_u, ueq_v])
#     A_bot = hstack([veq_u, veq_v])
#     A     = vstack([A_top, A_bot]).tocsr()
#
#     # Top Corner is the identity matrix with the first first element tc[0,0]
#     # equal to 0.
#     tc      = identity(m, format='csr', dtype=np.cfloat)
#     tc[0,0] = 0.0
#
#     # Create B matrix of zeros, where the top corner B[:m, :m] is the identity
#     # matrix.
#     B = vstack([
#         hstack([tc, csr_matrix((m,m))]),
#         csr_matrix((m, 2 * m))
#     ]).tocsr()
#
#     return A, B
#
#
# def create_matrix(df, k = 1):
#
#     # Create B matrix using df
#     row_n   = 1.0050
#     df      = df[df["Points:1"] == row_n]
#     m       = df.count()[0]
#     A       = identity(m, format='csr').asfptype()
#
#     # Populate diagonals using the values of U
#     indx    = 0
#     for u in df["U:0"]:
#         A[indx, indx] = -k**2 * u
#         indx += 1
#
#     # Generate A matrix
#     B = identity(m, format='csr').asfptype()
#     B[0, 0]  = 0.0
#     B[m - 1, m - 1] = 0.0
#     A[m - 1, m - 1] = 1.0
#
#     return A, B


# def remove_inf_eigs_sparse(A, B, save_matrix = True):
#     """
#     Implements the algo found in GoussisPearlstein_1989. Uses sparse scipy
#     matrices so it's memory and time efficient. Saves the sparse matrices
#     in a matlab file. Egienvalue function from scipy for sparse matrices
#     doesn't have full functionality.
#     """
#     from scipy.io import savemat
#
#     # Find dimensions of B matrix
#     n, m  = B.shape
#
#     # Remove rows with all zero entries
#     keep_cols = sorted(set(np.nonzero(B)[0]))
#     all_cols  = np.arange(n)
#     move_cols = np.where(np.logical_not(np.in1d(all_cols, keep_cols)))[0]
#
#     # Remove rows with all zero entries
#     B_    = B[keep_cols,:]
#     B     = vstack([B_, B[move_cols,:]])
#     A     = vstack([A[keep_cols,:], A[move_cols,:]])
#
#     n_,m_ = B_.shape
#     k     = n - n_
#
#     E_k   = identity(k, format='csr')
#     E_k    .setdiag(np.random.rand(k))
#
#     H     = A[:n - k,:]
#     P     = A[n - k:,:]
#
#     F     = vstack([H, E_k * P])
#     G_B   = vstack([-B_, P])
#
#     if save_matrix == True:
#         # Save matlab file with sparse matrices for later computation
#         savemat("sparse_matrices", {"G_B": G_B, "F": F})


def main():
    filename = "out.csv"
    df = pd.read_csv(filename)
    A,B = create_matrix_ex(df)
    remove_inf_eigs_sparse(A,B)


if __name__ == "__main__":
    main()
