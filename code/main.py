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
from modules.energy_estimation import main as energy_estim

logger = logging.getLogger(__name__)

#TODO: Paralelize instruction estimation task as no dependencies are associated
@click.command()
@click.option('-L', '--language', help='High level language of the application', required=True)
@click.option('-l', '--location', help='Directory containing the source code of the application', required=True)
@click.option('-s', '--sequential', help='Executes the dynamic profile in sequential order', is_flag=True)
def main(language, location, sequential):
    """ Framework aimed to analyze an application in order to estimate its energy consumption 
    """
    #Get variables required by multiple modules
    main_function, function_sintax, comment_sintax = set_language(language)
    code_directory = get_code_directory(location)
    binary_name = get_binary_name() #File name of the application binary
    main_file_name = search_file(location, main_function)
        
    #Execution of modules
    cg = execute_call_graph_module(main_file_name, function_sintax, comment_sintax, code_directory, binary_name) #Execute Call Graph Set Module
    execute_instruction_estimation_module(binary_name, code_directory) #Run instruction estimation module
    execute_dynamic_profiling(sequential, binary_name) #Execute dynamic profiling
    ipc, counter_means, counters_metrics, execution_times = execute_signals_reconstruction(cg) #Retrieves the metrics from the profiling
    df_decimate, power_profile, energy = execute_energy_estimation(counter_means, execution_times)
    export_results(cg, ipc, counter_means, counters_metrics, execution_times, df_decimate, power_profile, energy)
    print("\n\n########################################################")
    print("Energy estimation for CPU: %sJ \n" % energy.iloc[0, 0])
    print("Energy estimation for Memory: %sJ \n" % energy.iloc[0, 1])
    print("########################################################")
    return energy

def set_language(language):
    """ Locates and returns the initial function of the application to analyze
    """
    language = language.lower()
    if(language == 'c++'):
        main_name = 'main'
        function_sintax = ""
        comment_sintax = ""
    elif(language == 'fortran'):
        function_sintax = "call"
        comment_sintax = "c "
        main_name = 'open'
    else:
        raise Exception('The selected programming language is not supported by the application')
    return main_name, function_sintax, comment_sintax
        

def search_file(directory, word):
    """ Locates the main file of the application to analyze
    """
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

def get_code_directory(location):
    """ Fetchs and returns the directory containing the source code of the application
    """
    if not location.endswith('/'):
        location += '/'
    return location.split('/')[-2]

def execute_call_graph_module(main_file_name, function_sintax, comment_sintax, code_directory, binary_name):
    """ Runs the call graph module
    """
    os.chdir('modules/cg') #Change of workspace in orden to execute Doxygen
    cg, labels = call_graph.main(main_file_name) #Get Paths
    if cg.empty:
        raise Exception('Error executing CFG module')
    cg_source_code.main(cg, labels, function_sintax, comment_sintax, code_directory) #Generate source code of the paths
    cg_binaries.main(binary_name, code_directory) #Compile paths to create binary file
    os.chdir('../..')
    return cg

def get_binary_name():
    """ Fetchs amd returns the file name of the binary associated to the application
    """
    directory = '../source_code/bin/'
    files = []
    try:
        files = os.listdir(directory)
    except FileNotFoundError as e:
        logger.error(e)
        raise
    if len(files) > 1 or len(files) == 0:
        logger.error("Multiple/None binary files found")
        raise Exception("Multiple/None binary files found, please leave only one")
    return files[0]

def execute_instruction_estimation_module(binary_name, code_directory):
    """ Runs the instruction estimation module
    """
    os.chdir('modules/instruction_estimation')
    result = estimate.main(binary_name, code_directory)#Instruction estimation module
    os.chdir('../..')
    return result

def execute_dynamic_profiling(sequential, binary_name):
    """ Runs the profiling module
    """
    os.chdir('modules/profiling')
    if(sequential):
        sequential_profiling.main(binary_name) #Sequential profiling
    else:
        profiling.run_binaries(binary_name) #Dynamic Profiling of the module
    os.chdir('../..')
    
def execute_signals_reconstruction(cg):
    """ Runs the signals reconstruction module
    """
    os.chdir('modules/signals_reconstruction')
    ipc, counters_means, counters_metrics, execution_times = signal_rec.reconstruct(cg)
    os.chdir('../..')
    return ipc, counters_means, counters_metrics, execution_times

def execute_energy_estimation(means, execution_times):
    os.chdir('modules/energy_estimation')
    df_decimate, power_profile, energy = energy_estim.main(means, execution_times)
    os.chdir('../..')
    return df_decimate, power_profile, energy

def export_results(cg, ipc, counters_means, counters_metrics, execution_times, df_decimate, power_profile, energy):
    signal = 'results/signal_reconstruction/'
    energy_estimation_path = 'results/energy_estimation/'
    if not os.path.exists(signal):
        os.mkdir(signal)
    export.export_dataframe(cg, 'results/paths')
    export.export_dataframe(execution_times, signal+'execution_times')
    export.export_dataframe(ipc, signal+'ipc')
    export.export_dataframe(counters_metrics, signal+'counters_metrics')
    export.export_dataframe(counters_means, signal+'counters_means')
    export.export_dataframe(df_decimate, energy_estimation_path+'decimate')
    export.export_dataframe(power_profile, energy_estimation_path+'power_profile')
    export.export_dataframe(energy, energy_estimation_path+'energy')
    
if __name__ == '__main__':
    main()
