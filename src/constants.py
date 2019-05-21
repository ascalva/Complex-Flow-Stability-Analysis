from enum  import Enum

from .     import OB_equations2 as eqF
from .     import boundary_conditions as BC
from .misc import get_func_name

# Define bounding values
X_MIN         = 0.977#0.95
X_MAX         = 1.123#1.15
Y_MIN         = 0.977
Y_MAX         = 1.123
Z_VAL         = 0.01

# Neighbor info
NEIGHBOR_NUM  = 5
NEIGHBOR_LOC  = ["cen", "up", "down", "left", "right"]
CHANNEL_TYPE  = ["inlet", "outlet"]
BOUND_NAME    = "bound"
NEIGHBOR      = dict((v,k) for k,v in enumerate(NEIGHBOR_LOC))

# System parameters
H             = eqF.H
DX            = eqF.DX
DY            = eqF.DY
LAMBDA        = eqF.LAMBDA
COORD         = eqF.COORD

ATTRIBUTES    = eqF.get_vars()

# Simulation parameters
LOAD_INTERVAL = 500
COORD_TOL     = 0.001
