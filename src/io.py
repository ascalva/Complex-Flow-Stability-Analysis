import numpy as np
import pandas as pd

INT_PATH = "intermediate_data/"

def save_matrix_to_ml(F, G_B, filename = "sparse_matrices"):
    """
    Saves F and G_B matrices to matlab file for later eigenvalue computation.
    The sparse form of the matries is preserved to keep the data memory
    efficient.
    """
    from scipy.io import savemat

    savemat(filename, {"G_B": G_B, "F": F})


def check_dataframe(filename):
    """
    Checks if there exists a pickle file with the given file name within the
    intermediate_data directory.
    Returns True if the file exists, False otherwise.
    """
    from os.path import isfile

    if isfile( INT_PATH + filename ):
        return True

    else: return False


def save_dataframe(df, filename):
    """
    Serialize the given dataframe and save for later.
    """
    df.to_pickle(INT_PATH + filename)


def read_dataframe(filename):
    """
    Read in dataframe from a pickle file with the name supplied. It is assumed
    that the file exists.
    """
    return pd.read_pickle(INT_PATH + filename)
