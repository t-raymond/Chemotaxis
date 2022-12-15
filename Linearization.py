"""
Module containing functions relating to determination of linearity
"""

from Solver import solve_pde
import numpy as np
from scipy.stats import linregress

def time_to_linearize(C_profile, t_array, dist_array, desired_linearity):
    '''
    C_profile is list of concentration profile arrays at each time
    
    C_profile = [C_timestamp(t=0), C_timestamp(t=1),..]
    C_timestamp = [C(x=0),C(x=1),....]
    
    dist_array = list of distances. Single 1-D array
    '''
    
    for i, C in enumerate(C_profile):
        
        try:
            regress_results = linregress(C, dist_array)
            linearity = 1 - regress_results.stderr
        except:
            linearity = np.NAN
        
        if linearity >= desired_linearity:
            return t_array[i]
        else:
            continue
    
    return False

def linearization(lambda_d, lambda_h, k_A, k_eq, theta_S, linearity = 0.99):
    """
    Determines the time to linearity for bulk and boundary layers
    """

    # Solver parameters
    seg = 101      # Number of length segments
    tf = 1.0E5      # Final time

    # Boundary conditions
    theta_BC = np.array((1., 0.))

    # Initial conditions
    theta_IC = np.zeros(3 * seg)
    
    # Solve PDEs
    sol = solve_pde(tf, theta_IC, theta_BC, lambda_d, lambda_h, k_A, k_eq, theta_S)

    # Unpack solution
    t = np.logspace(np.log10(tf) - 10, np.log10(tf), 1001)
    theta_B, theta_BL, theta_Ads = np.split(sol.sol(t), 3)
    
    t_B = time_to_linearize(theta_B.T, t, np.linspace(0, 1, seg), linearity)
    t_BL = time_to_linearize(theta_BL.T, t, np.linspace(0, 1, seg), linearity)

    return [t_B, t_BL]