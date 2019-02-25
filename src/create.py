import numpy as np
import sys
from scipy.sparse import csr_matrix, identity, vstack, hstack
from src import equations


def create_matrix_A(df, k = 1):
    """
    USED FOR TESTING. automated matrix creation
    """

    # Initialize variables
    eq_n    = 2
    m       = df.size
    eq_mtrx = []

    # Create all the components of the A matrix (in this case, 4 diagonal
    # matrices).
    for row in range(eq_n):
        mtrx_row = []

        for col in range(eq_n):
            # Populate row of matrices
            mtrx_row.append(
                identity(m, format='csr', dtype=np.cfloat)
            )

        # Add row to eq_mtrx
        eq_mtrx.append( mtrx_row )

    # Create list of equation functions to utilize during matrix calculations.
    eqs = [
        [equations.ueq_u, equations.ueq_v],
        [equations.veq_u, equations.veq_v]
    ]

    # Data used from data frame
    u_0   = "U:0"
    v_0   = "A:0"

    # Populate all matrices along their diagonal
    for indx, row in df.iterrows():

        # Obtain variables
        u = row[u_0]
        v = row[v_0]

        # At a specific location, calculate the value for each matrix with
        # its respective equation.
        for r_indx in range(eq_n):
            for c_indx in range(eq_n):
                eq_mtrx[r_indx][c_indx][indx, indx] = eqs[r_indx][c_indx](u, v, k)


    # Make the first and last elements of the ueq_v diagonal matrix equal
    # to 0 (boundary conditions).
    eq_mtrx[0][0][0, 0]         = 1.0
    eq_mtrx[0][0][m - 1, m - 1] = 1.0

    eq_mtrx[0][1][0, 0]         = 0.0
    eq_mtrx[0][1][m - 1, m - 1] = 0.0

    # Stack all matrices to form the A matrix, such that the it follows the
    # format:
    #              u         v
    #  U_eqn  [ ueq_u[]   ueq_v[] ]
    #  V_eqn  [ veq_u[]   veq_v[] ]
    #
    for row in range(eq_n):
        # Horizontally stack each row
        eq_mtrx[row] = hstack(eq_mtrx[row])

    # Vertically stack all rows
    return vstack(eq_mtrx)


def create_matrix_B(m):
    """
    Construct a sparse matrix for B and apply boundary conditions
    """
    # Top Corner is the identity matrix with the first first element tc[0,0]
    # equal to 0 (boundary condition).
    tc      = identity(m, format='csr', dtype=np.cfloat)
    tc[0,0] = 0.0
    tc[m - 1, m - 1] = 0.0

    # Create B matrix of zeros, where the top corner B[:m, :m] is the identity
    # matrix.
    return vstack([
        hstack([tc, csr_matrix((m,m))]),
        csr_matrix((m, 2 * m))
    ]).tocsr()
    

def create_matrix_ex(df, k = 1):
    """
    USED FOR TESTING.
    """

    # Create all the components of the A matrix (in this case, 4 diagonal
    # matrices).
    m     = df.size
    ueq_u = identity(m, format='csr', dtype=np.cfloat)
    ueq_v = identity(m, format='csr', dtype=np.cfloat)
    veq_u = identity(m, format='csr', dtype=np.cfloat)
    veq_v = identity(m, format='csr', dtype=np.cfloat)

    # Data used from data frame
    u_0   = "U:0"
    v_0   = "A:0"

    # Populate all matrices along their diagonal
    indx  = 0
    for u, v in zip(df[u_0], df[v_0]):
        ueq_u[indx, indx] = v - k**2
        ueq_v[indx, indx] = u
        veq_u[indx, indx] = - 1j * k
        veq_v[indx, indx] = 2 * v

        indx += 1

    # Make the first and last elements of the ueq_v diagonal matrix equal
    # to 0.
    ueq_u[0, 0]         = 1.0
    ueq_v[0, 0]         = 0.0
    ueq_u[m - 1, m - 1] = 1.0
    ueq_v[m - 1, m - 1] = 0.0

    # Stack all matrices to form the A matrix, such that the it follows the
    # format:
    #              u         v
    #  U_eqn  [ ueq_u[]   ueq_v[] ]
    #  V_eqn  [ veq_u[]   veq_v[] ]
    #
    A_top = hstack([ueq_u, ueq_v])
    A_bot = hstack([veq_u, veq_v])
    A     = vstack([A_top, A_bot]).tocsr()

    # Top Corner is the identity matrix with the first first element tc[0,0]
    # equal to 0.
    tc      = identity(m, format='csr', dtype=np.cfloat)
    tc[0,0] = 0.0
    tc[m - 1, m - 1] = 0.0

    # Create B matrix of zeros, where the top corner B[:m, :m] is the identity
    # matrix.
    B = vstack([
        hstack([tc, csr_matrix((m,m))]),
        csr_matrix((m, 2 * m))
    ]).tocsr()

    return A, B



def main():
    import pandas as pd

    filename = "out.csv"
    df = pd.read_csv(filename)
    A,B = create_matrix_ex(df)


if __name__ == "__main__":
    main()
