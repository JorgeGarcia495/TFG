#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva
"""

import os
import csv
import logging
import pandas as pd
from . import path_instructions as path_instr

logger = logging.getLogger(__name__)

def main(cg, main_name):
    """Executes the steps required to perform the signals reconstructions
    """
    counters_metrics = get_counters_metrics()        
    means = calculate_mean_counter_metrics(counters_metrics)
    ipc = calculate_ipc(counters_metrics)
    instructions_per_function = path_instr.get_total_instructions()
    instructions_per_path = path_instr.get_instructions_per_path(instructions_per_function, cg, main_name)
    return ipc, instructions_per_path

def get_counters_metrics():
    paths_directory = '../../results/cg/source_code_paths/'
    counters = 'temp_file'
    bin_folder = '/bin/'
    counters_metrics = {}
    #Counters associated to the cpu to execute the whole application
    events = ['BR_INST_RETIRED', 'BR_MISS_PRED_RETIRED', 'CPU_CLK_UNHALTED', 'INST_RETIRED', 'LLC_MISSES:0x41', 	'LLC_REFS:0x4f',
	'arith:fpu_div_active', 	'l1d:0x1', 'l2_rqsts:0x1', 'l2_rqsts:0x3', 'l2_rqsts:0x8', 'l2_rqsts:0x20',	'mem_trans_retired:0x2',	 
    'mem_uops_retired:all_stores',	'misalign_mem_ref:0x1', 	'misalign_mem_ref:0x2',	'resource_stalls:any', 'uops_dispatched:core']
    try:
        #Get paths
        total_paths = os.listdir(paths_directory)
    except FileNotFoundError as e:
        print('La carpeta que contiene los distintos paths no existe')
        logger.error(e)
        raise
    #Iterate each path
    for path in total_paths:
        #Retrieve values for each event
        for event in events:
            number, counter, percentage = iterate_counters_metrics(paths_directory+path+bin_folder+counters, event)
            #Add values to dictionary
            if counters_metrics.get(path) == None:
                counters_metrics[path] = {event: [number, counter, percentage]}
            else :
                counters_metrics.get(path)[event] = [number, counter, percentage]
    return counters_metrics

def iterate_counters_metrics(location, event):
    """ Reads the file where the counter metrics are stores and returns it values
    """
    iteration = 0
    number = 0
    percentage = 0
    try:
        with open(location, encoding='utf-8') as file: #Open file containing the dynamic profiling(Counters metrics)
            for line in file:#Iterate each line
                blank_line = line.strip()
                if event in blank_line:
                    iteration = iteration + 1
                    number = number + int(blank_line.split()[1].replace(',', '').strip())
                    percentage = float(blank_line.split()[2].strip())
            file.close() #Close file
            return number, iteration, percentage
    except FileNotFoundError as e:
        logger.error(e)
        raise

def get_counters_metrics_per_iteration():
    paths_directory = '../../results/cg/source_code_paths/'
    counters = 'temp_file'
    bin_folder = '/bin/'
    counters_metrics = []
    #Counters associated to the cpu to execute the whole application
    events = ['BR_INST_RETIRED', 'BR_MISS_PRED_RETIRED', 'CPU_CLK_UNHALTED', 'INST_RETIRED', 'LLC_MISSES:0x41', 	'LLC_REFS:0x4f',
	'arith:fpu_div_active', 	'l1d:0x1', 'l2_rqsts:0x1', 'l2_rqsts:0x3', 'l2_rqsts:0x8', 'l2_rqsts:0x20',	'mem_trans_retired:0x2',	 
    'mem_uops_retired:all_stores',	'misalign_mem_ref:0x1', 	'misalign_mem_ref:0x2',	'resource_stalls:any', 'uops_dispatched:core']
    try:
        #Get paths
        total_paths = os.listdir(paths_directory)
    except FileNotFoundError as e:
        print('La carpeta que contiene los distintos paths no existe')
        logger.error(e)
        raise
    for path in total_paths:
            path_metrics = get_metrics_per_iteration(path, paths_directory+path+bin_folder+counters, events)
            counters_metrics.extend(path_metrics[:])
    return counters_metrics

    dfhsa = pd.read_csv(name, delimiter=',', names=events)
    dfhsa.index
    aaaa = pd.DataFrame(counters_metrics)
    aa = counters_metrics[2][2:]
    aa[2:100]
    counters_metrics[0:5]
        
def get_metrics_per_iteration(path, location, events):
    result = []
    values = []
    iteration = 0
    try:
        with open(location, encoding='utf-8') as file: #Open file containing the dynamic profiling(Counters metrics)
            for line in file:
                blank_line = line.strip()
                if line.startswith('Current time'):
                    if iteration is not 0:
                        values.insert(0, path)
                        values.insert(1, iteration)
                        result.extend([values[:]])
                        values.clear()
                    iteration = iteration + 100
                elif len(blank_line) > 0 and blank_line.split()[0] in events:
                    values.append(int(blank_line.split()[1].replace(',', '').strip()))
#            if len(values) > 0:
#                values.insert(0, path)
#                values.insert(1, iteration)
#                result.extend([values[:]])
            file.close() #Close file
            return result
    except FileNotFoundError as e:
        logger.error(e)
        raise
        
def calculate_mean_counter_metrics(counters_metrics):
    """ Calculates the mean values of the counter metrics for each path
    """
    result = {}
    mean = 0
    #Iterate the metrics
    for key, values in counters_metrics.items():
        result[key] = {}
        #Get mean values
        for event, metrics in values.items():
            value = metrics[0]
            iterations = metrics[1]
            mean = value / iterations
            result.get(key)[event] = mean
    return result

def calculate_ipc(counters_metrics):
    """ Calculates the instructions per cycle for each path
    """
    result = {}
    for key, values in counters_metrics.items():
        inst_retired = values['INST_RETIRED'][0]
        clock_cycles = values['CPU_CLK_UNHALTED'][0]
        result[key] = inst_retired / clock_cycles
    return result

name = 'pepe.txt'
data = counters_metrics

def export_paths_metrics(name, data):
    if os.path.exists(name):
        os.remove(name)
    with open(name, 'w') as file:
        data_writer = csv.writer(file, delimiter=',', dialect='excel')
        data_writer.writerows(data)
    file.close()
        
if __name__ == '__main__':
    main()
    
    