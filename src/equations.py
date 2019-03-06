#
# filename: equations.py
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Provides all necessary equations for the calculation of the
#          A-matrix based on the given data.
#

##############################################################################
############################## MATRIX STRUCTURE ##############################
##############################################################################

def get_equation_number():
    """
    Return number of equations and unknowns for the given system.
    """
    return 2


def get_equations():
    """
    Return the equations used for calculating the matrices. The order and
    position of the equations is important. The placement of each equation
    will determine the placement of the matrix for that equation along the
    A matrix.
    """
    return [
        [ueq_u, ueq_v],
        [veq_u, veq_v]
    ]


def get_vars():
    """
    Return parameters used for calculations. The order is important, it should
    match the order of the parameters of the equations.
    """
    return [
        "U:0",
        "A:0"
    ]


##############################################################################
############################ BOUNDARY CONDITIONS #############################
##############################################################################

def set_bound_conditions(eq_mtrx, m, m_type):
    """
    Sets boundary conditions of matrix equation, subject to change depending
    on simulation geometry and type.
    """
    if m_type == "A":
        set_bound_conditions_A(eq_mtrx, m)

    elif m_type == "B":
        set_bound_conditions_B(eq_mtrx, m)

    else:
        raise ValueError("Wrong matrix type!")


def set_bound_conditions_A(eq_mtrx, m):
    """
    Make the first and last elements of the ueq_v diagonal matrix equal
    to 0 (boundary conditions).
    """

    # Ueqn_u
    eq_mtrx[0][0][0, 0]         = 1.0
    eq_mtrx[0][0][m - 1, m - 1] = 1.0

    # Ueqn_v
    eq_mtrx[0][1][0, 0]         = 0.0
    eq_mtrx[0][1][m - 1, m - 1] = 0.0


def set_bound_conditions_B(eq_mtrx, m):
    """
    Make the first and last elements of the ueq_v diagonal matrix equal
    to 0 (boundary conditions).
    """
    # Set top and bottom of rows of identity matrix equal to zero.
    eq_mtrx[0][0][0,0] = 0.0
    eq_mtrx[0][0][m - 1, m - 1] = 0.0


##############################################################################
################################# EQUATIONS ##################################
##############################################################################

def ueq_u(params, k):
    """
    Calculate the u-component of the U matrix.
    """
    if len(params) == 0:
        return 1

    u = params[0]
    v = params[1]
    return v - k[0]**2


def ueq_v(params, k):
    """
    Calculate the v-component of the U matrix.
    """
    if len(params) == 0:
        return 1

    u = params[0]
    v = params[1]
    return u


def veq_u(params, k):
    """
    Calculate the u-component of the V matrix.
    """
    if len(params) == 0:
        return 1

    u = params[0]
    v = params[1]
    return - 1j * k[0]


def veq_v(params, k):
    """
    Calculate the v-component of the V matrix.
    """
    if len(params) == 0:
        return 1

    u = params[0]
    v = params[1]
    return 2 * v
