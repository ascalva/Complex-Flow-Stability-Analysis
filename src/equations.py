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
