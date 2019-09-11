#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
import os
import click
import logging

import controller

logger = logging.getLogger(__name__)

#TODO: Paralelize instruction estimation task as no dependencies are associated
@click.command()
@click.option('-L', '--language', help='High level language of the application', required=True)
@click.option('-l', '--location', help='Directory containing the source code of the application', required=True)
@click.option('-s', '--sequential', help='Executes the dynamic profile in sequential order', is_flag=True)
@click.option('-v', '--verbose', help='Displays on terminal the information associated to the processes executed', is_flag=True)
@click.option('-c', '--clase', help='Class type of the application to analyze', required=False)
def main(language, location, sequential, verbose, clase):
    """ Framework aimed to analyze an application in order to estimate its energy consumption 
    """
    clase = clase.upper()
    main_function, function_sintax, comment_sintax = set_language(language)
    code_directory = get_code_directory(location)
    binary_name = get_binary_name(clase)
    main_file_name = search_file(location, main_function)
    display_values(language, sequential, code_directory, binary_name, main_file_name)
    
    energy = controller.run(main_file_name, function_sintax, comment_sintax, code_directory, binary_name, sequential, verbose, clase)
    
    print("\n\n########################################################")
    print("Energy estimation for CPU: %sJ \n" % round(energy.iloc[0, 0], 2))
    print("Energy estimation for Memory: %sJ \n" % round(energy.iloc[0, 1]), 2)
    print("########################################################")

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
        raise Exception('The selected programming language(%s) is not supported by the application' % language)
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

def get_binary_name(clase):
    """ Fetchs amd returns the file name of the binary associated to the application
    """
    directory = '../source_code/bin/'
    files = []
    try:
        files = os.listdir(directory)
    except FileNotFoundError as e:
        logger.error(e)
        raise
    if len(files) == 0:
        logger.error("No binary files found")
        raise Exception("No binary files found")
    elif clase != None:
        for file in files:
            if clase in file:
                return file
    else:
        if len(files) > 1:
            logger.error("Multiple binary files found")
            raise Exception("Multiple binary files found")
        return files[0]

def display_values(language, sequential, code_directory, binary_name, main_file_name):
    print("\n\n################################################################")
    print("Language of the application:", language)
    print('Sequential profiling' if sequential else 'Parallel profiling')
    print('Source code directory:', code_directory)
    print('Name of the binary file:', binary_name)
    print('Entrypoint file of the application:', main_file_name)
    print("################################################################\n\n")

if __name__ == '__main__':
    main()
