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

def main(cg):
    """Entrypoint of the module
    """
    generate_code_paths(cg)

def generate_code_paths(cg):
    """Locates the main file of the application to analyze
    """
    try:
        shutil.rmtree('../../results/cfg/source_code_paths/')
        for index, path in enumerate(cg):
            directory = '../../results/cfg/source_code_paths/'+str(index)
            shutil.copytree('../../../nas_bt', directory)
            for file in os.listdir('../../results/cfg/source_code_paths/'+str(index)+'/BT/'):
                if file.split('.')[0] not in path and file != 'bt.f' and file != 'Makefile' and not file.endswith('.h'):
                    os.remove('../../results/cfg/source_code_paths/'+str(index)+'/BT/'+file)
            remove_unneeded_functions(directory, path)
    except FileNotFoundError as e:
        logger.error(e)
        raise
        
#TODO: Remove the static main by a dynamic one inserting it as a parameter
def remove_unneeded_functions(directory, path):
    """Removes the functions not needen on each path from the main file of the application
    """
    with open(directory+'/BT/bt.f', encoding="utf-8") as file:
        with open(directory+'/BT/tempfile.txt', 'w') as tmp:
            for line in file:
                line_no_blank = line.strip()
                if line_no_blank.startswith('call') and line_no_blank.split(' ')[1] not in path:
                    tmp.write('c ')
                tmp.write(line)
    os.remove(directory+'/BT/bt.f')
    os.rename(directory+'/BT/tempfile.txt', directory+'/BT/bt.f')
    
if __name__ == '__main__':
    main()