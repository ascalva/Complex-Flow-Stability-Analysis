#
# filename: equations.py
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Provides all necessary equations for the calculation of the
#          A-matrix based on the given data.
#          Uses the system of equations for the Oldroyd-B model in 2D.
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
        "A:0",            # A_11
        "A:1",            # A_12
        "A:3",            # A_22
        "Gradients U:0",  # v_1x_1
        "Gradients U:3",  # v_2x_1
        "Gradients U:4",  # v_2x_2
        "U:1",            # v_0
        "U:2"             # v_1
    ]


##############################################################################
############################ BOUNDARY CONDITIONS #############################
##############################################################################

def set_bound_conditions(eq_mtrx, m, m_type):
    """
    Sets boundary conditions of matrix equation, subject to change depending
    on simulation geometry and type.
    """
    # if m_type == "A":
    #     set_bound_conditions_A(eq_mtrx, m)
    #
    # elif m_type == "B":
    #     set_bound_conditions_B(eq_mtrx, m)
    #
    # else:
    #     raise ValueError("Wrong matrix type!")
    return



##############################################################################
################################# EQUATIONS ##################################
##############################################################################
#
# params = [A_11, A_12, A_22, v_1x_1, v_2x_1, v_2x_2, v_0, v_1]
# k      = [k_1, k_2]
#
############################### A_11 Equation ################################
def A11eq_p(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0

def A11eq_v1(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return (params[0] * 1j * k[0]) + (2 * params[1] * 1j * k[1])

def A11eq_v2(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return - params[0] * 1j * k[1]

def A11eq_A11(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return params[3] - params[5] - 1

def A11eq_A12(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 2 * params[3]

def A11eq_A22(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0


############################### A_12 Equation ################################
# params = [A_11, A_12, A_22, v_1x_1, v_2x_1, v_2x_2, v_0, v_1]

def A12eq_p(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0

def A12eq_v1(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return params[2] * 1j * k[1]

def A12eq_v2(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return params[0] * 1j * k[0]

def A12eq_A11(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return params[4]

def A12eq_A12(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0 # there's no value in pdf

def A12eq_A22(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return params[3]


############################### A_22 Equation ################################

def A22eq_p(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0

def A22eq_v1(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0

def A22eq_v2(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0

def A22eq_A11(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0

def A22eq_A12(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0

def A22eq_A22(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0


########################### x_1 Momentum Equation ############################
