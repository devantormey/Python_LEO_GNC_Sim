# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:34:34 2024

@author: devan
"""
import sys
import os

def add_paths():
    # Get the absolute path of the 'lib' directory
    lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    
    # Directories to add to sys.path
    directories = ['', 'coords', 'environment', 'ui']
    
    # Iterate over the directories and add them to sys.path
    for directory in directories:
        path_to_add = os.path.join(lib_path, directory)
        if path_to_add not in sys.path:
            sys.path.append(path_to_add)
            print(f"Added to sys.path: {path_to_add}")
