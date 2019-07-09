#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def main(cg, ipc, means):
    """ Generates several files in order to organize the data obtained from the profiling
    """
    path = '../../results/signal_reconstruction/plot/'
    check_path(path)
    instructions_per_path = get_instructions_per_path(cg)
    df = pd.DataFrame(instructions_per_path, 
                      columns=["Path", "Instructions"])
    path_exec_time = calculate_execution_time(df, ipc, means)
    means = means.drop(np.setdiff1d(means.index.to_series(), path_exec_time.index.to_series()))
    for counter in means.columns:
        times = time_preparation(path_exec_time)
        values = data_preparation(means[counter])
        generate_plot(times, values, counter, path)
    return path_exec_time
    
def check_path(path):
    """ Checks if the path passed as an argument is created
    """
    if os.path.exists(path):
        os.remove(path)
    os.mkdir(path)
    
#TODO: Check again once the instruction estimation module is completed
def get_instructions_per_path(cg):
    """ Reads the data generated by the instruction estimation module and retrieves
    the number of instructions per path
    """
    directory = '../../results/instructions_estimation/instructions_per_path.csv'
    indexes = []
    instructions = []
    instructions_per_path = pd.read_csv(directory, delimiter=',', skiprows=1, decimal='.', 
                       names=["Function_1","Function_2","Function_3", "Function_4","Instructions",])
    for index, path in enumerate(cg):
        path_functions = np.array(path)
        for index_df, row in instructions_per_path.iterrows():
            if np.all(np.in1d(row[:-1], path_functions)):
                indexes.append(index)
                instructions.append(row[-1])
    return {"Path" : indexes, "Instructions" : instructions}

def calculate_execution_time(df, ipc, means):
    """ Creates and returns a dataframe with the execution time for each path
    """
    result = pd.DataFrame.copy(df)
    result["Cycles"] = df.Path.map(lambda x: means.loc[x].CPU_CLK_UNHALTED)
    result["IPC"] = df.Path.map(lambda x: ipc.loc[x].item())
    result["Time"] = df.Instructions / df.Path.map(lambda x: ipc.loc[x].item() * means.loc[x].CPU_CLK_UNHALTED * 10)
    result["Total_Time"] = np.cumsum(result.Time)
    result.set_index("Path", inplace=True)
    return result

def time_preparation(data):
    """ Handles the data contained on the argument to display a better view on next steps
    """
    result = data.Total_Time[:]
    result = result.append(data.Total_Time[1:]-0.001)
    return result.sort_values()
    
def data_preparation(values):
    """ Handles the data contained on the argument to display a better view on next steps
    """
    result = values[:]
    result = result.append(values[:-1])
    return result.sort_index()
    
def generate_plot(x_axis, values, counter, path):
    """ Creates a plot with the data contained on the arguements
    """
    plt.figure(figsize=(9,4))
    plt.plot(x_axis, values, label=counter)
    plt.title('BT - CLASS B (Hardware counter signal reconstruction)')
    plt.xlabel('Time(s)')
    plt.legend()
    plt.ylabel(counter)
    plt.xlim(xmin=0, xmax=x_axis.max()+5)
    save_path = path+counter+'.png'
    plt.savefig(save_path.replace(':', '_'))
    plt.cla()