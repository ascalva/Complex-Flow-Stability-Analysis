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
X_LAB         = eqF.COORD[0]
Y_LAB         = eqF.COORD[1]
LOAD_INTERVAL = 500
DX            = eqF.DX
DY            = eqF.DY

def init_matrix(m, eq_n):
    """
    Create all the components of a matrix such that there will be eq_n x eq_n
    number of sub matrices in a 2D array.
    """
    eq_mtrx = []

    # Populate array with arrays of sparse matrices
    for row in range(eq_n):
        mtrx_row = []

        for col in range(eq_n):
            # Populate row of matrices
            mtrx_row.append(
                lil_matrix((m, m), dtype=np.cfloat)
            )

        # Add row to eq_mtrx
        eq_mtrx.append( mtrx_row )

    return eq_mtrx


def stitch_matrix(mtrx, eq_n):
    """
    Stack all matrices to form a single sparse matrix such that the it retains
    the order provided by the equation matrix. Stacks all components in a row
    into one matrix, then stacks all rows into a single matrix of size.
    """

    # Horizontally stack each row
    for row in range(eq_n):
        mtrx[row] = hstack(mtrx[row])

    # Vertically stack all rows
    return vstack(mtrx).tocsr()


def get_neighbor_ind(df, indx):
    """
    Returns the dataframe indices of the neighbors at a specified point. If a
    neighbor does not exist, it is assumed that the center point is along a
    boundary. The neighbor is given a index of -1.

    Index return: [center, up, down, left, right]
    If boolean 'bound' is true, the center point lies along a boundary, false
    otherwise.
    """

    # Initialize boundary bool
    bound = False

    # Get center location
    curr  = df.loc[indx]
    x     = curr[X_LAB]
    y     = curr[Y_LAB]

    # Find neighbor indices, will return a list with one element since
    # all points are unique (deduplicated during preprocess).
    up    = df[(df[X_LAB] == x)      & (df[Y_LAB] == y - DY)].index.values
    down  = df[(df[X_LAB] == x)      & (df[Y_LAB] == y + DY)].index.values
    left  = df[(df[X_LAB] == x - DX) & (df[Y_LAB] == y)     ].index.values
    right = df[(df[X_LAB] == x + DX) & (df[Y_LAB] == y)     ].index.values

    # If a list is empty, assign the neighbor an index of -1 and mark the point
    # as a boundary.
    if len(up)    == 0: up    = [-1]; bound = True
    if len(down)  == 0: down  = [-1]; bound = True
    if len(left)  == 0: left  = [-1]; bound = True
    if len(right) == 0: right = [-1]; bound = True

    return (indx, *up, *down, *left, *right), bound


def get_func_name(eq_name, var_name, description):
    """
    Return a formatted string that represents the name of the function that
    should be used at a point based on the current equation and variable.
    """
    return "{0}_{1}_{2}".format(eq_name, var_name, description)


def boundary_condition_A(df, neighbors, mtrx, eq_name, var_name):
    """
    If a point resides at a boundary, evaluate it properly for the A matrix
    """
    bound     = get_func_name(eq_name, var_name, BOUND_NAME)
    curr_indx = neighbors[0]

    if hasattr(BC, bound): #and curr_indx != -1:
        mtrx[curr_indx,curr_indx] = getattr(BC, bound)([])


def boundary_condition_B(df, neighbors, mtrx):
    """
    If a point resides at a boundary, evaluate it properly for the B matrix
    """
    indx            = neighbors[0]
    mtrx[indx,indx] = 0


def evaluate_point(df, neighbors, mtrx, eq_name, var_name):
    """
    Evaluate a point in the B matrix that does not reside along a boundary.
    Calls on the appropriate function name within the equations file.
    If the function is not predefined, then the expression at the point is
    evaluated as 0.
    If the function does exist, evaluate the point using the existing
    expression.
    """

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


def build_B(B_, eq_names, var_names, m, eq_n):
    """
    Use the sub matrix B_ to create the B matrix of size (m * eq_n) x (m * eq_n)
    and paste the contents of B_ along the diagonal. Assumes that the order of
    the variables and equations is the same.

    Current implementation skips the last equation-component pair.
    """
    B_mtrx = init_matrix(m, eq_n)

    for eq_var_pair in range(eq_n - 1):
        B_mtrx[eq_var_pair][eq_var_pair] = B_

    return B_mtrx


def build_coefficient_matrix(df):
    """
    Builds the coefficient matrix B and applies boundary conditions to the
    A matrix. Utilizes the equations file to achieve this.
    """

    # Initialize variables
    eq_n    = eqF.get_equation_number()
    m,_     = df.shape
    eq_mtrx = init_matrix(m, eq_n)

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

    # Finalize A matrix
    A_mtrx = stitch_matrix( eq_mtrx, eq_n )

    # Build and finalize B matrix
    B_mtrx = stitch_matrix( build_B(B_, eq_names, var_names, m, eq_n), eq_n )

    return A_mtrx, B_mtrx



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
