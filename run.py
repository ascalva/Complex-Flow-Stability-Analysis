import pandas as pd

from src.preprocess import bound, negate
from src.routines import run_range_2k

def main():

    # Create data frame with simulation data.
    # out.csv is pre-filtered data from a 90-degree bend flow.
    # Simulation properties include: De = 5, delta = 1e-2, shear banding
    filename = "data/OB_crossslot_symmetric_De0.37.csv"
    df       = pd.read_csv(filename)

    # Bound data
    df = bound(df)

    # Fix values in data by negating those on right side
    negate(df)

    # Create A matrices for different values of k
    k_limits = (1,2)
    run_range_2k(df, k_limits)


main()
