import pandas as pd
import argparse
from src.preprocess import bound, negate, non_dimensionalize, deduplicate
from src.routines import run_range_2k

def main2():
    from src.parameters import FILENAME, change_filename
    print(FILENAME)
    change_filename("hello")

    from src.parameters import FILENAME
    print(FILENAME)
    
def main():
    # Default values
    filename = "data/OB_crossslot_symmetric_De0.36.csv"
    k_limits = (1,3)

    # Create argument parser
    ap = argparse.ArgumentParser(description="Create sparse matrix from data and more")

    # Add file argument
    ap.add_argument(
        "-f",
        "--file",
        type=str,
        help="Name csv file",
        default=filename
    )

    # Add k-value(s) argument
    ap.add_argument(
        "-kR",
        "--krange",
        type=int,
        nargs="+",
        help="Range of k-values",
        default=k_limits
    )

    # ap.add_argument("-kV", "--kvalues", type=list, help="Value(s) of k", default=k_limits)

    # Parse arguments
    args = vars(ap.parse_args())

    # Create data frame with simulation data.
    # out.csv is pre-filtered data from a 90-degree bend flow.
    # Simulation properties include: De = 5, delta = 1e-2, shear banding
    df = pd.read_csv(args["file"])

    # Bound data
    df = bound(df)

    # Fix values in data by negating those on right side
    negate(df)

    # Convert dimensional data into non-dimensionalized
    non_dimensionalize(df)

    # Remove duplicate values, typically occur on the line of symmetry
    # Updates indices
    deduplicate(df, up_index=True)

    # Create A matrices for different values of k
    run_range_2k(df, args["krange"])


main()
