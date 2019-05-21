
def get_func_name(eq_name, var_name, description):
    """
    Return a formatted string that represents the name of the function that
    should be used at a point based on the current equation and variable.
    """
    return "{0}_{1}_{2}".format(eq_name, var_name, description)
