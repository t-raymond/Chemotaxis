"""
Module to dimensionalize or nondimensionalize values
"""

def dimensionalize(alpha, beta):
    """
    Dimensionalize nondimensional parameters
    """
    
    pass

def nondimensionalize(L, D, k, k_Ads):
    """
    Nondimensionalize dimensional parameters
    """
    
    alpha = k * L * L / D
    beta = k_Ads / k

    return alpha, beta