import pandas as pd

from src.create import create_matrix_A, create_matrix_B
from src.eigs import remove_inf_eigs

def preprocess(df):

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

    return df


def main():

    # Create data frame with simulation data.
    # out.csv is pre-filtered data from a 90-degree bend flow.
    # Simulation properties include: De = 5, delta = 1e-2, shear banding
    # filename = "./data/flow_data.csv"
    filename = "data/OB_crossslot_symmetric_De0.37.csv"
    df       = pd.read_csv(filename)

    # Clean up data
    df = preprocess(df)

    # K-values
    k = [1,2]

    # Build pre-configured A,B matrices with simulation data
    A  = create_matrix_A(df, k)
    B  = create_matrix_B(df.size)

    # Remove infinite eigen values (map them to smaller values) and save the
    # resulting matrices as sparse matrices in a matlab file.
    remove_inf_eigs(A, B, save_matrix = True)


main()
