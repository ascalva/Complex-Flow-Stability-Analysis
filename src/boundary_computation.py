import numpy as np

from .misc              import get_func_name, find_row_from_coord
from .point_computation import get_neighbor_ind
from .constants         import *

X_LAB = COORD[0]
Y_LAB = COORD[1]

def get_bound_type_left(df, curr_indx):
    x = df.loc[curr_indx][X_LAB]

    if np.isclose(x, X_MIN, atol = COORD_TOL * 2):
        # df.loc[curr_indx, "Boundary"] = 3
        return CHANNEL_TYPE[0]

    else:
        # df.loc[curr_indx, "Boundary"] = 4
        return CHANNEL_TYPE[1]


def get_bound_type_right(df, curr_indx):
    x = df.loc[curr_indx][X_LAB]

    if np.isclose(x, X_MAX, atol = COORD_TOL * 2):
        # df.loc[curr_indx, "Boundary"] = 5
        return CHANNEL_TYPE[0]

    else:
        # df.loc[curr_indx, "Boundary"] = 6
        return CHANNEL_TYPE[1]


def get_bound_type_up(df, curr_indx):
    y = df.loc[curr_indx][Y_LAB]

    if np.isclose(y, Y_MIN, atol = COORD_TOL * 2):
        # df.loc[curr_indx, "Boundary"] = 7
        return CHANNEL_TYPE[1]

    else:
        # df.loc[curr_indx, "Boundary"] = 8
        return CHANNEL_TYPE[0]


def get_bound_type_down(df, curr_indx):
    y = df.loc[curr_indx][Y_LAB]

    if np.isclose(y, Y_MAX, atol = COORD_TOL * 2):
        # df.loc[curr_indx, "Boundary"] = 9
        return CHANNEL_TYPE[1]

    else:
        # df.loc[curr_indx, "Boundary"] = 10
        return CHANNEL_TYPE[0]


def get_bound_type_wall(df, curr_indx, neighbors):
    if neighbors[NEIGHBOR[LEFT]]    == -1:
        b_type = get_bound_type_left(df, curr_indx)

    elif neighbors[NEIGHBOR[RIGHT]] == -1:
        b_type = get_bound_type_right(df, curr_indx)

    elif neighbors[NEIGHBOR[UP]]    == -1:
        b_type = get_bound_type_up(df, curr_indx)

    elif neighbors[NEIGHBOR[DOWN]]  == -1:
        b_type = get_bound_type_down(df, curr_indx)

    else:
        print("Somthing went wrong")

    return b_type


def get_corner_type_up_left(df, curr_indx):
    x = df.loc[curr_indx][X_LAB]
    y = df.loc[curr_indx][Y_LAB]

    left_edge = np.isclose(x, X_MIN, atol = COORD_TOL * 2)
    up_edge   = np.isclose(y, Y_MIN, atol = COORD_TOL * 2)

    if left_edge and not up_edge:
        # df.loc[curr_indx, "Boundary"] = 11
        return CHANNEL_TYPE[0]

    elif not left_edge and up_edge:
        # df.loc[curr_indx, "Boundary"] = 12
        return CHANNEL_TYPE[1]


def get_corner_type_up_right(df, curr_indx):
    x = df.loc[curr_indx][X_LAB]
    y = df.loc[curr_indx][Y_LAB]

    right_edge = np.isclose(x, X_MAX, atol = COORD_TOL * 2)
    up_edge    = np.isclose(y, Y_MIN, atol = COORD_TOL * 2)

    if right_edge and not up_edge:
        # df.loc[curr_indx, "Boundary"] = 13
        return CHANNEL_TYPE[0]

    elif not right_edge and up_edge:
        # df.loc[curr_indx, "Boundary"] = 14
        return CHANNEL_TYPE[1]


def get_corner_type_down_right(df, curr_indx):
    x = df.loc[curr_indx][X_LAB]
    y = df.loc[curr_indx][Y_LAB]

    right_edge = np.isclose(x, X_MAX, atol = COORD_TOL * 2)
    down_edge  = np.isclose(y, Y_MAX, atol = COORD_TOL * 2)

    if right_edge and not down_edge:
        # df.loc[curr_indx, "Boundary"] = 15
        return CHANNEL_TYPE[0]

    elif not right_edge and down_edge:
        # df.loc[curr_indx, "Boundary"] = 16
        return CHANNEL_TYPE[1]


def get_corner_type_down_left(df, curr_indx):
    x = df.loc[curr_indx][X_LAB]
    y = df.loc[curr_indx][Y_LAB]

    left_edge = np.isclose(x, X_MIN, atol = COORD_TOL * 2)
    down_edge = np.isclose(y, Y_MAX, atol = COORD_TOL * 2)

    if left_edge and not down_edge:
        # df.loc[curr_indx, "Boundary"] = 17
        return CHANNEL_TYPE[0]

    elif not left_edge and down_edge:
        # df.loc[curr_indx, "Boundary"] = 18
        return CHANNEL_TYPE[1]


def get_bound_type_corner(df, curr_indx, neighbors):

    if   neighbors[1] == -1 and neighbors[3] == -1:
        c_type = get_corner_type_up_left(df, curr_indx)

    elif neighbors[1] == -1 and neighbors[4] == -1:
        c_type = get_corner_type_up_right(df, curr_indx)

    elif neighbors[2] == -1 and neighbors[4] == -1:
        c_type = get_corner_type_down_right(df, curr_indx)

    elif neighbors[2] == -1 and neighbors[3] == -1:
        c_type = get_corner_type_down_left(df, curr_indx)

    else:
        print("Type of corner does not exist!")


    return c_type

def get_bound_type_corner_inner(df, curr_indx, neighbors):
    return ""

def boundary_condition_A(df, neighbors, mtrx, eq_name, var_name, b_lst):
    """
    If a point resides at a boundary, evaluate it properly for the A matrix
    """
    attributes = ATTRIBUTES
    curr_indx  = neighbors[0]
    walls      = list(filter(None, b_lst))
    wall_num   = len(walls)
    b_name     = DELIM.join(walls)
    b_type     = ""

    # Wall boundary
    if wall_num   == 1:
        b_type = get_bound_type_wall(df, curr_indx, neighbors)

    # Outer corner boundary
    elif wall_num == 2:
        b_type = get_bound_type_corner(df, curr_indx, neighbors)

    # Inner corner boundary
    elif wall_num == 0:
        b_type = get_bound_type_corner_inner(df, curr_indx, neighbors)

    # Get function name for boundary equation
    b_name   += DELIM + b_type + DELIM

    # Index of center cell
    curr_indx = neighbors[0]

    # Iterate over all neighbors (includes center location)
    for neigh in range(0, NEIGHBOR_NUM):

        # Find name of function at current location
        bound   = get_func_name(eq_name, var_name, b_name + NEIGHBOR_LOC[neigh])
        df_indx = neighbors[neigh]

        # Search for function and compute value at point, ignore vacant neighb
        if hasattr(BC, bound) and df_indx != -1:

            df_row                    = df.loc[df_indx]
            variables                 = [df_row[attr] for attr in attributes]
            mtrx[curr_indx,curr_indx] = getattr(BC, bound)(variables)

            df.loc[curr_indx, "Boundary"] = 2


def boundary_condition_B(df, neighbors, mtrx):
    """
    If a point resides at a boundary, evaluate it properly for the B matrix
    """
    indx            = neighbors[0]
    mtrx[indx,indx] = 0.0

def evaluate_inner_corners(df, eq_mtrx):
    """
    Evaluate inner corners of the simulation. Special care is required since
    are not missing any neighbors, and are evaluated as non-boundary points.
    Their locations are predefined and evaluated after the main evaluation loop.
    """

    # Get all necessary attributes/equation names
    eq_n      = EQ_NUM
    eq_names  = EQ_NAMES
    var_names = VAR_NAMES
    corners   = INNR_CRNR_LOC

    # Iterate over all 4 inner corners
    for x,y in corners:

        # Find row index and neighbors
        indx          = find_row_from_coord(df, x, y)
        neighbors,_,_ = get_neighbor_ind(df, indx)

        # At a specific location, calculate the value for each matrix with
        # its respective equation.
        for r_indx in range(eq_n):
            for c_indx in range(eq_n):

                # Get current values (matrix and names of eq and var)
                curr_eq_mtrx  = eq_mtrx[r_indx][c_indx]
                curr_eq_name  = eq_names[r_indx]
                curr_var_name = var_names[c_indx]

                boundary_condition_A(df, neighbors, curr_eq_mtrx, curr_eq_name, curr_var_name, [])
