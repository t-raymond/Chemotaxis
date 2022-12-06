from scipy.integrate import solve_ivp
import numpy as np


def PDE(t, y, y_BC, alpha, nx):
    """
    PDE discretized in length as a system of coupled ODEs in time
    """

    dydt_B = np.zeros(nx)
    dydt_BL = np.zeros(nx)

    y_B = np.insert(y_BC, 1, y[0:nx])
    y_BL = y[nx:]

    dydt_BL = np.array([alpha * (y_B[i + 1] - y_BL[i]) for i in range(nx)])
    dydt_B = np.array([-dydt_BL[i] + (y_B[i] - 2 * y_B[i + 1] + y_B[i + 2]) * nx * nx for i in range(nx)])

    return np.hstack((dydt_B, dydt_BL))


def solve_pde(tf, y0, y_BC, alpha):
    """
    Implementation of SciPy solve_ivp to solve system of spatially-discretized PDEs
    """

    a = (y_BC, alpha, int(len(y0) / 2))
    
    sol = solve_ivp(
        PDE, 
        (0., tf), 
        y0, 
        method = 'RK45', 
        t_eval = np.linspace(0, tf, 1001),
        args = a,
        )

    return sol

if __name__ == "__main__":
    tf = 2.0
    y0 = np.zeros(2 * 100)
    y_BC = np.array((1.0, 0.0))
    alpha = 5.

    sol = solve_pde(tf, y0, y_BC, alpha)
    print(sol)