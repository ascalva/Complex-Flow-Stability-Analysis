import numpy as np
# import importlib

from scipy.sparse import csr_matrix, identity, vstack, hstack, lil_matrix
# from src.error import check_matrix_dims
# from src.OB_equations import get_equation_number, get_equations, get_vars, \
#                           set_bound_conditions

import src.OB_equations2 as eqF

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
    eq_n    = eqF.get_equation_number()
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
    eqs = eqF.get_equations()

    # Data used from data frame
    attributes = eqF.get_vars()

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
    eqF.set_bound_conditions(eq_mtrx, m, "A")

    # Stack all matrices to form the A matrix, such that the it retains the
    # order provided by the equation matrix, eqs.
    for row in range(eq_n):
        # Horizontally stack each row
        eq_mtrx[row] = hstack(eq_mtrx[row])

    # Vertically stack all rows
    return vstack(eq_mtrx).tocsr()


def get_neighbor_ind(df, x, y):
    DX = 0.002
    DY = 0.002

    X_LAB = "Points:0"
    Y_LAB = "Points:1"
    curr  = df[(df[X_LAB] == x)      & (df[Y_LAB] == y     )].index.values
    up    = df[(df[X_LAB] == x)      & (df[Y_LAB] == y - DY)].index.values
    down  = df[(df[X_LAB] == x)      & (df[Y_LAB] == y + DY)].index.values
    left  = df[(df[X_LAB] == x - DX) & (df[Y_LAB] == y)     ].index.values
    right = df[(df[X_LAB] == x + DX) & (df[Y_LAB] == y)     ].index.values

    if len(up)    == 0: up    = [-1]#[curr+3]
    if len(down)  == 0: down  = [-1]#[curr-3]
    if len(left)  == 0: left  = [-1]#[curr+3]
    if len(right) == 0: right = [-1]#[curr-3]

    return (*up, *down, *left, *right)


def function_caller(df, indx, mtrx, eq_name, var_name):

    X_LAB = "Points:0"
    Y_LAB = "Points:1"

    # Data used from data frame
    attributes = eqF.get_vars()

    curr       = df.loc[indx]
    neighbors  = get_neighbor_ind(df, curr[X_LAB], curr[Y_LAB])

    curr_name  = str(eq_name) + "_" + str(var_name) + "_cen"
    up_name    = str(eq_name) + "_" + str(var_name) + "_up"
    down_name  = str(eq_name) + "_" + str(var_name) + "_down"
    left_name  = str(eq_name) + "_" + str(var_name) + "_left"
    right_name = str(eq_name) + "_" + str(var_name) + "_right"

    if hasattr(eqF, curr_name):
        df_row             = df.loc[indx]
        variables          = [df_row[attr] for attr in attributes]
        mtrx[indx,indx]    = getattr(eqF, curr_name)(variables)

    if hasattr(eqF, up_name) and neighbors[0] != -1:
        df_indx            = neighbors[0]
        df_row             = df.loc[df_indx]
        variables          = [df_row[attr] for attr in attributes]
        mtrx[indx,df_indx] = getattr(eqF, up_name)(variables)

    if hasattr(eqF, down_name) and neighbors[1] != -1:
        df_indx            = neighbors[1]
        df_row             = df.loc[df_indx]
        variables          = [df_row[attr] for attr in attributes]
        mtrx[indx,df_indx] = getattr(eqF, down_name)(variables)

    if hasattr(eqF, left_name) and neighbors[2] != -1:
        df_indx            = neighbors[2]
        df_row             = df.loc[df_indx]
        variables          = [df_row[attr] for attr in attributes]
        mtrx[indx,df_indx] = getattr(eqF, left_name)(variables)

    if hasattr(eqF, right_name) and neighbors[3] != -1:
        df_indx            = neighbors[3]
        df_row             = df.loc[df_indx]
        variables          = [df_row[attr] for attr in attributes]
        mtrx[indx,df_indx] = getattr(eqF, right_name)(variables)


def create_matrix_A_new(df):
    # Initialize variables
    eq_n    = eqF.get_equation_number()
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
    # eqs = eqF.get_equations()

    eq_names  = eqF.get_equation_names()
    var_names = eqF.get_component_names()

    # Populate all matrices along their diagonal
    for indx, row in df.iterrows():

        if indx % 100 == 0:
            print("{0:.1f}% complete..".format(indx * 100 / df.shape[0]))

        # At a specific location, calculate the value for each matrix with
        # its respective equation.
        for r_indx in range(eq_n):
            for c_indx in range(eq_n):

                function_caller(
                    df,
                    indx,
                    eq_mtrx[r_indx][c_indx],
                    eq_names[r_indx],
                    var_names[c_indx]
                )

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
    eq_n    = eqF.get_equation_number()
    def_val = 1

    # Generate default values for diagonal
    lhs = [def_val] * eq_n

    # Create list of equation functions to utilize during matrix calculations.
    eqs = np.array(eqF.get_equations())

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


def test_neighbor_function():
    """
    TESTING
    """
    import pandas as pd
    import preprocess as p

    filename = "../data/OB_crossslot_symmetric_De0.37.csv"
    df = pd.read_csv(filename)
    df = p.bound(df)
    p.deduplicate(df, up_index=True)

    n = get_neighbor_ind(df, 1.05, 1.05)

    print(n)
    print(df.loc[n[0]])
    print(df.loc[n[1]])
    print(df.loc[n[2]])
    print(df.loc[n[3]])


if __name__ == "__main__":
    test_neighbor_function()
