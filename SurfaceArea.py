import numpy as np
import math

def nanofiber_surfacearea(radius, concentration):
    '''
    radius = [L]
    concentration = [nanofibers/L] L in axis perpendicular to nanofiber direction
    
    SA of cylinder sides = 2*pi*r*h
    '''
    indiv_sa = 1 * math.pi * radius #[L]

    unit_sa = indiv_sa * concentration #[L/L]
    
    return unit_sa

    
def calc_area(radius = 0.25):
    """
    
    """

    # Fiber concentration cannot be more than 1/(fiber diameter) per unit

    concentration_range = []

    fiber_concentration = np.linspace(0, 1 / (2 * radius), 10)
    for j in fiber_concentration[1:]:
        concentration_range.append(nanofiber_surfacearea(radius, j))


    return np.mean(concentration_range)