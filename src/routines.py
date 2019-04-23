from .create import create_matrix_A, create_matrix_B
from .eigs import remove_inf_eigs, save_matrix_to_ml

#
# filename: routines.py
#
# @author: Alberto Serrano (axs4986)
#
# description: Provides different ways of automating the creation of
#              matrices with varying k-values.
#

def run_range_2k(df, limits, filename = "sparse_matrices", dirname = "out"):
    """
    Create an A-matrix for different combinations of k-values, where each
    k-value is in the range of limits = [min, max], and there are two
    k values required by the current set of equations [k_1, k_2].
    """

    # Create B-matrix
    B = create_matrix_B(df.shape[0])

    # Iterate over different values of k_1 and k_2
    for k_1 in range(limits[0], limits[1]):
        for k_2 in range(limits[0], limits[1]):

            # Create A-matrix with specific k combination
            A      = create_matrix_A(df, [k_1, k_2])

            # Remove infinite eigenvalues
            F, G_B = remove_inf_eigs(A, B)

            # Save sparse matrices to matlab file for later computation
            # of eigenvalues.
            save_matrix_to_ml(
                F, G_B,
                "{0}/{1}_{2}_{3}".format(dirname, filename, k_1, k_2)
            )


def run_specific_2k(df, kvalues, filename = "sparse_matrices", dirname = "out"):
    """
    Uses specified k-values to create A and B matrices and saves them into a
    matlab file.
    """

    # Create A-matrix with specific k combination
    A      = create_matrix_A(df, kvalues)

    # Create B-matrix
    B      = create_matrix_B(df.shape[0])

    # Remove infinite eigenvalues
    F, G_B = remove_inf_eigs(A, B)

    # Save sparse matrices to matlab file for later computation
    # of eigenvalues.
    save_matrix_to_ml(
        F, G_B,
        "{0}/{1}_{2}_{3}".format(dirname, filename, k_1, k_2)
    )
