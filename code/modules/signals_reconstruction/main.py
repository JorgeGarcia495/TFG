#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import logging
import pandas as pd
from . import reconstruction as rec

logger = logging.getLogger(__name__)

def reconstruct(cg, code_directory, clase):
    """Executes the steps required to perform the signals reconstructions
    """
    counters_metrics = get_counters_metrics()
    means = calculate_mean_counter_metrics(counters_metrics)
    ipc = calculate_ipc(counters_metrics)
    execution_times = rec.main(cg, ipc, means, code_directory, clase)
    return ipc, means, counters_metrics, execution_times

def get_counters_metrics():
    """ Gets the counters metrics generated during the dynamic profiling
    """
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
            path_metrics = iterate_counters_metrics(path, paths_directory+path+bin_folder+counters+'_'+path, events)
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
    
