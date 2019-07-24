# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import pandas as pd

import coefficient_constants as constants

def get_power_profile(df_decimate):
    """ Calculates and returns the power profile associated to the counters metrics
    """
    result = pd.DataFrame({}, columns=['POWER_CPU', 'POWER_MEM', 'TIME'])
    df = pd.DataFrame.copy(df_decimate)
    df = df.set_index(['Time'])
    for index, data in df.iterrows():
        power_cpu = power_cpu_formula(data[constants.C2], data[constants.C3], data[constants.C4], \
                             data[constants.C6], data[constants.C7], data[constants.C8])
        power_mem = power_memory_formula(data[constants.C2], data[constants.C3], \
                                         data[constants.C5], data[constants.C8])
        result = result.append(pd.Series([power_cpu, power_mem, index], \
                                         index=result.columns), ignore_index=True)
    return result
        
def power_cpu_formula(C2, C3, C4, C6, C7, C8):
    """ Executes the power cpu profile formula and returns its value
    """
    result = (constants.x0 * ((constants.x1*C8+1) / (constants.x2*C4+1))) \
             + ((constants.x3 * (((constants.x4*C6+1)*(constants.x5*C3+1)* \
                                 ((constants.x6*C2+1)**2)) / (constants.x7*C7+1))) \
                                 - constants.x8)
    return result

def power_memory_formula(C2, C3, C5, C8):
    """ Executes the power memory profile formula and returns its value
    """
    result = (constants.y0 * (constants.y1*C8+1) / (constants.y2*C5+1)) \
             + (constants.y3 * (constants.y4*C8+1)*(constants.y5*C2+1)* \
                                 (constants.y6*C3+1)-constants.y7)
    return result