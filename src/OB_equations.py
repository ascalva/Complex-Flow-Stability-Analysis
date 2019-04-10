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

LAMBDA = 0.01
H      = 0.1
ETA_S  = 0.1111111
ETA_P  = 0.8888889
El     = 1e6
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
        [A11eq_v1, A11eq_A11, A11eq_A12, A11eq_A22, 1],
        [A12eq_v1, A12eq_A11, A12eq_A12, A12eq_A22, 1],
        [A22eq_v1, A22eq_A11, A22eq_A12, A22eq_A22, 1],
        [v1eq_v1,  v1eq_A11,  v1eq_A12,  v1eq_A22,  1]
    ]

def get_equation_names():
    return [
        "A11",
        "A12",
        "A22",
        "x1",
        "x2",
        "m"
    ]

def get_component_names():
    return [
        "p",
        "v1",
        "v2",
        "A11",
        "A12",
        "A22"
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


##############################################################################
################################# EQUATIONS ##################################
##############################################################################
#
# params = [A_11, A_12, A_22, v_1x_1, v_2x_1, v_2x_2, v_0, v_1]
# k      = [k_1, k_2]
#

############################# Recurring Expressions ##########################
def Beta():
    return ETA_S / (ETA_S + ETA_P)

def vnkn(prms, k):
    return (prms[3] * 1j * k[0]) + (prms[4] * 1j * k[1])

def sum_k(k):
    """
    Compute the sum of squares of k's.
    """
    return (k[0] ** 2) + (k[1] ** 2)


############################### A_11 Equation ################################

def A11eq_v1(prms, k):
    """
    Calculate the v1-component of A_11 equation
    """
    return - prms[5] + (2 * prms[0] * 1j * k[0]) + (2 * prms[1] * 1j * k[1]) \
           + ((k[0]/k[1]) * prms[6])

def A11eq_A11(prms, k):
    """
    Calculate the A11-component of A_11 equation
    """
    return -vnkn(prms,k) + (2 * prms[11]) - 1 - ALPHA * (2 * prms[0] - 2)

def A11eq_A12(prms, k):
    """
    Calculate the A12-component of A_11 equation
    """
    return 2 * prms[12] - ALPHA * (2 * prms[1])

def A11eq_A22(prms, k):
    """
    Calculate the A22-component of A_11 equation
    """
    return 0


############################### A_12 Equation ################################

def A12eq_v1(prms, k):
    """
    Calculate the v1-component of A_12 equation
    """
    return - prms[7] + (prms[1] * 1j * k[0]) + (prms[2] * 1j * k[1]) \
           + (k[0]/k[1]) * (prms[8] - (prms[0] * 1j * k[0]) - (prms[1] * 1j * k[1]))

def A12eq_A11(prms, k):
    """
    Calculate the A11-component of A_12 equation
    """
    return prms[13] - ALPHA * prms[1]

def A12eq_A12(prms, k):
    """
    Calculate the A12-component of A_12 equation
    """
    return - vnkn(prms, k) + prms[11] + prms[14] - 1 \
           - ALPHA * (prms[0] + prms[2] - 2)

def A12eq_A22(prms, k):
    """
    Calculate the A22-component of A_12 equation
    """
    return prms[12] - ALPHA * prms[1]


############################### A_22 Equation ################################

def A22eq_v1(prms, k):
    """
    Calculate the v1-component of A_22 equation
    """
    return (k[0]/k[1]) * (prms[10] - (2 * prms[1] * 1j * k[0]) - (2 * prms[2] * 1j * k[1])) \
           - prms[9]

def A22eq_A11(prms, k):
    """
    Calculate the A11-component of A_22 equation
    """
    return 0

def A22eq_A12(prms, k):
    """
    Calculate the A12-component of A_22 equation
    """
    return (2 * prms[13]) - ALPHA * (2 * prms[1])

def A22eq_A22(prms, k):
    """
    Calculate the A22-component of A_22 equation
    """
    return - vnkn(prms, k) + (2 * prms[14]) - 1 - ALPHA * (2 * prms[2] - 2)


########################### v_1 Momentum Equation ############################

def v1eq_v1(prms, k):
    """
    Calculate the v1-component of v_1 equation
    TODO: Re-check
    """
    return (k[0] * prms[12] - k[1] * (prms[11] + vnkn(prms,k))
            + k[0] * prms[13] - (k[0]**2 / k[1]) * (prms[14] + vnkn(prms,k))
            ) * (k[1] / sum_k(k)) - (Beta() * sum_k(k) * El)

def v1eq_A11(prms, k):
    """
    Calculate the A11-component of v_1 equation
    """
    return (El * 1j * k[0] * (k[1] ** 2)) / sum_k(k)

def v1eq_A12(prms, k):
    """
    Calculate the A12-component of v_1 equation
    """
    return (El * 1j * k[1] * (k[1]**2 - k[0]**2)) / sum_k(k)

def v1eq_A22(prms, k):
    """
    Calculate the A22-component of v_1 equation
    """
    return - v1eq_A11(prms, k)
