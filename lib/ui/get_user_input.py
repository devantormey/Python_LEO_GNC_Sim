# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:09:44 2024

@author: Devan Tormey
this script creates a dialogue window and grabs user inputs defining orbital
mechanics
"""



import tkinter as tk
from tkinter import ttk
import numpy as np

class InputDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Orbital Parameters Input")
        self.top.geometry("500x500")  # Set the window size to 300x150 pixels

        # Altitude input
        ttk.Label(self.top, text="Orbital Altitude (km):").pack(pady=5)
        self.altitude_entry = ttk.Entry(self.top)
        self.altitude_entry.pack(pady=5)

        # Inclination input
        ttk.Label(self.top, text="Inclination (degrees):").pack(pady=5)
        self.inclination_entry = ttk.Entry(self.top)
        self.inclination_entry.pack(pady=5)
        
        # Number of Orbits input
        ttk.Label(self.top, text="# of Orbits:").pack(pady=5)
        self.orbit_entry = ttk.Entry(self.top)
        self.orbit_entry.pack(pady=5)
        
        # Submit button
        self.submit_button = ttk.Button(self.top, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=20)

        # Variable to store the result
        self.result = None

    def on_submit(self):
        # Try to get and validate user inputs
        try:
            altitude = float(self.altitude_entry.get()) * 1000  # Convert to meters
            inclination = float(self.inclination_entry.get())
            n_orbits = int(self.orbit_entry.get())
            if 0 <= altitude <= 1000 * 1000 and 0 <= inclination <= 180:
                inclination = np.radians(inclination)  # Convert to radians
                self.result = (altitude, inclination, n_orbits)
                self.top.destroy()  # Close the dialog
            else:
                tk.messagebox.showerror("Error", "Input values out of range.")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    input_dialog = InputDialog(root)
    root.wait_window(input_dialog.top)  # Wait for the dialog to be closed

    if input_dialog.result:
        altitude, inclination, n_orbits = input_dialog.result
        return altitude, inclination, n_orbits
    return None, None  # In case the dialog is closed without submitting

if __name__ == "__main__":
    altitude, inclination = get_user_input()
    if altitude is not None and inclination is not None:
        print(f"Altitude: {altitude}, Inclination: {np.degrees(inclination)} degrees")
        # Here you would call run_orbital_simulation(altitude, inclination)
    else:
        print("No input provided.")
