# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
#For reading arguments
import sys
#To traverse directories
import os
#To execute parallel processes
import subprocess
#For logging purposes
import logging
#Library to execute the cfg module
import modules.cfg.call_graph as call_graph
import modules.cfg.call_graph_source_code as cg_source_code
#Library to estimate the instructions of an application
import modules.estimate_instructions as estimate

logger = logging.getLogger(__name__)

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
        main = set_language(language)
        entry_file = search_file(directory, main)
        print("Punto de entrada de la aplicacion: ", entry_file)
        #Change of workspace in orden to execute Doxygen
        os.chdir('modules/cfg')
        cg, labels = call_graph.main()
        cg_source_code.generate_code_paths(cg, labels)
        #Back to original workspace
        os.chdir('../../')
        
        if(cg == None or len(cg) == 0):
            raise Exception('Error executing CFG module')
        #Module instruction estimation
        instr_estim = estimate.main()
        
def set_language(language):
    """ Locates and returns the initial function of the application to analyze
    """
    if(language == 'c++'):
        return 'main'
    elif(language == 'fortrand'):
        return 'open'
    else:
        raise Exception('The selected programming language is not supported by the application')
        
def search_file(directory, word):
    """ Locates the main file of the application to analyze
    """
    result = ''
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if word in open(directory + '\\' + file).read():
                    result = directory + '\\' + file
                    break
                if(result == ''):
                    raise Exception('The entry of the application was not found')
        return result
    except FileNotFoundError as e:
        logger.error(e)
        raise

    
if __name__ == '__main__':
    main()
