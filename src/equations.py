#
# filename: equations.py
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Provides all necessary equations for the calculation of the
#          A-matrix based on the given data.
#

def equation_number():
    return 2


def get_equations():
    return [
        [ueq_u, ueq_v],
        [veq_u, veq_v]
    ]

def get_vars():
    return [
        "U:0",
        "A:0"
    ]


def ueq_u(u, v, k):
    """
    Calculate the u-component of the U matrix.
    """
    return v - k**2

def ueq_v(u, v, k):
    """
    Calculate the v-component of the U matrix.
    """
    return u

def veq_u(u, v, k):
    """
    Calculate the u-component of the V matrix.
    """
    return - 1j * k

def veq_v(u, v, k):
    """
    Calculate the v-component of the V matrix.
    """
    return 2 * v
