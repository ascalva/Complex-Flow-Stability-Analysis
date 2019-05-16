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
    
def A11_A11_bound(prms):
    return 1

def A12_A12_bound(prms):
    return 1

def A22_A22_bound(prms):
    return 1

def x1_v1_bound(prms):
    return 1

def x2_v2_bound(prms):
    return 1

def m_p_bound(prms):
    return 1

def inner_corner_bound(prms):
    return 1
