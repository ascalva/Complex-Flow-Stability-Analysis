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
############################## SIMULATION PARAMS #############################
##############################################################################

LAMBDA = 0.1
H      = 0.1
ETA_S  = 0.1111111
ETA_P  = 0.8888889
El     = 10e6
ALPHA  = 0.0


##############################################################################
############################## MATRIX STRUCTURE ##############################
##############################################################################

def get_equation_number():
    """
    Return number of equations and unknowns for the given system.
    """
    return 4


def get_equations():
    """
    Return the equations used for calculating the matrices. The order and
    position of the equations is important. The placement of each equation
    will determine the placement of the matrix for that equation along the
    A matrix.
    """
    return [
        [A11eq_v1, A11eq_A11, A11eq_A12, A11eq_A22],
        [A12eq_v1, A12eq_A11, A12eq_A12, A12eq_A22],
        [A22eq_v1, A22eq_A11, A22eq_A12, A22eq_A22],
        [v1eq_v1,  v1eq_A11,  v1eq_A12,  v1eq_A22 ]
    ]


def get_vars():
    """
    Return parameters used for calculations. The order is important, it should
    match the order of the parameters of the equations.
    """
    return [
        "A:0",
        "A:1",
        "A:3",
        "U:0",
        "U:1",
        "Gradients A:0",
        "Gradients A:1",
        "Gradients A:3",
        "Gradients A:4",
        "Gradients A:9",
        "Gradients A:10",
        "Gradients U:0",
        "Gradients U:1",
        "Gradients U:3",
        "Gradients U:4"
    ]


##############################################################################
############################ BOUNDARY CONDITIONS #############################
##############################################################################

def set_bound_conditions(eq_mtrx, m, m_type):
    """
    Sets boundary conditions of matrix equation, subject to change depending
    on simulation geometry and type.
    """
    return


def Beta():
    return ETA_S / (ETA_S + ETA_P)



##############################################################################
################################# EQUATIONS ##################################
##############################################################################
#
# params = [A_11, A_12, A_22, v_1x_1, v_2x_1, v_2x_2, v_0, v_1]
# k      = [k_1, k_2]
#

def vnkn(prms, k):
    return (prms[3] * 1j * k[0]) + (prms[4] * 1j * k[1])

############################### A_11 Equation ################################

def A11eq_v1(prms, k):
    """
    Calculate the -component of A_11 equation
    """
    return -prms[5] + (2 * prms[0] * 1j * k[0]) + (2 * prms[1] * 1j * k[1]) + ((k[1]/k[0]) * prms[6])

def A11eq_A11(prms, k):
    """
    Calculate the -component of A_11 equation
    """
    return -vnkn(prms,k) + (2 * prms[11]) - 1 - ALPHA * (2 * prms[0] - 2)

def A11eq_A12(prms, k):
    """
    Calculate the -component of A_11 equation
    """
    return 2 * prms[12] - ALPHA * (2 * prms[1])

def A11eq_A22(prms, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0


############################### A_12 Equation ################################

def A12eq_v1(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return params[2] * 1j * k[1]

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

def A22eq_v1(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return - params[2] * 1j * k[0]

def A22eq_A11(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0

def A22eq_A12(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 2 * params[4]

def A22eq_A22(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return - params[3] + params[5] - 1


########################### x_1 Momentum Equation ############################

def x1eq_p(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return - 1j * k[0] * El

def x1eq_v1(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return - ((params[6] * 1j * k[0]) + params[3] + params[5]) \
           - Beta() * (k[0]**2 + k[1]**2) * El

def x1eq_v2(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return - params[6] * 1j * k[1]

def x1eq_A11(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 1j * k[0] * El

def x1eq_A12(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 1j * k[1] * El

def x1eq_A22(params, k):
    """
    Calculate the -component of A_11 equation
    """
    return 0
    
