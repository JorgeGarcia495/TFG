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
        workspace = '../../results/cfg/source_code_paths/'
        #Delete existing files
        if os.path.exists(workspace):
            shutil.rmtree(workspace)
        for index, path in enumerate(cg):
            directory = workspace+str(index)
            #Copy source code
            shutil.copytree('../../../nas_bt', directory)
            #Iterate source code files
            for file in os.listdir(workspace+str(index)+'/BT/'):
                #Delete if not needed
                if file.split('.')[0] not in path and file != 'bt.f' and file.endswith('.f'):
                    os.remove(workspace+str(index)+'/BT/'+file)
                    #Comment not needed functions on main file
            remove_unneeded_functions(directory, functions, path)
    except FileNotFoundError as e:
        logger.error(e)
        raise
        
#TODO: Remove the static main by a dynamic one inserting it as a parameter
def remove_unneeded_functions(directory, functions, path):
    """Removes the functions not needen on each path from the main file of the application
    """
    with open(directory+'/BT/bt.f', encoding="utf-8") as file:
        with open(directory+'/BT/tempfile.txt', 'w') as tmp:
            for line in file:
                line_no_blank = line.strip()
                if line_no_blank.startswith('call') :
                    function = line_no_blank.split(' ')[1]
                    if function.find('(') != -1:
                        function = function.split('(')[0]
                    if function in functions and function not in path:
                        tmp.write('c ')
                tmp.write(line)
    os.remove(directory+'/BT/bt.f')
    os.rename(directory+'/BT/tempfile.txt', directory+'/BT/bt.f')
    
if __name__ == '__main__':
    main()