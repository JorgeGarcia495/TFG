#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""


def get_total_instructions():
    """ Gets the number of instructions of each function in the program to analyze
    """
    directory = '../../results/instructions_estimation/total_instructions_per_function'
    key = ''
    result = {}
    with open(directory) as file:
        for line in file:
            line = line.lower()
            if 'function' in line:
                key = line.split()[1].strip()
            if 'instructions:' in line:
                result[key] = line.split()[2].strip()
    return result
                
                
def get_instructions_per_path(instructions_per_function, cg, main_name):
    """ Calculates the number of instructions for each path
    """
    result = {}
    for index, paths in enumerate(cg):
        total = 0
        for path in paths:
            if path == main_name:
                path = 'main_'
            total = total + 0 if (path not in instructions_per_function) else total + int(instructions_per_function[path])
        result[index] = total
    return result

