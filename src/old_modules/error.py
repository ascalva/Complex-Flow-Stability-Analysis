import numpy as np

# Global values
error_check_bool = False


def check_matrix_dims():
    global error_check_bool

    # Only error check first time this function has been called, return without
    # doing anything after.
    if not error_check_bool:
        print("hewwo")
        error_check_bool = True

    else:
        return

    # Retrive all equation data from equation file
    eq_n = get_equation_number()
    eqs  = np.array(get_equations())

    if len(eqs.shape) != 2:
        raise ValueError("Wrong dimensions: There could be an extra or missing value in equation matrix.")

    if not (eqs.shape[0] + 1 == eqs.shape[1]) and not (eqs.shape[0] + 1 == eqs.shape[1]):
        raise ValueError("Wrong dimensions: Equation matrix must be of dimension (n,n) or (n,n+1).")

    if eq_n != eqs.shape[0]:
        raise ValueError("Equation number and equation matrix dimensions don't match.")

def check_vars(df):
    var = get_vars()
