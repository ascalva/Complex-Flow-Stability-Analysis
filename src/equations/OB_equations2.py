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
DX     = 0.002
DY     = 0.002

COORD  = (
     "Points:0",
     "Points:1",
     "Points:2"
)


##############################################################################
############################## MATRIX STRUCTURE ##############################
##############################################################################

def get_equation_number():
    """
    Return number of equations and unknowns for the given system.
    """
    return 6

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
        "A11",
        "A12",
        "A22",
        "v1",
        "v2",
        "p"
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
# cen    = i, j
# up     = i, j - 1
# down   = i, j + 1
# left   = i - 1, j
# right  = i + 1, j
#

############################# Recurring Expressions ##########################
def Beta():
    return ETA_S / (ETA_S + ETA_P)

def dx():
    return 1 / (2 * DX)

def dy():
    return 1 / (2 * DX)

############################### A_11 Equation ################################

def A11_p_cen(prms):
    return 0

def A11_v1_cen(prms):
    return - prms[5]

def A11_v1_right(prms):
    return 2 * prms[0] * dx()

def A11_v1_left(prms):
    return - 2 * prms[0] * dx()

def A11_v1_down(prms):
    return 2 * prms[1] * dy()

def A11_v1_up(prms):
    return - 2 * prms[1] * dy()

def A11_v2_cen(prms):
    return - prms[6]

def A11_A11_cen(prms):
    return 2 * prms[11] - 1 - ALPHA * (2 * prms[0] - 2)

def A11_A11_right(prms):
    return - prms[3] * dx()

def A11_A11_left(prms):
    return prms[3] * dx()

def A11_A11_down(prms):
    return - prms[4] * dy()

def A11_A11_up(prms):
    return prms[4] * dy()

def A11_A12_cen(prms):
    return 2 * prms[12] - ALPHA * (2 * prms[1])

def A11_A22_cen(prms):
    return 0

############################### A_12 Equation ################################

def A12_p_cen(prms):
    return 0

def A12_v1_cen(prms):
    return - prms[7]

def A12_v1_right(prms):
    return 2 * prms[1] * dx()

def A12_v1_left(prms):
    return - 2 * prms[1] * dx()

def A12_v1_down(prms):
    return 2 * prms[2] * dy()

def A12_v1_up(prms):
    return - 2 * prms[2] * dy()

def A12_v2_cen(prms):
    return - prms[8]

def A12_v2_right(prms):
    return 2 * prms[0] * dx()

def A12_v2_left(prms):
    return - 2 * prms[0] * dx()

def A12_v2_down(prms):
    return 2 * prms[1] * dy()

def A12_v2_up(prms):
    return - 2 * prms[1] * dy()

def A12_A11_cen(prms):
    return prms[13] - ALPHA * prms[1]

def A12_A12_cen(prms):
    return prms[11] + prms[14] - 1 - ALPHA * (prms[0] + prms[2] - 2)

def A12_A12_right(prms):
    return - prms[3] * dx()

def A12_A12_left(prms):
    return prms[3] * dx()

def A12_A12_down(prms):
    return  - prms[4] * dy()

def A12_A12_up(prms):
    return prms[4] * dy()

def A12_A22_cen(prms):
    return prms[12] - ALPHA * prms[1]


############################### A_22 Equation ################################

def A22_p_cen(prms):
    return 0

def A22_v1_cen(prms):
    return - prms[9]

def A22_v2_cen(prms):
    return - prms[10]

def A22_v2_right(prms):
    return 2 * prms[1] * dx()

def A22_v2_left(prms):
    return - 2 * prms[1] * dx()

def A22_v2_down(prms):
    return 2 * prms[2] * dy()

def A22_v2_up(prms):
    return - 2 * prms[2] * dy()

def A22_A11_cen(prms):
    return 0

def A22_A12_cen(prms):
    return 2 * prms[13] - ALPHA * 2 * prms[1]

def A22_A22_cen(prms):
    return 2 * prms[14] - 1 - ALPHA * (2 * prms[2] - 2)

def A22_A22_right(prms):
    return - prms[3] * dx()

def A22_A22_left(prms):
    return prms[3] * dx()

def A22_A22_down(prms):
    return - prms[4] * dy()

def A22_A22_up(prms):
    return prms[4] * dy()


############################### x1 Equation ################################

def x1_p_right(prms):
    return - dx() * El

def x1_p_left(prms):
    return dx() * El

def x1_v1_cen(prms):
    return - prms[11] - 2 * Beta() * El * (1 / DX**2 + 1 / DY**2)

def x1_v1_right(prms):
    return - prms[3] * dx() + El * Beta() / DX**2

def x1_v1_left(prms):
    return prms[3] * dx() + El * Beta() / DX**2

def x1_v1_down(prms):
    return - prms[4] * dy() + El * Beta() / DY**2

def x1_v1_up(prms):
    return prms[4] * dy() + El * Beta() / DY**2

def x1_v2_cen(prms):
    return - prms[12]

def x1_A11_right(prms):
    return dx() * El

def x1_A11_left(prms):
    return - dx() * El

def x1_A12_down(prms):
    return dy() * El

def x1_A12_up(prms):
    return - dy() * El

def x1_A22_cen(prms):
    return 0


############################### x2 Equation ################################

def x2_p_down(prms):
    return - dy() * El

def x2_p_up(prms):
    return dy() * El

def x2_v1_cen(prms):
    return - prms[13]

def x2_v2_cen(prms):
    return - prms[11] - 2 * El * Beta() * (1/DX**2 + 1/DY**2)

def x2_v2_right(prms):
    return - prms[3] * dx() + El * Beta() / DX**2

def x2_v2_left(prms):
    return prms[3] * dx() + El * Beta() / DX**2

def x2_v2_down(prms):
    return - prms[4] * dy() + El * Beta() / DY**2

def x2_v2_up(prms):
    return prms[4] * dy() + El * Beta() / DY**2

def x2_A11_cen(prms):
    return 0

def x2_A12_right(prms):
    return dx() * El

def x2_A12_left(prms):
    return - dx() * El

def x2_A22_down(prms):
    return dy() * El

def x2_A22_up(prms):
    return - dy() * El


############################### m Equation ################################

def m_p_cen(prms):
    return 0

def m_v1_right(prms):
    return dx()

def m_v1_left(prms):
    return - dx()

def m_v2_down(prms):
    return dy()

def m_v2_up(prms):
    return - dy()

def m_A11_cen(prms):
    return 0

def m_A12_cen(prms):
    return 0

def m_A22_cen(prms):
    return 0
