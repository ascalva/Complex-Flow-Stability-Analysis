def negate_threshold():
    return 1.05

def negate_attributes():
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
    x = "Points:0"
    for attr in negate_attributes():
        df.loc[df[x] > negate_threshold(), attr] *= -1


def bound(df):

    # Define bounding values
    x_min = 1.0
    x_max = 1.1
    y_min = 1.0
    y_max = 1.1
    z_val = 0.01

    # Define attribute names
    x = "Points:0"
    y = "Points:1"
    z = "Points:2"

    # Bound x-values
    df = df[(df[x] >= x_min) & (df[x] <= x_max)]

    # Bound y-values
    df = df[(df[y] >= y_min) & (df[y] <= y_max)]

    # Bound z-values
    df = df[df[z] == z_val]

    return df.reset_index()
