import pandas as pd
import argparse

from src.preprocess import bound, negate, non_dimensionalize, deduplicate
from src.create     import build_coefficient_matrix
from src.eigs       import remove_inf_eigs
from src.io         import *

#
# filename: run.py
#
# @author: Alberto Serrano
#
# purpose:
#

DATA_FILENAME = "data/OB_crossslot_symmetric_De0.36.csv"
MTLB_FILENAME = "out/coefficient_matrices"

def init(args):
    """
    Initialize data by using preexisting dataframe in pickle file. If there is
    no file, read in the csv file and preprocess the data. Save the preprocessed
    data into a pickle file for later use.
    """
    filename = "".join(args["file"].split("/")[-1].split(".")[:-1])

    # Check if preprocessed data frame exists in intermediate_data directory
    if check_dataframe(filename):
        print("Loading preexisting pickle file: {0}".format(filename))

        df = read_dataframe(filename)

    # If preprocessed data does not exist, load raw data and preprocess
    else:
        path = args["file"]
        print("Reading in file: {0}".format(path))

        # Create data frame with simulation data.
        # out.csv is pre-filtered data from a 90-degree bend flow.
        # Simulation properties include: De = 5, delta = 1e-2, shear banding
        df = pd.read_csv(path)

        # Bound data
        df = bound(df)

        # Fix values in data by negating those on right side
        negate(df)

        # Convert dimensional data into non-dimensionalized
        non_dimensionalize(df)

        # Remove duplicate values, typically occur on the line of symmetry
        # Updates indices
        deduplicate(df, up_index=True)

        # Save dataframe for later use
        save_dataframe(df, filename)

    return df


def coefficient_matrix_setup(df):

    # Run with neighbor implementation
    A,B_ = build_coefficient_matrix(df)

    # Remove infinite eigenvalues
    # F, G_B = remove_inf_eigs(A, B)

    # Save coefficient matrices
    save_matrix_to_ml(A,B_, MTLB_FILENAME)


def main():

    # Create argument parser
    ap = argparse.ArgumentParser(description="Create sparse matrix from data and more")

    # Add file argument
    ap.add_argument(
        "-f",
        "--file",
        type=str,
        help="Name csv file",
        default=DATA_FILENAME
    )

    # Parse arguments
    args = vars(ap.parse_args())

    # Load data frame
    df = init(args)

    coefficient_matrix_setup(df)


main()
