#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
import os
import shutil
import logging

logger = logging.getLogger(__name__)

#TODO: Retrieve cg info from call_graph if this module is executed independently
def main():
    """Entrypoint of the module
    """
    print('This module requires the execution of the call graph')
    proceed = input('Do you want to proceed? (y/n)')
    proceed = proceed.uppercase()
    if proceed == 'YES' or proceed == 'Y' or proceed == 'SI' or proceed == 'S':
        generate_code_paths(cg, labels)
    else: 
        print('Nothing to do...')

#TODO: Parametrize main file name instead of 'bt'
def generate_code_paths(cg, labels):
    """Locates the main file of the application to analyze
    """
    functions = list(labels.values())
    try:
        workspace = '../../results/cg/source_code_paths/'
        #Delete existing files
        if os.path.exists(workspace):
            shutil.rmtree(workspace)
            os.mkdir(workspace)
        required_files = ['Makefile', 'header.h']
        for index, path in enumerate(cg):
            directory = workspace+str(index)
            #Copy source code
            shutil.copytree('../../../nas_bt', directory)
            directory = directory+'/BT/'
            #Iterate source code files
            for file in os.listdir(directory):
                #Delete if not needed 
                if not file.endswith('.f') and not file.endswith('.h') and file not in required_files:
                    os.remove(directory+file)
                    #Comment not needed functions on main file
            remove_unneeded_functions(directory, functions, path)
    except FileNotFoundError as e:
        logger.error(e)
        raise
        
#TODO: Remove the static main by a dynamic one inserting it as a parameter
def remove_unneeded_functions(directory, functions, path):
    """Removes the functions not needed on each path from the main file of the application
    """
    for files in os.listdir(directory):
        if files.split('.')[0] in path:
            with open(directory+files, encoding='utf-8') as file:
                with open(directory+'tempfile.txt', 'w') as tmp:
                    open_parenthesis = 0
                    function = ''
                    for line in file:
                        #Remove blank spaces at beginning and end of the line
                        line_no_blank = line.strip()
                        #Comment functions occupying several lines
                        if open_parenthesis != 0:
                            open_parenthesis = open_parenthesis + line_no_blank.count('(') - line_no_blank.count(')')
                            if function in functions and function not in path:
                                tmp.write('c ')
                            #Check if there is a function
                        if line_no_blank.startswith('call') :
                            #Get name of the function to call
                            index = line_no_blank.index(" ")
                            function = line_no_blank[index+1:]
                            #Remove parenthesis if they exists on the function name
                            if function.find('(') != -1:
                                #Check if closing parenthesis of the functions is on the same line
                                open_parenthesis = open_parenthesis + function.count('(') - function.count(')')
                                function = function.split('(')[0]
                            if function in functions and function not in path:
                                tmp.write('c ')
                        tmp.write(line)
            os.remove(directory+files)
            os.rename(directory+'tempfile.txt', directory+files)
    
    
if __name__ == '__main__':
    main()