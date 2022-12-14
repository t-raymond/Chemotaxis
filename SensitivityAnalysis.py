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

def Beta(fun, beta_vals, alpha, Keq, **kwargs):
    """
    Make 1D sensitivity analysis for parameter beta (with fixed alpha and Keq)
    """
    t_B = np.zeros(len(beta_vals))
    t_BL = np.zeros(len(beta_vals))
    
    for i, a in enumerate(beta_vals):
        t_B[i], t_BL[i] = fun(a, alpha, Keq, **kwargs)
       
    fig = SA_1D((beta_vals, beta_vals), (t_B, t_BL), ('Bulk','Boundary Layer'), r"$\beta$", r"$Fo_{m}$", r"Dimensionless Time to Linearity")
    
    return fig

def KEQ(fun, Keq_vals, alpha, beta, **kwargs):
    """
    Make 1D sensitivity analysis for parameter Keq (with fixed alpha and beta)
    """
    t_B = np.zeros(len(Keq_vals))
    t_BL = np.zeros(len(Keq_vals))
    
    for i, a in enumerate(Keq_vals):
        t_B[i], t_BL[i] = fun(a, alpha, beta, **kwargs)
       
    fig = SA_1D((Keq_vals, Keq_vals), (t_B, t_BL), ('Bulk','Boundary Layer'), "Keq", r"$Fo_{m}$", r"Dimensionless Time to Linearity")
    
    return fig
    
    pass

def Morris(fun, alpha_range, beta_range, Keq_range):
    """
    \\TODO
    
    Make Morris sensitivity analysis work for 3 dimensionless parameters (alpha, beta, Keq)
    
    alpha/beta/Keq range = array of [lower_bound, higher_bound]
    
    fun = linearization (return t_bulk, t_bl)
    """
    
    morris_problem = {
        'num_vars': 3,
        'names': ['alpha','beta','Keq'],
        'bounds': [alpha_range,
                beta_range,
                Keq_range], 
        'groups': None
    }

    num_levels = 4
    trajectories = 1000
    sample = ms.sample(morris_problem, trajectories, num_levels = num_levels)
    sample.shape
    output_bulk, output_BL = [],[]
    for i in range(0, len(sample)):
        bulk, BL = fun(*sample[i])
        output_bulk.append(bulk)
        output_BL.append(BL)

    #BULK ANALYSIS
    Si_bulk = ma.analyze(morris_problem,
                sample,
                output_bulk,
                print_to_console=False,
                num_levels=num_levels)

    print("{:20s} {:>7s} {:>7s} {:>7s}".format("Name", "mu", "mu_star", "sigma"))
    for name, s1, st, mean in zip(morris_problem['names'], Si['mu'], Si['mu_star'], Si['sigma']):
        print("{:20s} {:=7.2f} {:=7.2f} {:=7.2f}".format(name, s1, st, mean))
        
    fig_bulk, (ax1, ax2) = plt.subplots(1,2)
    mp.horizontal_bar_plot(ax1, Si_bulk) #  param_dict={}
    mp.covariance_plot(ax2, Si_bulk, {})
    
    #BL ANALYSIS
    Si_BL = ma.analyze(morris_problem,
            sample,
            output_BL,
            print_to_console=False,
            num_levels=num_levels)

    print("{:20s} {:>7s} {:>7s} {:>7s}".format("Name", "mu", "mu_star", "sigma"))
    for name, s1, st, mean in zip(morris_problem['names'], Si['mu'], Si['mu_star'], Si['sigma']):
        print("{:20s} {:=7.2f} {:=7.2f} {:=7.2f}".format(name, s1, st, mean))
        
    fig_BL, (ax1, ax2) = plt.subplots(1,2)
    mp.horizontal_bar_plot(ax1, Si_BL) #  param_dict={}
    mp.covariance_plot(ax2, Si_BL, {})


    return fig_bulk, fig_BL
