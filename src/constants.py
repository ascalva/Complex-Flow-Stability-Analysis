from enum  import Enum

from . import OB_equations2       as eqF
from . import boundary_equations  as BC

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

# Equation information
EQ_NUM        = eqF.get_equation_number()
EQ_NAMES      = eqF.get_equation_names()
VAR_NAMES     = eqF.get_component_names()
ATTRIBUTES    = eqF.get_vars()

# Inner corner information
INNR_CRNR_LOC = BC.get_inner_corners()

# Simulation parameters
LOAD_INTERVAL = 500
COORD_TOL     = 0.001
DELIM         = "_"
