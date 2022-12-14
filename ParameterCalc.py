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

def AdsorptionSites(particle_radius, nf_radius, nf_concentration):
    """
    Calculate the number of adsorption sites per unit area [mol/m^2]
    
    nf_radius range from .15 to 1.0 um (.15e-6 to 1e-6)
    nf_concentration range from 0 to 1/(2*nf_radius)
    """
 
    a_particle = (6/np.sqrt(3)) * particle_radius **2
        
    default_area = 1 #unit area without nanofibers
    
    sa_nf = np.pi*nf_radius
    
    additional_sa_nf = (sa_nf - 2*nf_radius)*nf_concentration #addition of fibers increases surface area
    
    area = default_area + additional_sa_nf
    
    ads_sites = area/a_particle #particles/m^2
    
    '''
    6.02e23 particles/1mol
    '''
    mol_max_ads = ads_sites/6.02e23 #mol/m^2
    
    return mol_max_ads
