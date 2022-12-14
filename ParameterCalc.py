"""
Module to calculate system parameters
"""

from scipy.constants import Boltzmann as kB
from scipy.constants import gas_constant as R
from scipy.constants import pi
import numpy as np

def Diffusivity(T, eta, r):
    return kB * T / (6 * pi * eta * r)
    
def RateConstant(T, A, Ea, Tref = None):
    if Tref is None: return A * np.exp(-Ea / (R * T))
    else: return A * np.exp(-Ea / R * (1 / T - 1 / Tref))
