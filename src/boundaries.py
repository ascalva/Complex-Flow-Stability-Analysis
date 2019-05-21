import numpy as np

from .constants  import *

X_LAB         = eqF.COORD[0]
Y_LAB         = eqF.COORD[1]

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
    # if b_name == "left":
    if neighbors[NEIGHBOR["left"]]    == -1:
        b_type = get_bound_type_left(df, curr_indx)

    # elif b_name == "right":
    elif neighbors[NEIGHBOR["right"]] == -1:
        b_type = get_bound_type_right(df, curr_indx)

    elif neighbors[NEIGHBOR["up"]]    == -1:
        b_type = get_bound_type_up(df, curr_indx)

    elif neighbors[NEIGHBOR["down"]]  == -1:
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


def boundary_condition_A(df, neighbors, mtrx, eq_name, var_name, b_lst):
    """
    If a point resides at a boundary, evaluate it properly for the A matrix
    """

    curr_indx = neighbors[0]
    walls     = list(filter(None, b_lst))
    wall_num  = len(walls)
    b_name    = "_".join(walls)
    b_type    = ""

    if wall_num == 1:
        b_type = get_bound_type_wall(df, curr_indx, neighbors)

    elif wall_num == 2:
        b_type = get_bound_type_corner(df, curr_indx, neighbors)

    # Get function name for boundary equation
    b_name   += "_" + b_type
    bound     = get_func_name(eq_name, var_name, b_name)

    # Search for function and compute value at point
    if hasattr(BC, bound):

        attributes                = ATTRIBUTES
        df_row                    = df.loc[curr_indx]
        variables                 = [df_row[attr] for attr in attributes]
        mtrx[curr_indx,curr_indx] = getattr(BC, bound)(variables)

        # df.loc[curr_indx, "Boundary"] = 2


def boundary_condition_B(df, neighbors, mtrx):
    """
    If a point resides at a boundary, evaluate it properly for the B matrix
    """
    indx            = neighbors[0]
    mtrx[indx,indx] = 0
