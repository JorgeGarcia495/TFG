# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import numpy as np
import pandas as pd

from . import plots
from . import power_profiles as pow_profiles

def main(means, execution_times, code_directory, clase):
    """ Entrypoint of the script
    """
    
    df_decimate = diezmado(means, execution_times)
    power_profile = pow_profiles.get_power_profile(df_decimate)
    plots.check_path('../../results/energy_estimation/')
    plots.get_power_plots(power_profile, code_directory, clase)
    energy = estimate_energy(power_profile)
    return df_decimate, power_profile, energy
    
def diezmado(means, execution_times):
    """ Prepares the data with samples for every 10s
    """
    values = pd.DataFrame.copy(means)
    values = values.drop(np.setdiff1d(values.index.to_series(), execution_times.index.to_series()))
    
    return split_data(values, execution_times)

def split_data(values, execution_times):
    """ Splits the data contained on the counters metrics on samples for every 10s
    """
    result = pd.DataFrame(columns=values.columns)
    df = pd.DataFrame(columns=values.columns)
    
    for path in values.index:
        time_ms = int(execution_times.Time[path] * 10)
        df = df.append([values.loc[path]]*time_ms, ignore_index=True)
    df["Time"] = 100
    df["Time"] = df["Time"].cumsum()
    
    start = 0
    end = 100
    
    for i in range(100,len(df)+100, 100):
        end = i
        data = df.iloc[start:end, :-1]
        if len(data) == 100:
            result = result.append(data.sum(), ignore_index=True)
        start = end
    result["Time"] = 10
    result["Time"] = result["Time"].cumsum()
    return result

def estimate_energy(power_profile):
    """ Estimates the energy consumption of the application being analyzed
    """
    result = {}
    result["Memory"] = [power_profile.POWER_MEM.sum() * 10]
    result["CPU"] = [power_profile.POWER_CPU.sum() * 10]
    return pd.DataFrame(result)
    
    
    
    
