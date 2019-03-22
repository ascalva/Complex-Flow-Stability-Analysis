import numpy as np
# import importlib

from scipy.sparse import csr_matrix, identity, vstack, hstack, lil_matrix
# from src.error import check_matrix_dims
from src.OB_equations import get_equation_number, get_equations, get_vars, \
                          set_bound_conditions

#
# filename: create.py
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Builds and populates A and B matrix based on the equations provided
#          in the equations file.
#


def create_matrix_A(df, k):
    """
    Generalized function to build A matrix from a set of equations and
    attributes supplied from the equatins file. Builds a sparse matrix for
    every equation and combines them all in the order that was given by the
    get_equations and get_vars functions.
    """

    # Perform error checking
    # check_matrix_dims()

    # Initialize variables
    eq_n    = get_equation_number()
    m,_     = df.shape
    eq_mtrx = []

    # Create all the components of the A matrix (in this case, 4 diagonal
    # matrices).
    for row in range(eq_n):
        mtrx_row = []

        for col in range(eq_n):
            # Populate row of matrices
            mtrx_row.append(
                lil_matrix((m, m), dtype=np.cfloat)
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
                eq_mtrx[r_indx][c_indx][indx, indx] = eqs[r_indx][c_indx](variables, k)

    # Set boundary conditions in certain matrix equations
    set_bound_conditions(eq_mtrx, m, "A")

    # Stack all matrices to form the A matrix, such that the it retains the
    # order provided by the equation matrix, eqs.
    for row in range(eq_n):
        # Horizontally stack each row
        eq_mtrx[row] = hstack(eq_mtrx[row])

    # Vertically stack all rows
    return vstack(eq_mtrx).tocsr()


def create_matrix_B(m):
    """
    Construct a sparse matrix for B and apply boundary conditions. This will
    consist of either a zero-matrix or an identity matrix for every matrix
    equation.
    TODO: Run more tests to check the correctness of the B-matrix creation
    """

    # Perform error checking
    # check_matrix_dims()

    # Initialize variables
    eq_n    = get_equation_number()
    def_val = 1

    # Generate default values for diagonal
    lhs = [def_val] * eq_n

    # Create list of equation functions to utilize during matrix calculations.
    eqs = np.array(get_equations())

    # If there is an extra column (last column) in the equation matrix, utilize
    # values to form matrix. So if the i-th equation has a 0, then all the
    # diagonal values for that equation are equal to 0.
    if (len(eqs.shape) == 2) and (eqs.shape[0] + 1 == eqs.shape[1]):
        lhs = eqs[:,eq_n]

        if not all(isinstance(elt,int) for elt in lhs):
            raise ValueError("The last column of the equation matrix must contain only ints..")

    # Initialize B matrix as an identity matrix of type lil, to make sparcity
    # changes efficient
    B = identity(eq_n * m, format='lil', dtype=np.cfloat)

    # Adopt values from equation matrix along the diagonal
    for eq in range(len(lhs)):
        for elt in range(m * eq, m * eq + m):
            B[elt,elt] = lhs[eq]

    # Return and convert (to csr) B matrix
    return B.tocsr()


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
