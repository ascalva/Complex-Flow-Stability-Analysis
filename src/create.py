import numpy as np
import sys

from scipy.sparse import csr_matrix, identity, vstack, hstack, lil_matrix

sys.path.append(".")

from . import OB_equations2 as eqF
from . import boundary_conditions as BC

#
# filename: create.py
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Builds and populates A and B matrix based on the equations provided
#          in the equations file.
#

NEIGHBOR_NUM  = 5
NEIGHBOR_LOC  = ["cen", "up", "down", "left", "right"]
BOUND_NAME    = "bound"
LOAD_INTERVAL = 100
DX            = eqF.DX
DY            = eqF.DY

def get_neighbor_ind(df, indx):

    X_LAB = "Points:0"
    Y_LAB = "Points:1"
    bound = False

    curr  = df.loc[indx]
    x     = curr[X_LAB]
    y     = curr[Y_LAB]

    up    = df[(df[X_LAB] == x)      & (df[Y_LAB] == y - DY)].index.values
    down  = df[(df[X_LAB] == x)      & (df[Y_LAB] == y + DY)].index.values
    left  = df[(df[X_LAB] == x - DX) & (df[Y_LAB] == y)     ].index.values
    right = df[(df[X_LAB] == x + DX) & (df[Y_LAB] == y)     ].index.values

    if len(up)    == 0: up    = [-1]; bound = True
    if len(down)  == 0: down  = [-1]; bound = True
    if len(left)  == 0: left  = [-1]; bound = True
    if len(right) == 0: right = [-1]; bound = True

    return (indx, *up, *down, *left, *right), bound


def get_func_name(eq_name, var_name, description):
    return "{0}_{1}_{2}".format(eq_name, var_name, description)


def boundary_condition_A(df, neighbors, mtrx, eq_name, var_name):
    bound     = get_func_name(eq_name, var_name, BOUND_NAME)
    curr_indx = neighbors[0]

    if hasattr(BC, bound): #and curr_indx != -1:
        mtrx[curr_indx,curr_indx] = getattr(BC, bound)([])


def boundary_condition_B(df, neighbors, mtrx):
    indx            = neighbors[0]
    mtrx[indx,indx] = 0


def evaluate_point(df, neighbors, mtrx, eq_name, var_name):

    # Get attribute names
    attributes = eqF.get_vars()

    # Index of center cell
    curr_indx  = neighbors[0]

    # Iterate over all neighbors (includes center location)
    for neigh in range(0, NEIGHBOR_NUM):

        # Find name of function at current location
        func_name = get_func_name(eq_name, var_name, NEIGHBOR_LOC[neigh])

        # Check if function with calculated name exists
        if hasattr(eqF, func_name): #and neighbors[neigh] != -1:

            # Evaluate matrix at location with found function
            df_indx                 = neighbors[neigh]
            df_row                  = df.loc[df_indx]
            variables               = [df_row[attr] for attr in attributes]
            mtrx[curr_indx,df_indx] = getattr(eqF, func_name)(variables)


def build_coefficient_matrix(df):
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

    # Create top left matrix (mxm) of B matrix, will be an identity where the
    # row is zero at a boundary
    B_ = identity(m, format='lil', dtype=np.cfloat)

    eq_names  = eqF.get_equation_names()
    var_names = eqF.get_component_names()

    # Populate all matrices along their diagonal
    for indx, row in df.iterrows():

        if indx % LOAD_INTERVAL == 0:
            print("{0:.1f}% complete..".format(indx * 100 / df.shape[0]))

        # Get indices of neighboring points
        neighbors, bound = get_neighbor_ind(df, indx)

        # Bound B if at a boundary
        if bound: boundary_condition_B(df, neighbors, B_)

        # At a specific location, calculate the value for each matrix with
        # its respective equation.
        for r_indx in range(eq_n):
            for c_indx in range(eq_n):

                # Get current values (matrix and names of eq and var)
                curr_eq_mtrx  = eq_mtrx[r_indx][c_indx]
                curr_eq_name  = eq_names[r_indx]
                curr_var_name = var_names[c_indx]

                # Evaluate point if not at a wall
                if not bound:
                    evaluate_point(df, neighbors, curr_eq_mtrx, curr_eq_name, curr_var_name)

                # Evaluate point if at a wall
                else:
                    boundary_condition_A(df, neighbors, curr_eq_mtrx, curr_eq_name, curr_var_name)


    # Stack all matrices to form the A matrix, such that the it retains the
    # order provided by the equation matrix, eqs.
    for row in range(eq_n):
        # Horizontally stack each row
        eq_mtrx[row] = hstack(eq_mtrx[row])

    # Vertically stack all rows
    return vstack(eq_mtrx).tocsr(), B_.tocsr()

# def create_matrix_A(df, k):
#     """
#     Generalized function to build A matrix from a set of equations and
#     attributes supplied from the equatins file. Builds a sparse matrix for
#     every equation and combines them all in the order that was given by the
#     get_equations and get_vars functions.
#     """
#
#     # Perform error checking
#     # check_matrix_dims()
#
#     # Initialize variables
#     eq_n    = eqF.get_equation_number()
#     m,_     = df.shape
#     eq_mtrx = []
#
#     # Create all the components of the A matrix (in this case, 4 diagonal
#     # matrices).
#     for row in range(eq_n):
#         mtrx_row = []
#
#         for col in range(eq_n):
#             # Populate row of matrices
#             mtrx_row.append(
#                 lil_matrix((m, m), dtype=np.cfloat)
#             )
#
#         # Add row to eq_mtrx
#         eq_mtrx.append( mtrx_row )
#
#     # Create list of equation functions to utilize during matrix calculations.
#     eqs = eqF.get_equations()
#
#     # Data used from data frame
#     attributes = eqF.get_vars()
#
#     # Populate all matrices along their diagonal
#     for indx, row in df.iterrows():
#
#         # Obtain variables
#         variables = [row[attr] for attr in attributes]
#
#         # At a specific location, calculate the value for each matrix with
#         # its respective equation.
#         for r_indx in range(eq_n):
#             for c_indx in range(eq_n):
#                 eq_mtrx[r_indx][c_indx][indx, indx] = eqs[r_indx][c_indx](variables, k)
#
#     # Set boundary conditions in certain matrix equations
#     eqF.set_bound_conditions(eq_mtrx, m, "A")
#
#     # Stack all matrices to form the A matrix, such that the it retains the
#     # order provided by the equation matrix, eqs.
#     for row in range(eq_n):
#         # Horizontally stack each row
#         eq_mtrx[row] = hstack(eq_mtrx[row])
#
#     # Vertically stack all rows
#     return vstack(eq_mtrx).tocsr()
#
#
# def create_matrix_B(m):
#     """
#     Construct a sparse matrix for B and apply boundary conditions. This will
#     consist of either a zero-matrix or an identity matrix for every matrix
#     equation.
#     TODO: Run more tests to check the correctness of the B-matrix creation
#     """
#
#     # Perform error checking
#     # check_matrix_dims()
#
#     # Initialize variables
#     eq_n    = eqF.get_equation_number()
#     def_val = 1
#
#     # Generate default values for diagonal
#     lhs = [def_val] * eq_n
#
#     # Create list of equation functions to utilize during matrix calculations.
#     eqs = np.array(eqF.get_equations())
#
#     # If there is an extra column (last column) in the equation matrix, utilize
#     # values to form matrix. So if the i-th equation has a 0, then all the
#     # diagonal values for that equation are equal to 0.
#     if (len(eqs.shape) == 2) and (eqs.shape[0] + 1 == eqs.shape[1]):
#         lhs = eqs[:,eq_n]
#
#         if not all(isinstance(elt,int) for elt in lhs):
#             raise ValueError("The last column of the equation matrix must contain only ints..")
#
#     # Initialize B matrix as an identity matrix of type lil, to make sparcity
#     # changes efficient
#     B = identity(eq_n * m, format='lil', dtype=np.cfloat)
#
#     # Adopt values from equation matrix along the diagonal
#     for eq in range(len(lhs)):
#         for elt in range(m * eq, m * eq + m):
#             B[elt,elt] = lhs[eq]
#
#     # Return and convert (to csr) B matrix
#     return B.tocsr()


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
