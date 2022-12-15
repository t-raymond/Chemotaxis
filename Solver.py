"""
Module containing functions relating to solving system of characteristic PDEs
"""

from scipy.integrate import solve_ivp
import numpy as np

def AdsIsotherm(C, Keq = 1):
    C_Ads_eq = Keq * C / (1 + Keq + C)
    return C_Ads_eq

def PDE(t, y, y_BC, lambda_d, lambda_h, k_A, k_eq, theta_S):
    """
    PDE discretized in length as a system of coupled ODEs in time
    """

    nx = int(len(y) / 3)
    dydt_B, dydt_BL, dydt_A = np.array_split(np.zeros_like(y), 3)

    y_B, y_BL, y_A = np.array_split(y, 3)

    y_BC = np.hstack((y_BC[0] * np.ones(4), y_BC[1] * np.ones(4)))
    y_B = np.insert(y_BC, int(len(y_BC) / 2), y_B)

    capacity_factor = lambda_d / (lambda_h - lambda_d)

    r_diffusion = np.array([(-1 / 560 * y_B[i] + 8 / 315 * y_B[i + 1] - 1 / 5 * y_B[i + 2] + 8 / 5 * y_B[i + 3] - 205 / 72 * y_B[i + 4] + 8 / 5 * y_B[i + 5] - 1 / 5 * y_B[i + 6] + 8 / 315 * y_B[i + 7] - 1 / 560 * y_B[i + 8]) * nx ** 2 for i in range(nx)])
    r_boundary = np.array([(y_B[i + 4] - y_BL[i]) / lambda_d ** 2 / capacity_factor for i in range(nx)])
    r_adsorption = np.array([k_A * (AdsIsotherm(y_BL[i], k_eq) - y_A[i]) / lambda_d ** 2 for i in range (nx)])

    dydt_B = r_diffusion - capacity_factor ** 2 * r_boundary
    dydt_BL = r_boundary - theta_S * r_adsorption
    dydt_A = r_adsorption

    return np.hstack((dydt_B, dydt_BL, dydt_A))


def solve_pde(tf, y0, y_BC, lambda_d, lambda_h, k_A, k_eq, theta_S):
    """
    Implementation of SciPy solve_ivp to solve system of spatially-discretized PDEs
    """

    a = (y_BC, lambda_d, lambda_h, k_A, k_eq, theta_S)
    
    sol = solve_ivp(
        PDE, 
        (0., tf), 
        y0, 
        method = 'BDF',
        dense_output = True,
        args = a,
        )

    return sol

if __name__ == "__main__":
    tf = 1.0E8
    y0 = np.zeros(3 * 1001)
    y_BC = np.array((1.0, 0.0))
    lambda_d = 1.0E-6 / 11.0E-3
    lambda_h = 1.0E-3 / 11.0E-3
    k_A = 1.0E3
    k_eq = 1.0E-3
    theta_S = 50.0E-9

    sol = solve_pde(tf, y0, y_BC, lambda_d, lambda_h, k_A, k_eq, theta_S)
    print(sol)