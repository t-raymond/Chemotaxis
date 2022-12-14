"""
Module to calculate system parameters
"""

from scipy.constants import Boltzmann as kB
from scipy.constants import gas_constant as R
from scipy.constants import pi
import numpy as np

def Diffusivity(T, eta, r):
    """
    Calculate diffusivity [m^2/s]
    """
    return kB * T / (6 * pi * eta * r)
    
def RateConstant(T, A, Ea, Tref = None):
    """
    Calculate rate and equilibrium constants
    """
    if Tref is None: return A * np.exp(-Ea / (R * T))
    else: return A * np.exp(-Ea / R * (1 / T - 1 / Tref))

def AdsorptionSites():
    """
    Calculate the number of adsorption sites per unit area [mol/m^2]
    """
    pass