# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:08:45 2024

@author: Devan Tormey
this is our main script that calls both the user input for orbital parameters 
and subsequently calls all of the simulations
"""
import tkinter as tk
from tkinter import simpledialog
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from add_paths import add_paths
import sys
import os

try:
    from run_orbital_simulation import run_orbital_simulation
    from get_user_input import get_user_input
except ImportError:
    add_paths()
    print("Done Adding Paths")
    from run_orbital_simulation import run_orbital_simulation
    from get_user_input import get_user_input
    
print("finished importing packages running main...")

if __name__ == "__main__":
    print("Gathering Inputs")
    user_inputs = get_user_input()
    if user_inputs:
        altitude, inclination, n_orbits = user_inputs
        solution = run_orbital_simulation(altitude, inclination, n_orbits)
        
        #Necessary Constants
        # Gravitational Constant
        G = 6.67430e-11  # m^3 kg^-1 s^-2
        # Earth's Mass
        M = 5.972e24  # kg
        # Earth's radius in meters
        Re = 6.371e6  # Earth radius in meters
            
        ## ~~~~~~~~~~ Plotting Data (images, references) ~~~~~~~~~~~~
        # Add in a representative Sphere for earth
        phi, theta = np.linspace(0, 2 * np.pi, 100), np.linspace(0, np.pi, 100)
        phi, theta = np.meshgrid(phi, theta)
        x = Re * np.sin(theta) * np.cos(phi)
        y = Re * np.sin(theta) * np.sin(phi)
        z = Re * np.cos(theta)
        
        # Flat Map Image dimensions
        img_width = 2202
        img_height = 1000
        
        # Load the map image
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'include/flatmap.png'))
        
        map_img = plt.imread(img_path)
        
        
        ## ~~~~~~~~~~ Plotting Data Conversions ~~~~~~~~~~~~
        
        # Convert from cartesian coordinates to Lat-Lon
        lat = np.arcsin(solution.y[2] / np.sqrt(solution.y[0]**2 + solution.y[1]**2 + solution.y[2]**2))
        lon = np.arctan2(solution.y[1], solution.y[0])
        
        # If we wish to account for earth's rotoation we can adjust here
        
        # Assuming solution.t is the array of time points in seconds
        # Convert times to hours for rotation calculation
        times_hours = solution.t / 3600.0
        
        # Earth's rotation speed in degrees per hour
        rotation_speed_deg_per_hour = 360.0 / 24.0
        
        # For each time point, calculate the Earth's rotational shift
        earth_rotation_adjustment = (times_hours * rotation_speed_deg_per_hour)
        
        # Adjust the longitude for Earth's rotation
        # Ensure longitude remains within [-pi, pi] or [0, 2*pi] after adjustment
        adjusted_lon = (lon - np.radians(earth_rotation_adjustment)) % (2 * np.pi)
        
        # Convert adjusted_lon back to the range used for plotting if necessary
        x_img = ((adjusted_lon + np.pi) % (2 * np.pi)) / (2 * np.pi) * img_width
        
        # Map latitude to y coordinate using Mercator projection
        y_img = (np.log(np.tan(np.pi / 4 + lat / 2)) / (2 * np.pi) + 0.5) * img_height
        y_img = img_height - y_img  # Flip y-axis to match image coordinates
        
        
        
        ## ~~~~~~~~~~ Plotting ~~~~~~~~~~~~
        # 3D plotting
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(solution.y[0], solution.y[1], solution.y[2], label='Satellite Orbit', color='red')
        ax.plot_surface(x, y, z, color='blue', edgecolor='none', alpha=0.3)
        ax.set_xlabel('X Position (m)')
        ax.set_ylabel('Y Position (m)')
        ax.set_zlabel('Z Position (m)')
        plt.title('3D Satellite Orbit Simulation')
        plt.legend()
        plt.show()
        
        
        #2d Plotting
        fig, ax = plt.subplots()
        ax.imshow(map_img, extent=[0, img_width, 0, img_height])
        
        def plot_orbit_segments(x, y, color='r'):
            # Initialize the first segment
            current_segment_x = [x[0]]
            current_segment_y = [y[0]]
            
            for i in range(1, len(x)):
                # Check for wrap-around
                if np.abs(x[i] - x[i-1]) > img_width * 0.5:
                    # Plot the current segment before wrap-around
                    ax.plot(current_segment_x, current_segment_y, color)
                    # Start a new segment
                    current_segment_x = [x[i]]
                    current_segment_y = [y[i]]
                else:
                    # Continue accumulating points in the current segment
                    current_segment_x.append(x[i])
                    current_segment_y.append(y[i])
            
            # Plot the last segment
            ax.plot(current_segment_x, current_segment_y, color)
        
        plot_orbit_segments(x_img, y_img, 'r')  # Use the function to plot orbit segments
        #ax.scatter(x_img, y_img, color='r', s=1)  # 'r' for red
        
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.set_xlabel('X Position (m)')
        ax.set_ylabel('Y Position (m)')
        plt.title('Satellite Orbit on Mercator Projection')
        #plt.legend()
        plt.show()

