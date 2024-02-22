# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:32:02 2024

@author: devan

Description: This function is for converting from ECI reference frame to ECEF 
"""

import numpy as np

def eci_to_ecef(eci_coords, elapsed_hours_since_vernal_equinox):
    """
    Convert ECI coordinates to ECEF coordinates.

    Parameters:
    - eci_coords: numpy array of the ECI coordinates (x, y, z).
    - elapsed_hours_since_vernal_equinox: time elapsed in hours since the vernal equinox.

    Returns:
    - numpy array of the ECEF coordinates (x, y, z).
    """
    # Earth's rotation rate (radians per sidereal hour)
    omega_earth = 2 * np.pi / 23.9345  # 23.9345 hours for a sidereal day

    # Calculate the rotation angle
    theta = omega_earth * elapsed_hours_since_vernal_equinox

    # Rotation matrix about the Z-axis
    rotation_matrix = np.array([
        [np.cos(theta), np.sin(theta), 0],
        [-np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

    # Convert ECI to ECEF
    ecef_coords = np.dot(rotation_matrix, eci_coords)

    return ecef_coords