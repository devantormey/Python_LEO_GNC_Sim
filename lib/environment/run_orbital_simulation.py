# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:09:44 2024

@author: Devan Tormey
this runs an orbital simulation that can be used to informed sattelite simulations
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#import eci_to_ecef
#import vernal_equinox_calculation

def run_orbital_simulation(altitude, inclination, n_orbits):
## ~~~~~~~~~~ Constants Definitions ~~~~~~~~~~~~
    # Gravitational Constant
    G = 6.67430e-11  # m^3 kg^-1 s^-2
    # Earth's Mass
    M = 5.972e24  # kg
    # Earth's radius in meters
    Re = 6.371e6  # Earth radius in meters
    
    
    ## ~~~~~~~~~~ Orbital Elements ~~~~~~~~~~~~
    # Orbital Elements needed to define our orbit
    #altitude = 500e3  # 500 km converted to meters
    i = inclination  # Inclination in radians, e.g., 28.5 degrees
    a = Re + altitude # Calculate the semi-major axis
    # non rotated initial position and velocity
    r0 = [Re + altitude, 0, 0]  # 500 km orbit initial condition
    # Calculate circular orbit velocity
    v0 = [0, np.sqrt(G * M / (Re + altitude)), 0]  # Initial velocity in m/s
    #number of orbits
    
    # Calculate the orbital period
    T = 2 * np.pi * np.sqrt(a**3 / (G * M))
    
    # Rotation matrix for inclination
    def rotation_matrix(i):
        return np.array([
            [1, 0, 0],
            [0, np.cos(i), -np.sin(i)],
            [0, np.sin(i), np.cos(i)]
        ])
    
    # Rotate initial position and velocity
    r0 = np.dot(rotation_matrix(i), r0)
    v0 = np.dot(rotation_matrix(i), v0)
    
    
    ## ~~~~~~~~~~ Orbital Dynamics ~~~~~~~~~~~~
    def orbit_dynamics(t, y):
        r = np.sqrt(y[0]**2 + y[1]**2 + y[2]**2) # Calculate the magnitude of the radius vector
        # Calculate the gravitational acceleration vector
        acc = -G * M / r**2 * np.array([y[0], y[1], y[2]]) / r
        return [y[3], y[4], y[5], acc[0], acc[1], acc[2]]
    
    # Time span for the simulation
    
    # Calculate total simulation time in seconds
    total_simulation_time = n_orbits * T
    
    t_span = [0, total_simulation_time]  # 12 hours
    y0 = np.concatenate((r0, v0))  # Correctly concatenate position and velocity vectors
    
    
    ## ~~~~~~~~~~ Solving Orbital Dynamics ~~~~~~~~~~~~
    # Solve the differential equations
    solution = solve_ivp(orbit_dynamics, t_span, y0, method='RK45', rtol=1e-6, atol=1e-9)
    
    return solution
    








