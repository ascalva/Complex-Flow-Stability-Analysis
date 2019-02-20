import numpy as np
# import pandas as pd
from scipy.sparse import csr_matrix, identity, vstack, hstack

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
    ueq_v[0, 0]  = 0.0
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

    # Create B matrix of zeros, where the top corner B[:m, :m] is the identity
    # matrix.
    B = vstack([
        hstack([tc, csr_matrix((m,m))]),
        csr_matrix((m, 2 * m))
    ]).tocsr()

    return A, B


def create_matrix_yf(df, k = 1, row_n = 1.0050):
    """
    USED FOR TESTING.
    Creates a matrix based on data at a fixed y-value
    """

    # Create B matrix using df
    df      = df[df["Points:1"] == row_n]
    m       = df.count()[0]
    A       = identity(m, format='csr').asfptype()

    # Populate diagonals using the values of U
    indx    = 0
    for u in df["U:0"]:
        A[indx, indx] = -k**2 * u
        indx += 1

    # Generate A matrix
    B = identity(m, format='csr').asfptype()
    B[0, 0]  = 0.0
    B[m - 1, m - 1] = 0.0
    A[m - 1, m - 1] = 1.0

    return A, B


def main():
    import pandas as pd
    
    filename = "out.csv"
    df = pd.read_csv(filename)
    A,B = create_matrix_ex(df)


if __name__ == "__main__":
    main()
