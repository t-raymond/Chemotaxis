"""
Module containing functions relating to sensitivity analyses
"""

import numpy as np
from Plots import SA_1D
from SALib.sample.morris import morris as ms
from SALib.analyze import morris as ma
from SALib.plotting import morris as mp
import matplotlib.pyplot as plt

def LAMBDA_D(fun, lambda_d_vals, lambda_h, k_A, k_eq, theta_S, **kwargs):
    """
    1D sensitivity analysis for parameter lambda_d (with all other parameters fixed)
    """
    
    t_B  = np.zeros(len(lambda_d_vals))
    t_BL = np.zeros(len(lambda_d_vals))

    for i, lambda_d in enumerate(lambda_d_vals):
        t_B[i], t_BL[i] = fun(lambda_d, lambda_h, k_A, k_eq, theta_S, **kwargs)

    fig = SA_1D((lambda_d_vals, lambda_d_vals), (t_B, t_BL), ("Bulk", "Boundary Layer"), r"$\lambda_{d}$", r"$Fo_{m}$", r"Dimensionless Time to Linearity")

    return fig

def LAMBDA_H(fun, lambda_h_vals, lambda_d, k_A, k_eq, theta_S, **kwargs):
    """
    1D sensitivity analysis for parameter lambda_h (with all other parameters fixed)
    """
    
    t_B  = np.zeros(len(lambda_h_vals))
    t_BL = np.zeros(len(lambda_h_vals))

    for i, lambda_h in enumerate(lambda_h_vals):
        t_B[i], t_BL[i] = fun(lambda_d, lambda_h, k_A, k_eq, theta_S, **kwargs)

    fig = SA_1D((lambda_h_vals, lambda_h_vals), (t_B, t_BL), ("Bulk", "Boundary Layer"), r"$\lambda_{h}$", r"$Fo_{m}$", r"Dimensionless Time to Linearity")

    return fig

def K_A(fun, k_A_vals, lambda_d, lambda_h, k_eq, theta_S, **kwargs):
    """
    1D sensitivity analysis for parameter k_A (with all other parameters fixed)
    """
    
    t_B  = np.zeros(len(k_A_vals))
    t_BL = np.zeros(len(k_A_vals))

    for i, k_A in enumerate(k_A_vals):
        t_B[i], t_BL[i] = fun(lambda_d, lambda_h, k_A, k_eq, theta_S, **kwargs)

    fig = SA_1D((k_A_vals, k_A_vals), (t_B, t_BL), ("Bulk", "Boundary Layer"), r"$\kappa_{A}$", r"$Fo_{m}$", r"Dimensionless Time to Linearity")

    return fig

def K_EQ(fun, k_eq_vals, lambda_d, lambda_h, k_A, theta_S, **kwargs):
    """
    1D sensitivity analysis for parameter k_A (with all other parameters fixed)
    """
    
    t_B  = np.zeros(len(k_eq_vals))
    t_BL = np.zeros(len(k_eq_vals))

    for i, k_eq in enumerate(k_eq_vals):
        t_B[i], t_BL[i] = fun(lambda_d, lambda_h, k_A, k_eq, theta_S, **kwargs)

    fig = SA_1D((k_eq_vals, k_eq_vals), (t_B, t_BL), ("Bulk", "Boundary Layer"), r"$\kappa_{eq}$", r"$Fo_{m}$", r"Dimensionless Time to Linearity")

    return fig

def THETA_S(fun, theta_S_vals, lambda_d, lambda_h, k_A, k_eq, **kwargs):
    """
    1D sensitivity analysis for parameter k_A (with all other parameters fixed)
    """
    
    t_B  = np.zeros(len(theta_S_vals))
    t_BL = np.zeros(len(theta_S_vals))

    for i, theta_S in enumerate(theta_S_vals):
        t_B[i], t_BL[i] = fun(lambda_d, lambda_h, k_A, k_eq, theta_S, **kwargs)

    fig = SA_1D((theta_S_vals, theta_S_vals), (t_B, t_BL), ("Bulk", "Boundary Layer"), r"$\theta_{S}$", r"$Fo_{m}$", r"Dimensionless Time to Linearity")

    return fig

def Morris(fun, lambda_d_range, lambda_h_range, k_A_range, k_eq_range, theta_S_range):
    """
    \\TODO
    
    Make Morris sensitivity analysis work for 3 dimensionless parameters (alpha, beta, Keq)
    
    alpha/beta/Keq range = array of [lower_bound, higher_bound]
    
    fun = linearization (return t_bulk, t_bl)
    """
    
    morris_problem = {
        'num_vars': 5,
        'names': ['Log_lambda_d', 'Log_lambda_h', 'Log_k_A', 'Log_k_eq', 'Log_theta_S'],
        'bounds': np.log10([lambda_d_range,
                lambda_h_range,
                k_A_range,
                k_eq_range, 
                theta_S_range]), 
        'groups': None
    }

    num_levels = 4
    trajectories = 10
    sample = ms.sample(morris_problem, trajectories, num_levels = num_levels)
    output_B, output_BL = [],[]
    for i in range(0, len(sample)):
        s = np.float_power(10., sample[i])
        B, BL = fun(*s)
        output_B.append(B)
        output_BL.append(BL)

    output_B = np.array(output_B)
    output_BL = np.array(output_BL)

    #BULK ANALYSIS
    Si_B = ma.analyze(morris_problem,
                sample,
                output_B,
                print_to_console=False,
                num_levels=num_levels)

    print("{:20s} {:>7s} {:>7s} {:>7s}".format("Name", "mu", "mu_star", "sigma"))
    for name, s1, st, mean in zip(morris_problem['names'], Si_B['mu'], Si_B['mu_star'], Si_B['sigma']):
        print("{:20s} {:=7.2f} {:=7.2f} {:=7.2f}".format(name, s1, st, mean))
        
    fig_B, (ax1, ax2) = plt.subplots(1,2)
    mp.horizontal_bar_plot(ax1, Si_B) #  param_dict={}
    mp.covariance_plot(ax2, Si_B, {})
    fig_B.xscale('log')
    
    #BL ANALYSIS
    Si_BL = ma.analyze(morris_problem,
            sample,
            output_BL,
            print_to_console=False,
            num_levels=num_levels)

    print("{:20s} {:>7s} {:>7s} {:>7s}".format("Name", "mu", "mu_star", "sigma"))
    for name, s1, st, mean in zip(morris_problem['names'], Si_BL['mu'], Si_BL['mu_star'], Si_BL['sigma']):
        print("{:20s} {:=7.2f} {:=7.2f} {:=7.2f}".format(name, s1, st, mean))
        
    fig_BL, (ax1, ax2) = plt.subplots(1,2)
    mp.horizontal_bar_plot(ax1, Si_BL) #  param_dict={}
    mp.covariance_plot(ax2, Si_BL, {})
    fig_BL.xscale('log')


    return fig_B, fig_BL
