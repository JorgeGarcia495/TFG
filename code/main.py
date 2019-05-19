# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
import os
import sys
import logging

from modules import export_data as export
from modules.cg import call_graph as call_graph
from modules.cg import call_graph_source_code as cg_source_code
from modules.cg import call_graph_binaries as cg_binaries
from modules.instruction_estimation import estimate_instructions as estimate
from modules.profiling import main as profiling
from modules.signals_reconstruction import main as signal_rec

logger = logging.getLogger(__name__)

#TODO: Paralelize instruction estimation task as no dependencies are associated
def main():
    """ Entrypoint of the program
    """
    if(len(sys.argv) != 3):
        raise Exception("The programming language and location of the program is expected to be passed as an argument")
    else:
        language = sys.argv[1]
        print("Idioma seleccionado: ", language)
        directory = sys.argv[2]
        print("Directorio raiz de la aplicacion: ", directory)
        entrypoint = set_language(language)
        main_name = search_file(directory, entrypoint)
        print("Punto de entrada de la aplicacion: ", entrypoint)
        
        #Execute Call Graph Set Module
        cg = execute_call_graph_module()
        #Export results to csv
        export.export_multiple_lists_csv(cg, 'results/paths.csv')
        #Move to instruction estimation module
        execute_instruction_estimation_module()
        execute_dynamic_profiling()
        ipc, instructions_per_path = execute_signals_reconstruction(cg, main_name)
        export.export_list_csv(instructions_per_path.values(), 'results/instructions_per_path.csv')
        export.export_dict_csv(ipc, 'results/counters_metrics.csv')
        
        
def set_language(language):
    """ Locates and returns the initial function of the application to analyze
    """
    if(language == 'c++'):
        return 'main'
    elif(language == 'fortran'):
        return 'open'
    else:
        raise Exception('The selected programming language is not supported by the application')
        
def search_file(directory, word):
    """ Locates the main file of the application to analyze
    """
    directory = '../nas_bt/BT/'
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

def execute_call_graph_module():
    """ Runs the call graph module
    """
    #Change of workspace in orden to execute Doxygen
    os.chdir('modules/cg')
    #Get Paths
    cg, labels = call_graph.main()
    if(cg == None or len(cg) == 0):
        raise Exception('Error executing CFG module')
    #Generate source code of the paths
    cg_source_code.generate_code_paths(cg, labels)
    #Compile paths to create binary file
    cg_binaries.main()
    #Back to original workspace
    os.chdir('../..')
    return cg

def execute_instruction_estimation_module():
    """ Runs the instruction estimation module
    """
    os.chdir('modules/instruction_estimation')
    #Instruction estimation module
    result = estimate.main()
    os.chdir('../..')
    return result

def execute_dynamic_profiling():
    """ Runs the profiling module
    """
    os.chdir('modules/profiling')
    #Dynamic Profiling of the module
    profiling.run_binaries()
    os.chdir('../..')
    
def execute_signals_reconstruction(cg, main_name):
    """ Runs the signals reconstruction module
    """
    os.chdir('modules/signals_reconstruction')
    ipc, instrucions_per_path = signal_rec.main(cg, main_name.split('.f')[1])
    os.chdir('../..')
    return ipc, instrucions_per_path
    
if __name__ == '__main__':
    main()
