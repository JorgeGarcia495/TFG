#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
import os
import click
import logging

from modules import export_data as export
from modules.cg import call_graph as call_graph
from modules.cg import call_graph_source_code as cg_source_code
from modules.cg import call_graph_binaries as cg_binaries
from modules.instruction_estimation import estimate_instructions as estimate
from modules.profiling import main as profiling
from modules.profiling import main_sequential as sequential_profiling
from modules.signals_reconstruction import main as signal_rec

logger = logging.getLogger(__name__)

#TODO: Paralelize instruction estimation task as no dependencies are associated
@click.command()
@click.option('-L', '--language', help='High level language of the application', required=True)
@click.option('-l', '--location', help='Directory containing the source code of the application', required=True)
@click.option('-s', '--sequential', help='Executes the dynamic profile in sequential order', is_flag=True)
def main(language, location, sequential):
    """ Framework intended to analyze an application in order to estimate its energy consumtpion """
    entrypoint = set_language(language)
    main_name = search_file(location, entrypoint)
    cg = execute_call_graph_module(main_name) #Execute Call Graph Set Module
    execute_instruction_estimation_module() #Run instruction estimation module
    execute_dynamic_profiling(sequential) #Execute dynamic profiling
    ipc, counter_means, counters_metrics, execution_times = execute_signals_reconstruction(cg) #Retrieves the metrics from the profiling
    export_results(cg, ipc, counter_means, counters_metrics, execution_times)

def set_language(language):
    """ Locates and returns the initial function of the application to analyze
    """
    language = language.lower()
    if(language == 'c++'):
        return 'main'
    elif(language == 'fortran'):
        return 'open'
    else:
        raise Exception('The selected programming language is not supported by the application')
        
def search_file(directory, word):
    """ Locates the main file of the application to analyze
    """
    directory = '../nas_bt/%s/' % directory
    word = 'open'
    result = ''
    try:
        for files in os.listdir(directory):
            if files.endswith('.f'):
                with open(directory+files) as file:
                    for line in file:
                        if word in line.strip():
                            return files
        if(result == ''):
            raise Exception('The entry of the application was not found')
    except FileNotFoundError as e:
        logger.error(e)
        raise

def execute_call_graph_module(main_name):
    """ Runs the call graph module
    """
    os.chdir('modules/cg') #Change of workspace in orden to execute Doxygen
    cg, labels = call_graph.main(main_name) #Get Paths
    if(cg == None or len(cg) == 0):
        raise Exception('Error executing CFG module')
    cg_source_code.generate_code_paths(cg, labels) #Generate source code of the paths
    cg_binaries.main() #Compile paths to create binary file
    os.chdir('../..') #Back to original workspace
    return cg

def execute_instruction_estimation_module():
    """ Runs the instruction estimation module
    """
    os.chdir('modules/instruction_estimation')
    result = estimate.main()#Instruction estimation module
    os.chdir('../..')
    return result

def execute_dynamic_profiling(sequential):
    """ Runs the profiling module
    """
    os.chdir('modules/profiling')
    if(sequential):
        sequential_profiling.main() #Sequential profiling
    else:
        profiling.run_binaries() #Dynamic Profiling of the module
    os.chdir('../..')
    
def execute_signals_reconstruction(cg):
    """ Runs the signals reconstruction module
    """
    os.chdir('modules/signals_reconstruction')
    ipc, counters_means, counters_metrics, execution_times = signal_rec.reconstruct(cg)
    os.chdir('../..')
    return ipc, counters_means, counters_metrics, execution_times

def export_results(cg, ipc, counters_means, counters_metrics, execution_times):
    signal = 'results/signal_reconstruction/'
    if not os.path.exists(signal):
        os.mkdir(signal)
    export.export_dataframe(cg, 'results/paths')
    export.export_dataframe(execution_times, signal+'execution_times')
    export.export_dataframe(ipc, signal+'ipc')
    export.export_dataframe(counters_metrics, signal+'counters_metrics')
    export.export_dataframe(counters_means, signal+'counters_means')
    
if __name__ == '__main__':
    main()
