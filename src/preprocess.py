#
# filename: preprocess.py
#
# @author: Alberto Serrano
#
# purpose: All functions used to clean, filter, or alter data before matrix
#          computation exist here.
#

from .OB_equations2 import LAMBDA, H, get_vars

# Define bounding values
X_MIN = 0.95
X_MAX = 1.15
Y_MIN = 0.95
Y_MAX = 1.15
Z_VAL = 0.01

COORD = (
    "Points:0",
     "Points:1",
     "Points:2"
)


def update_index(df):
    """
    Update the indices of a data frame in place so that indeces are sequential
    """
    df.reset_index(drop=True, inplace=True)


def deduplicate(df, up_index=False):
    """
    Remove rows that share the same coordinates (location), keep the first one
    found at the specific coordinates.
    """
    df.drop_duplicates(
        subset=COORD,
        keep='first',
        inplace=True
    )

    if up_index: update_index(df)


def negate_threshold():
    """
    Values (for specific attribute) above threshold will be negated.
    """
    return 1.05


def negate_attributes():
    """
    Return a list of attributes where their values will be negated above the
    specified threshold.
    """
    return [
        "A:1",            # A_12
        "U:0",            # v_1
        "Gradients A:0",  # A_11
        "Gradients A:4",  # A_22
        "Gradients A:9",  # A_22
        "Gradients U:1",  # v_2x_1
        "Gradients U:4"   # v_2x_2
    ]

def negate(df, up_index=False):
    """
    Negates the values of specific attributes to the right of a threshold.
    """
    x = COORD[0]
    for attr in negate_attributes():
        df.loc[df[x] > negate_threshold(), attr] *= -1

    if up_index: update_index(df)


def non_dimensionalize_U(df):
    #TODO: make more dynamic
    for attr in get_vars()[3:5]:
        df.loc[:, attr] *= LAMBDA / H


def non_dimensionalize_gradU(df):
    #TODO: make more dynamic
    for attr in get_vars()[11:]:
        df.loc[:, attr] *= LAMBDA


def non_dimensionalize_gradA(df):
    #TODO: make more dynamic
    for attr in get_vars()[5:11]:
        df.loc[:, attr] *= H


def non_dimensionalize(df, up_index=False):
    """
    Data imported is dimensionalized, needs to be non-dimensionalized.
    """
    non_dimensionalize_U(df)
    non_dimensionalize_gradU(df)
    non_dimensionalize_gradA(df)

    if up_index: update_index(df)


def bound(df, up_index=False):
    """
    Using the bounding conditions above, filters out data not in that range.
    """

    # Define attribute names
    x = "Points:0"
    y = "Points:1"
    z = "Points:2"

    # Bound x-values
    df = df[(df[COORD[0]] >= X_MIN) & (df[COORD[0]] <= X_MAX)]

    # Bound y-values
    df = df[(df[COORD[1]] >= Y_MIN) & (df[COORD[1]] <= Y_MAX)]

    # Bound z-values
    df = df[df[COORD[2]] == Z_VAL]

    if up_index: update_index(df)

    return df
