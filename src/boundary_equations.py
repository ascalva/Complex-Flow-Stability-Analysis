##############################################################################
############################ BOUNDARY CONDITIONS #############################
##############################################################################
#
# filename: boundary_condition.py
#
# @author: Alberto Serrano
#

CHANNEL_LENGTH = 1.0
CHANNEL_WIDTH  = 0.1

def get_inner_corners():
    return [
        ( CHANNEL_LENGTH,                 CHANNEL_LENGTH                 ),
        ( CHANNEL_LENGTH,                 CHANNEL_LENGTH + CHANNEL_WIDTH ),
        ( CHANNEL_LENGTH + CHANNEL_WIDTH, CHANNEL_LENGTH                 ),
        ( CHANNEL_LENGTH + CHANNEL_WIDTH, CHANNEL_LENGTH + CHANNEL_WIDTH )
    ]

# points on a boundary:
# eq_var_wall-orientation_channel_neighbor

# Left wall along left inlet
def x1_v1_left_inlet_cen(prms):
    return 1

def A11_A11_left_inlet_cen(prms):
    return 1

def m_p_left_inlet_cen(prms):
    return

def m_p_left_inlet_right(prms):
    return

# Right wall along right inlet
def x1_v1_right_inlet(prms):
    return 1

def A11_A11_right_inlet(prms):
    return 1

def m_p_right_inlet(prms):
    return 1

# Upper wall along the top outlet


# Bottom wall along the bottom outlet


# The top walls along the inlets

# The bottom walls along the inlets

# The left walls along the outlets

# The right walls along the outlets

# Outer corners along the outlets

# Outer corners along the inlets

# def A11_A11_bound(prms):
#     return 1
#
# def A12_A12_bound(prms):
#     return 1
#
# def A22_A22_bound(prms):
#     return 1
#
# def x1_v1_bound(prms):
#     return 1
#
# def x2_v2_bound(prms):
#     return 1
#
# def m_p_bound(prms):
#     return 1
#
# def inner_corner_bound(prms):
#     return 1
