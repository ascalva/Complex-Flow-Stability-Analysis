import pandas as pd

from src.create import create_matrix_A, create_matrix_B
from src.eigs import remove_inf_eigs, save_matrix_to_ml
from src.preprocess import bound, negate

def k2_routine(df, limits, filename = "sparse_matrices", dirname = "out"):

    B = create_matrix_B(df.shape[0])

    for k_1 in range(limits[0], limits[1]):
        for k_2 in range(limits[0], limits[1]):

            A      = create_matrix_A(df, [k_1, k_2])
            F, G_B = remove_inf_eigs(A, B)

            # Save sparse matrices to matlab file for later computation
            # of eigenvalues.
            save_matrix_to_ml(
                F, G_B,
                "{0}/{1}_{2}_{3}".format(dirname, filename, k_1, k_2)
            )

def main():

    # Create data frame with simulation data.
    # out.csv is pre-filtered data from a 90-degree bend flow.
    # Simulation properties include: De = 5, delta = 1e-2, shear banding
    # filename = "./data/flow_data.csv"
    filename = "data/OB_crossslot_symmetric_De0.37.csv"
    df       = pd.read_csv(filename)

    # Clean up data
    df = bound(df)

    # K-values
    # k = [1,2]

    # Build pre-configured A,B matrices with simulation data
    # A  = create_matrix_A(df, k)
    # B  = create_matrix_B(df.shape[0])


    # Remove infinite eigen values (map them to smaller values) and save the
    # resulting matrices as sparse matrices in a matlab file.
    # remove_inf_eigs(A, B, save_matrix = True)

    k_minits = (1,3)
    k2_routine(df, k_minits)


main()
