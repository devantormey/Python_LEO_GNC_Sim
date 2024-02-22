# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:35:06 2024

@author: devan
this is for calculating the elapsed time since the vernal equinox, this is 
necessary for the conversion from ECI to ECEF
"""

from datetime import datetime, timedelta, timezone

def calculate_elapsed_hours_since_vernal_equinox(date_input):
    """
    Calculate the elapsed hours since the vernal equinox of the same year as the given date.

    Parameters:
    - date_input: datetime object representing the current date and time.

    Returns:
    - Elapsed hours since the vernal equinox as a float.
    """
    # Determine the year of the input date
    year = date_input.year
    
    # Define the vernal equinox of the same year at 00:00 UTC
    # Adjust the day and time as needed for precision
    vernal_equinox = datetime(year, 3, 20, 0, 0, tzinfo=timezone.utc)
    
    # Calculate the time difference
    time_difference = date_input - vernal_equinox
    
    # Convert time difference to hours
    elapsed_hours = time_difference.total_seconds() / 3600.0
    
    return elapsed_hours