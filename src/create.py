import numpy as np

from scipy.sparse import csr_matrix, identity, vstack, hstack
from src.equations import get_equation_number, get_equations, get_vars, \
                          set_bound_conditions

#
# filename: create.py
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Builds and populates A and B matrix based on the equations provided
#          in the equations file.
#

def create_matrix_A(df, k = 1):
    """
    Generalized function to build A matrix from a set of equations and
    attributes supplied from the equatins file. Builds a sparse matrix for
    every equation and combines them all in the order that was given by the
    get_equations and get_vars functions.
    """

    # Initialize variables
    eq_n    = get_equation_number()
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
    eqs = get_equations()

    # Data used from data frame
    attributes = get_vars()

    # Populate all matrices along their diagonal
    for indx, row in df.iterrows():

        # Obtain variables
        variables = [row[attr] for attr in attributes]

        # At a specific location, calculate the value for each matrix with
        # its respective equation.
        for r_indx in range(eq_n):
            for c_indx in range(eq_n):
                eq_mtrx[r_indx][c_indx][indx, indx] = eqs[r_indx][c_indx](*variables, k)


    # Set boundary conditions in certain matrix equations
    set_bound_conditions(eq_mtrx, m, "A")

    # Stack all matrices to form the A matrix, such that the it retains the
    # order provided by the equation matrix, eqs.
    for row in range(eq_n):
        # Horizontally stack each row
        eq_mtrx[row] = hstack(eq_mtrx[row])

    # Vertically stack all rows
    return vstack(eq_mtrx)


def create_matrix_B(m):
    """
    Construct a sparse matrix for B and apply boundary conditions. This will
    consist of either a zero-matrix or an identity matrix for every matrix
    equation.
    TODO: STRUCTURE OF B-MATRIX STILL NEEDS TO BE GENERALIZED.
    """
    # Top Corner of B-matrix is the identity matrix
    tc = identity(m, format='csr', dtype=np.cfloat)

    # Apply boundary conditions where the first first element, tc[0,0], is
    # equal to 0.
    set_bound_conditions(tc, m, "B")

    # Create B matrix of zeros, where the top corner B[:m, :m] is the identity
    # matrix.
    return vstack([
        hstack([tc, csr_matrix((m,m))]),
        csr_matrix((m, 2 * m))
    ]).tocsr()


def main():
    """
    TESTING
    """
    import pandas as pd

    filename = "out.csv"
    df = pd.read_csv(filename)
    A,B = create_matrix_ex(df)


if __name__ == "__main__":
    main()
