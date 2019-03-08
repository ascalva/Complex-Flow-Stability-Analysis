#
# filename: preprocess.py
#
# @author: Alberto Serrano
#
# purpose: All functions used to clean, filter, or alter data before matrix
#          computation exist here.
#

# Define bounding values
X_MIN = 1.0
X_MAX = 1.1
Y_MIN = 1.0
Y_MAX = 1.1
Z_VAL = 0.01


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

def negate(df):
    """
    Negates the values of specific attributes to the right of a threshold.
    """
    x = "Points:0"
    for attr in negate_attributes():
        df.loc[df[x] > negate_threshold(), attr] *= -1


def bound(df):
    """
    Using the bounding conditions above, filters out data not in that range.
    """

    # Define attribute names
    x = "Points:0"
    y = "Points:1"
    z = "Points:2"

    # Bound x-values
    df = df[(df[x] >= X_MIN) & (df[x] <= X_MAX)]

    # Bound y-values
    df = df[(df[y] >= Y_MIN) & (df[y] <= Y_MAX)]

    # Bound z-values
    df = df[df[z] == Z_VAL]

    return df.reset_index(drop=True)
