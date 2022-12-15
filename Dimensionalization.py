"""
Module to dimensionalize or nondimensionalize values
"""

def dimensionalize(theta_B, theta_BL, Fo_m, lambda_x):
    """
    Dimensionalize nondimensional parameters
    """
    
    pass

def nondimensionalize(L, h, d, D, k_Ads, K_eq, C0, S0):
    """
    Nondimensionalize dimensional parameters
    """
    
    lambda_d = d / L
    lambda_h = h / L
    k_A = k_Ads * d ** 2 / D
    k_eq = K_eq * C0
    theta_S = S0 / (d * C0)

    return lambda_d, lambda_h, k_A, k_eq, theta_S