import pandas as pd

from src.preprocess import bound, negate
from src.routines import run_range_2k

def main():

    # Create data frame with simulation data.
    # out.csv is pre-filtered data from a 90-degree bend flow.
    # Simulation properties include: De = 5, delta = 1e-2, shear banding
    filename = "data/OB_crossslot_symmetric_De0.37.csv"
    df       = pd.read_csv(filename)

    # Clean up data
    df = bound(df)

    # Create A matrices for different values of k
    k_minits = (1,3)
    run_range_2k(df, k_minits)


main()
