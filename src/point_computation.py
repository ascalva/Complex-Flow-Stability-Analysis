from .misc      import get_func_name
from .constants import *

X_LAB         = eqF.COORD[0]
Y_LAB         = eqF.COORD[1]

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
    b_lst = ["","","","",""]

    # Get center location
    curr  = df.loc[indx]
    x     = curr[X_LAB]
    y     = curr[Y_LAB]

    # Find neighbor indices, will return a list with one element since
    # all points are unique (deduplicated during preprocess).
    up    = df[ (df[X_LAB] == x)      & (df[Y_LAB] == y - DY) ].index.values
    down  = df[ (df[X_LAB] == x)      & (df[Y_LAB] == y + DY) ].index.values
    left  = df[ (df[X_LAB] == x - DX) & (df[Y_LAB] == y)      ].index.values
    right = df[ (df[X_LAB] == x + DX) & (df[Y_LAB] == y)      ].index.values

    # If a list is empty, assign the neighbor an index of -1 and mark the point
    # as a boundary.
    if len(up)    == 0:
        up1 = df[ (df[X_LAB] == x)      & (df[Y_LAB] == y - DY + COORD_TOL) ].index.values
        if len(up1) != 0:
            up = up1

        up2 = df[ (df[X_LAB] == x)      & (df[Y_LAB] == y - DY - COORD_TOL) ].index.values
        if len(up2) != 0:
            up = up2

        if len(up) == 0:
            up       = [-1];
            bound    = True
            b_lst[NEIGHBOR["up"]] = "up"

    if len(down)  == 0:
        down1 = df[ (df[X_LAB] == x)      & (df[Y_LAB] == y + DY + COORD_TOL) ].index.values
        if len(down1) != 0:
            down = down1
            # print("hmm1")

        down2 = df[ (df[X_LAB] == x)      & (df[Y_LAB] == y + DY - COORD_TOL) ].index.values
        if len(down2) != 0:
            down = down2
            # print("hmm2")

        if len(down) == 0:
            down     = [-1];
            bound    = True
            b_lst[NEIGHBOR["down"]] = "down"

    if len(left)  == 0:
        left1  = df[ (df[X_LAB] == x - DX + COORD_TOL) & (df[Y_LAB] == y)      ].index.values
        if len(left1) != 0:
            left = left1

        left2  = df[ (df[X_LAB] == x - DX - COORD_TOL) & (df[Y_LAB] == y)      ].index.values
        if len(left2) != 0:
            left = left2

        if len(left) == 0:
            left     = [-1]
            bound    = True
            b_lst[NEIGHBOR["left"]] = "left"

    if len(right) == 0:
        right1 = df[ (df[X_LAB] == x + DX + COORD_TOL) & (df[Y_LAB] == y)      ].index.values
        if len(right1) != 0:
            right = right1

        right2 = df[ (df[X_LAB] == x + DX - COORD_TOL) & (df[Y_LAB] == y)      ].index.values
        if len(right2) != 0:
            right = right2

        if len(right) == 0:
            right    = [-1]
            bound    = True
            b_lst[NEIGHBOR["right"]] = "right"


    return (indx, *up, *down, *left, *right), bound, b_lst

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
    attributes = ATTRIBUTES

    # Index of center cell
    curr_indx  = neighbors[0]

    # Iterate over all neighbors (includes center location)
    for neigh in range(0, NEIGHBOR_NUM):

        # Find name of function at current location
        func_name = get_func_name(eq_name, var_name, NEIGHBOR_LOC[neigh])

        # Check if function with calculated name exists
        if hasattr(eqF, func_name): #and neighbors[neigh] != -1:
            # df.loc[curr_indx, "Boundary"] = 3

            # Evaluate matrix at location with found function
            df_indx                 = neighbors[neigh]
            df_row                  = df.loc[df_indx]
            variables               = [df_row[attr] for attr in attributes]
            mtrx[curr_indx,df_indx] = getattr(eqF, func_name)(variables)


# def get_neighbor_ind_new(df, indx):
#     tol = 0.003
#
#     # Initialize boundary bool
#     bound = False
#
#     # Get center location
#     curr  = df.loc[indx]
#     x     = curr[X_LAB]
#     y     = curr[Y_LAB]
#
#     approx = df["Points:1"].apply(np.isclose, b=y, atol=tol)
#     res    = df[df["Points:1"]==approx][df["Points:0"]==x]
#
#     # up    = df[df[Y_LAB] == df[Y_LAB].apply(np.isclose, b=y, atol=tol)][df[X_LAB] == x].index.values
#     up    = df[df[X_LAB] == df[Y_LAB].apply(np.isclose, b=y, atol=tol)][df[X_LAB] == x].index.values
#     # up    = df[ (df[X_LAB] == x)      & (df[Y_LAB] == y - DY) ].index.values
