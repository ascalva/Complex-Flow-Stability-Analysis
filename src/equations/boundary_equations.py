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
# <eq>_<var>_<wall-orientation>_<channel-type>_<neighbor-location>

# Left wall along left inlet
def x1_v1_left_inlet_cen(prms):
    return 1

def x2_v2_left_inlet_cen(prms):
    return 1

def A11_A11_left_inlet_cen(prms):
    return 1

def A12_A12_left_inlet_cen(prms):
    return 1

def A22_A22_left_inlet_cen(prms):
    return 1

def m_p_left_inlet_cen(prms):
    return -1

def m_p_left_inlet_right(prms):
    return 1


# Right wall along right inlet
def x1_v1_right_inlet_cen(prms):
    return 1

def x2_v2_right_inlet_cen(prms):
    return 1

def A11_A11_right_inlet_cen(prms):
    return 1

def A12_A12_right_inlet_cen(prms):
    return 1

def A22_A22_right_inlet_cen(prms):
    return 1

def m_p_right_inlet_cen(prms):
    return -1

def m_p_right_inlet_left(prms):
    return 1


# Upper wall along the top outlet
def m_p_up_outlet_cen(prms):
    return 1

def x1_v1_up_outlet_cen(prms):
    return -1

def x1_v1_up_outlet_down(prms):
    return 1

def x2_v2_up_outlet_cen(prms):
    return -1

def x2_v2_up_outlet_down(prms):
    return 1

def A11_A11_up_outlet_cen(prms):
    return -1

def A11_A11_up_outlet_down(prms):
    return 1

def A12_A12_up_outlet_cen(prms):
    return -1

def A12_A12_up_outlet_down(prms):
    return 1

def A22_A22_up_outlet_cen(prms):
    return -1

def A22_A22_up_outlet_down(prms):
    return 1


# Bottom wall along the bottom outlet
def m_p_down_outlet_cen(prms):
    return 1

def x1_v1_down_outlet_cen(prms):
    return -1

def x1_v1_down_outlet_up(prms):
    return 1

def x2_v2_down_outlet_cen(prms):
    return -1

def x2_v2_down_outlet_up(prms):
    return 1

def A11_A11_down_outlet_cen(prms):
    return -1

def A11_A11_down_outlet_up(prms):
    return 1

def A12_A12_down_outlet_cen(prms):
    return -1

def A12_A12_down_outlet_up(prms):
    return 1

def A22_A22_down_outlet_cen(prms):
    return -1

def A22_A22_down_outlet_up(prms):
    return 1


# The top walls along the inlets
def x1_v1_down_inlet_cen(prms):
    return 0

def x2_v2_down_inlet_cen(prms):
    return 0

def m_p_down_inlet_cen(prms):
    return 1

def m_p_down_inlet_up(prms):
    return -1

def A11_A11_down_inlet_cen(prms):
    return 1

def A11_A11_down_inlet_up(prms):
    return -1

def A12_A12_down_inlet_cen(prms):
    return 1

def A12_A12_down_inlet_up(prms):
    return -1

def A22_A22_down_inlet_cen(prms):
    return 1

def A22_A22_down_inlet_up(prms):
    return -1

# The bottom walls along the inlets
def x1_v1_up_inlet_cen(prms):
    return 0

def x2_v2_up_inlet_cen(prms):
    return 0

def m_p_up_inlet_cen(prms):
    return -1

def m_p_up_inlet_down(prms):
    return 1

def A11_A11_up_inlet_cen(prms):
    return -1

def A11_A11_up_inlet_down(prms):
    return 1

def A12_A12_up_inlet_cen(prms):
    return -1

def A12_A12_up_inlet_down(prms):
    return 1

def A22_A22_up_inlet_cen(prms):
    return -1

def A22_A22_up_inlet_down(prms):
    return 1


# The left walls along the outlets
def x1_v1_left_outlet_cen(prms):
    return 0

def x2_v2_left_outlet_cen(prms):
    return 0

def m_p_left_outlet_cen(prms):
    return -1

def m_p_left_outlet_right(prms):
    return 1

def A11_A11_left_outlet_cen(prms):
    return -1

def A11_A11_left_outlet_right(prms):
    return 1

def A12_A12_left_outlet_cen(prms):
    return -1

def A12_A12_left_outlet_right(prms):
    return 1

def A22_A22_left_outlet_cen(prms):
    return -1

def A22_A22_left_outlet_right(prms):
    return 1


# The right walls along the outlets
def x1_v1_right_outlet_cen(prms):
    return 0

def x2_v2_right_outlet_cen(prms):
    return 0

def m_p_right_outlet_cen(prms):
    return 1

def m_p_right_outlet_left(prms):
    return -1

def A11_A11_right_outlet_cen(prms):
    return 1

def A11_A11_right_outlet_left(prms):
    return -1

def A12_A12_right_outlet_cen(prms):
    return 1

def A12_A12_right_outlet_left(prms):
    return -1

def A22_A22_right_outlet_cen(prms):
    return 1

def A22_A22_right_outlet_left(prms):
    return -1

### Outer corners along the outlets ###

# Up-left corner
def m_p_up_left_outlet_cen(prms):
    return 1

def x1_v1_up_left_outlet_cen(prms):
    return -1

def x1_v1_up_left_outlet_down(prms):
    return 1

def x2_v2_up_left_outlet_cen(prms):
    return -1

def x2_v2_up_left_outlet_down(prms):
    return 1

def A11_A11_up_left_outlet_cen(prms):
    return 0

def A12_A12_up_left_outlet_cen(prms):
    return 0

def A22_A22_up_left_outlet_cen(prms):
    return 0

# Up-right corner
def m_p_up_right_outlet_cen(prms):
    return 1

def x1_v1_up_right_outlet_cen(prms):
    return -1

def x1_v1_up_right_outlet_down(prms):
    return 1

def x2_v2_up_right_outlet_cen(prms):
    return -1

def x2_v2_up_right_outlet_down(prms):
    return 1

def A11_A11_up_right_outlet_cen(prms):
    return 0

def A12_A12_up_right_outlet_cen(prms):
    return 0

def A22_A22_up_right_outlet_cen(prms):
    return 0

# Down-right corner
def m_p_down_right_outlet_cen(prms):
    return 1

def x1_v1_down_right_outlet_cen(prms):
    return -1

def x1_v1_down_right_outlet_up(prms):
    return 1

def x2_v2_down_right_outlet_cen(prms):
    return -1

def x2_v2_down_right_outlet_up(prms):
    return 1

def A11_A11_down_right_outlet_cen(prms):
    return 0

def A12_A12_down_right_outlet_cen(prms):
    return 0

def A22_A22_down_right_outlet_cen(prms):
    return 0

# Down-left corner
def m_p_down_left_outlet_cen(prms):
    return 1

def x1_v1_down_left_outlet_cen(prms):
    return -1

def x1_v1_down_left_outlet_up(prms):
    return 1

def x2_v2_down_left_outlet_cen(prms):
    return -1

def x2_v2_down_left_outlet_up(prms):
    return 1

def A11_A11_down_left_outlet_cen(prms):
    return 0

def A12_A12_down_left_outlet_cen(prms):
    return 0

def A22_A22_down_left_outlet_cen(prms):
    return 0


### Outer corners along the inlets ###

# Up-left corner
def m_p_up_left_inlet_cen(prms):
    return 0

def x1_v1_up_left_inlet_cen(prms):
    return 1

def x2_v2_up_left_inlet_cen(prms):
    return 1

def A11_A11_up_left_inlet_cen(prms):
    return 1

def A12_A12_up_left_inlet_cen(prms):
    return 1

def A22_A22_up_left_inlet_cen(prms):
    return 1

# Up-right corner
def m_p_up_right_inlet_cen(prms):
    return 0

def x1_v1_up_right_inlet_cen(prms):
    return 1

def x2_v2_up_right_inlet_cen(prms):
    return 1

def A11_A11_up_right_inlet_cen(prms):
    return 1

def A12_A12_up_right_inlet_cen(prms):
    return 1

def A22_A22_up_right_inlet_cen(prms):
    return 1

# Down-right corner
def m_p_down_right_inlet_cen(prms):
    return 0

def x1_v1_down_right_inlet_cen(prms):
    return 1

def x2_v2_down_right_inlet_cen(prms):
    return 1

def A11_A11_down_right_inlet_cen(prms):
    return 1

def A12_A12_down_right_inlet_cen(prms):
    return 1

def A22_A22_down_right_inlet_cen(prms):
    return 1

# Down-left corner
def m_p_down_left_inlet_cen(prms):
    return 0

def x1_v1_down_left_inlet_cen(prms):
    return 1

def x2_v2_down_left_inlet_cen(prms):
    return 1

def A11_A11_down_left_inlet_cen(prms):
    return 1

def A12_A12_down_left_inlet_cen(prms):
    return 1

def A22_A22_down_left_inlet_cen(prms):
    return 1
