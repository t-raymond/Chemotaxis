"""
Module containing functions relating to solving system of characteristic PDEs
"""

from scipy.integrate import solve_ivp
import numpy as np

def AdsIsotherm(C, Keq = 1):
    C_Ads_eq = Keq * C / (1 + Keq + C)
    return C_Ads_eq

def PDE(t, y, y_BC, alpha, beta, Keq, nx):
    """
    PDE discretized in length as a system of coupled ODEs in time
    """

    dydt_B = np.zeros(nx)
    dydt_BL = np.zeros(nx)
    dydt_Ads = np.zeros(nx)

    y_B, y_BL, y_Ads = np.array_split(y, 3)
    y_B = np.insert(y_BC, 1, y_B)

    dydt_BL = np.array([alpha * (y_B[i + 1] - y_BL[i]) for i in range(nx)])
    dydt_B = np.array([-dydt_BL[i] + (y_B[i] - 2 * y_B[i + 1] + y_B[i + 2]) * nx * nx for i in range(nx)])
    dydt_Ads = np.array([alpha * beta * (AdsIsotherm(y_BL[i], Keq) - y_Ads[i]) for i in range (nx)])

    return np.hstack((dydt_B, dydt_BL, dydt_Ads))


def solve_pde(tf, y0, y_BC, alpha, beta, Keq):
    """
    Implementation of SciPy solve_ivp to solve system of spatially-discretized PDEs
    """

    nx = int(len(y0) / 3)
    a = (y_BC, alpha, beta, Keq, nx)
    
    sol = solve_ivp(
        PDE, 
        (0., tf), 
        y0, 
        method = 'LSODA', 
        t_eval = np.logspace(np.log10(tf) - 5, np.log10(tf), 1001),
        args = a,
        )

    return sol

if __name__ == "__main__":
    tf = 100.
    y0 = np.zeros(3 * 100)
    y_BC = np.array((1.0, 0.0))
    alpha = 5.
    beta = 1.
    Keq = 3.

    sol = solve_pde(tf, y0, y_BC, alpha, beta, Keq)
    print(sol)