import numpy as np
from Plots import SA_1D
from SALib.sample import morris as ms
from SALib.analyze import morris as ma
from SALib.plotting import morris as mp
import matplotlib.pyplot as plt

def Alpha(fun):
    num_pts = 51
    A = np.logspace(-5, 5, num_pts)
    t_B = np.zeros(num_pts)
    t_BL = np.zeros(num_pts)

    for i, a in enumerate(A):
        t_B[i], t_BL[i] = fun(linearity = 0.95, alpha = a, beta = 1., Keq = 3.)

    fig = SA_1D((A, A), (t_B, t_BL), ("Bulk", "Boundary Layer"), r"$\alpha$", r"$Fo_{m}$", r"Dimensionless Time to Linearity")

    return fig

def Beta(fun):
    pass

def KEQ(fun):
    pass

def Morris():
    morris_problem = {
        'num_vars': 3,
        'names': ['alpha','beta','Keq'],
        'bounds': [[15, 90],
                [8000,20000],
                [.1, 20]], 
        'groups': None
    }

    num_levels = 4
    trajectories = 1000
    sample = ms.sample(morris_problem, trajectories, num_levels = num_levels)
    sample.shape
    output = sample.T

    Si = ma.analyze(morris_problem,
                sample,
                output,
                print_to_console=False,
                num_levels=num_levels)

    print("{:20s} {:>7s} {:>7s} {:>7s}".format("Name", "mu", "mu_star", "sigma"))
    for name, s1, st, mean in zip(morris_problem['names'], Si['mu'], Si['mu_star'], Si['sigma']):
        print("{:20s} {:=7.2f} {:=7.2f} {:=7.2f}".format(name, s1, st, mean))
        
    fig, (ax1, ax2) = plt.subplots(1,2)
    mp.horizontal_bar_plot(ax1, Si) #  param_dict={}
    mp.covariance_plot(ax2, Si, {})

    return fig
