#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva
"""

import os
import logging
from . import path_instructions as path_instr

logger = logging.getLogger(__name__)

def main(cg, main_name):
    """Executes the steps required to perform the signals reconstructions
    """
    counters_metrics = get_counters_metrics()        
    ipc = calculate_mean_counter_metrics(counters_metrics)
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
    counter = 0
    number = 0
    percentage = 0
    try:
        #Open file containing the dynamic profiling(Counters metrics)
        with open(location, encoding='utf-8') as file:
            #Iterate each line
            for line in file:
                blank_line = line.strip()
                if event in blank_line:
                    #Retrieve the values
                    counter = counter + 1
                    number = number + int(blank_line.split()[1].replace(',', '').strip())
                    percentage = float(blank_line.split()[2].strip())
                    #Close file
            file.close()
            return number, counter, percentage
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
            mean = metrics[0] / metrics[1]
            result.get(key)[event] = mean
    return result

if __name__ == '__main__':
    main()
    
    