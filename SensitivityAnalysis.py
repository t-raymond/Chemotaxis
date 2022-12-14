"""
Module containing functions relating to sensitivity analyses
"""

import numpy as np
from Plots import SA_1D
from SALib.sample import morris as ms
from SALib.analyze import morris as ma
from SALib.plotting import morris as mp
import matplotlib.pyplot as plt

def Alpha(fun, alpha_vals, beta, Keq, **kwargs):
    """
    1D sensitivity analysis for parameter alpha (with fixed beta and Keq)
    """
    
    t_B  = np.zeros(len(alpha_vals))
    t_BL = np.zeros(len(alpha_vals))

    for i, a in enumerate(alpha_vals):
        t_B[i], t_BL[i] = fun(a, beta, Keq, **kwargs)

    fig = SA_1D((alpha_vals, alpha_vals), (t_B, t_BL), ("Bulk", "Boundary Layer"), r"$\alpha$", r"$Fo_{m}$", r"Dimensionless Time to Linearity")

    return fig

def Beta(fun):
    """
    \\TODO

    Make 1D sensitivity analysis for parameter beta (with fixed alpha and Keq)
    """
    
    pass

def KEQ(fun):
    """
    \\TODO

    Make 1D sensitivity analysis for parameter Keq (with fixed alpha and beta)
    """
    
    pass

def Morris():
    """
    \\TODO
    
    Make Morris sensitivity analysis work for 3 dimensionless parameters (alpha, beta, Keq)
    """
    
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
