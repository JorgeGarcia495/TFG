#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def main(cg):
    """Executes the steps required to perform the signals reconstructions
    """
    counters_metrics = get_counters_metrics()
    means = calculate_mean_counter_metrics(counters_metrics)
    ipc = calculate_ipc(counters_metrics)
    execution_times = reconstruction(cg, ipc, means)
    return ipc, means, counters_metrics, execution_times

def get_counters_metrics():
    paths_directory = '../../results/cg/source_code_paths/'
    counters = 'temp_file'
    bin_folder = '/bin/'
    counters_metrics = []
    #Counters associated to the cpu to execute the whole application
    events = ['BR_INST_RETIRED', 'BR_MISS_PRED_RETIRED', 'CPU_CLK_UNHALTED', 'INST_RETIRED', 'LLC_MISSES:0x41', 	'LLC_REFS:0x4f',
	'arith:fpu_div_active', 'l1d:0x1', 'l2_rqsts:0x1', 'l2_rqsts:0x3', 'l2_rqsts:0x8', 'l2_rqsts:0x20',	'mem_trans_retired:0x2',
    'mem_uops_retired:all_stores',	'misalign_mem_ref:0x1', 	'misalign_mem_ref:0x2',	'resource_stalls:any', 'uops_dispatched:core']
    try:
        #Get paths
        total_paths = os.listdir(paths_directory)
    except FileNotFoundError as e:
        print('La carpeta que contiene los distintos paths no existe')
        logger.error(e)
        raise
    for path in total_paths:
            path_metrics = iterate_counters_metrics(path, paths_directory+path+bin_folder+counters, events)
            counters_metrics.extend(path_metrics[:])
    aux = pd.DataFrame(counters_metrics)
    result = aux.iloc[:, 2:]
    multi_index = [aux.iloc[:, 0].astype(int), aux.iloc[:,1]]
    result.index = multi_index
    result.columns = events
    result.index.names = ['Path', 'Cycles(s)']
    result.sort_index(level=0)
    return result

def iterate_counters_metrics(path, location, events):
    """ Reads the file where the counter metrics are stores and returns it values
    """
    result = []
    values = []
    iteration = 0
    try:
        with open(location, encoding='utf-8') as file: #Open file containing the dynamic profiling(Counters metrics)
            for line in file:
                blank_line = line.strip()
                if line.startswith('Current time'):
                    if iteration is not 0:
                        values.insert(0, path) #Insert path number on first column
                        values.insert(1, iteration) #Insert the cycle time on second column
                        result.extend([values[:]])
                    iteration = iteration + 100
                    values.clear()
                elif len(blank_line) > 0 and blank_line.split()[0] in events:
                    values.append(int(blank_line.split()[1].replace(',', '').strip()))
            file.close()
            return result
    except FileNotFoundError as e:
        logger.error(e)
        raise
        
def calculate_mean_counter_metrics(counters_metrics):
    """ Calculates the mean values of the counter metrics for each path
    """
    return counters_metrics.groupby(level=0, axis=0).mean()

def calculate_ipc(counters_metrics):
    """ Calculates the instructions per cycle for each path
    """
    sums = counters_metrics.loc[:, ['INST_RETIRED', 'CPU_CLK_UNHALTED']].groupby(level=0).apply(sum, axis=0)
    result = pd.DataFrame(sums.INST_RETIRED.divide(sums.CPU_CLK_UNHALTED))
    result.columns =['IPC']
    return result

def reconstruction(cg, ipc, means):
    """ Generates several files in order to organize the data obtained from the profiling
    """
    path = '../../results/signal_reconstruction/plot/'
#    check_path(path)
    instructions_per_path = get_instructions_per_path(cg)
#    df = pd.DataFrame(instructions_per_path["Instructions"], 
#                      index=instructions_per_path["Path"], columns=["Instructions"])
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
#    df["Time"] = df.Instructions / df.Paths]
    result = pd.DataFrame.copy(df)
    result["Cycles"] = df.Path.map(lambda x: means.loc[x].CPU_CLK_UNHALTED)
    result["IPC"] = df.Path.map(lambda x: ipc.loc[x].item())
    result["Time"] = df.Instructions / df.Path.map(lambda x: ipc.loc[x].item() * means.loc[x].CPU_CLK_UNHALTED * 10)
    result["Total_Time"] = np.cumsum(result.Time)
    result.set_index("Path", inplace=True)
    return result

def time_preparation(data):
    result = data.Total_Time[:]
    result = result.append(data.Total_Time[1:]-0.001)
    return result.sort_values()
    
def data_preparation(values):
    result = values[:]
    result = result.append(values[:-1])
    return result.sort_index()
    
def generate_plot(x_axis, values, counter, path):
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
    
if __name__ == '__main__':
    main()
    
    