import pandas as pd

from src.create import create_matrix_A, create_matrix_B
from src.eigs import remove_inf_eigs

def main():

    # Create data frame with simulation data.
    # out.csv is pre-filtered data from a 90-degree bend flow.
    # Simulation properties include: De = 5, delta = 1e-2, shear banding
    filename = "./data/out.csv"
    df = pd.read_csv(filename)

    # Build pre-configured A,B matrices with simulation data
    A  = create_matrix_A(df)
    B  = create_matrix_B(df.size)

    # Remove infinite eigen values (map them to smaller values) and save the
    # resulting matrices as sparse matrices in a matlab file.
    remove_inf_eigs(A, B, sparse = True, save_matrix = True)


main()
