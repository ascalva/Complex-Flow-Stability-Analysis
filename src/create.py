import numpy as np

from scipy.sparse          import identity, vstack, hstack, lil_matrix

from .boundary_computation import boundary_condition_A, boundary_condition_B
from .point_computation    import get_neighbor_ind, evaluate_point
from .constants            import *

#
# filename: create.py
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Builds and populates A and B matrix based on the equations provided
#          in the equations file.
#


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


def build_B(B_, eq_names, var_names, m, eq_n):
    """
    Use the sub matrix B_ to create the B matrix of size (m * eq_n) x (m * eq_n)
    and paste the contents of B_ along the diagonal. Assumes that the order of
    the variables and equations is the same.

    Current implementation skips the last equation-component pair.
    """
    B_mtrx   = init_matrix(m, eq_n)
    s_factor = 1e-4

    # Pairs up all equations and components
    for eq_var_pair in range(eq_n - 1):
        B_mtrx[eq_var_pair][eq_var_pair] = B_

    B_mtrx[eq_n - 1][eq_n - 1] = B_ * s_factor

    return B_mtrx


def build_coefficient_matrix(df):
    """
    Builds the coefficient matrix B and applies boundary conditions to the
    A matrix. Utilizes the equations file to achieve this.
    """

    # Initialize variables
    eq_n    = EQ_NUM
    m,_     = df.shape
    eq_mtrx = init_matrix(m, eq_n)

    # Create top left matrix (mxm) of B matrix, will be an identity where the
    # row is zero at a boundary
    B_ = identity(m, format='lil', dtype=np.cfloat)

    eq_names  = EQ_NAMES
    var_names = VAR_NAMES

    # bound_point = 0
    # non_bound_point = 0
    # Populate all matrices along their diagonal
    for indx, row in df.iterrows():

        if indx % LOAD_INTERVAL == 0:
            print("{0:.1f}% complete..".format(indx * 100 / df.shape[0]))
            # print(bound_point, non_bound_point)

        # Get indices of neighboring points
        neighbors, bound, b_lst = get_neighbor_ind(df, indx)

        # Bound B if at a boundary
        if bound: boundary_condition_B(df, neighbors, B_);
        # else: non_bound_point+=1

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
                    boundary_condition_A(df, neighbors, curr_eq_mtrx, curr_eq_name, curr_var_name, b_lst)


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
