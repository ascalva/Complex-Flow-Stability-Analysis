from .constants import *

def get_func_name(eq_name, var_name, description):
    """
    Return a formatted string that represents the name of the function that
    should be used at a point based on the current equation and variable.
    """
    return "{0}{3}{1}{3}{2}".format(eq_name, var_name, description, DELIM)

def find_row_from_coord(df, x, y):
    """
    Assumes that the data frame has been deduplicated. Returns the data frame
    index at the specificed location (x,y).
    """
    return df[ (df[COORD[0]] == x) & (df[COORD[1]] == y) ].index.values[0]
