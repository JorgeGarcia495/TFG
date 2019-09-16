#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
import os
import shutil
import logging
import subprocess
from . import call_graph_paths as cg_paths

logger = logging.getLogger(__name__)

def main(file, verbose, code_directory, clase):
    """Entrypoint of the module
    """
    directory = '../../../source_code/'
    check_code_directory(directory, code_directory)
    execute_doxygen(verbose)
    save_main(file, code_directory, clase)
    delete_generated_files()
    delete_code_directory(code_directory)
    return cg_paths.main()

def check_code_directory(directory, code_directory):
    """ Checks that the application to analyze is located in the same directory
        as the doxyfile
    """
    if not os.path.exists(code_directory):
        for files in os.listdir(directory):
            if os.path.isdir(directory+files):
                shutil.copytree(directory+files, files)
            else:
                shutil.copy(directory+files, files)

def execute_doxygen(verbose):
    """ Calls the system to execute the Doxygen
    """
    try:
        print("Start executing doxygen")
        call = ['doxygen', 'Doxyfile']
        if verbose:
            subprocess.check_call(call)
        else:
            subprocess.check_call(call, stdout=subprocess.PIPE, shell=False)
        print('End of doxygen execution')
    except subprocess.CalledProcessError as e:
        logger.error(e)
        raise
        
def save_main(main_name, code_directory, clase):
    """ Saves the source code based on the paths retrieved from the cg
    """
    try:
        directory = '../../results/'+code_directory + '/' + clase + '/cg/'
        if not os.path.exists(directory):
            os.mkdir(directory)
        found = False;
        for root, dirs, files in os.walk('html'):
            for file in files:
                if file.startswith(main_name.split('.')[0]) and file.endswith('.dot'):
                    name = 'cgraph.dot'
                    if os.path.exists(directory+name):
                        os.remove(directory+name)
                    os.rename('html/'+file, name)
                    shutil.copy(name, directory)
                    found = True
                    break
        if found == False:
            raise Exception('Error finding doxygen generated files...')
    except FileNotFoundError as e:
        logger.error(e)
        raise
            

def delete_generated_files():
    """Deletes the unnecessary files generated by the cg
    """
    try:
        shutil.rmtree('html')
    except FileNotFoundError as e:
        logger.error(e)
        raise

def delete_code_directory(code_directory):
    """ Deletes every folder on the current durectory
    """
    if os.path.exists(code_directory):
        for files in os.listdir():
            if os.path.isdir(files):
                shutil.rmtree(files)
