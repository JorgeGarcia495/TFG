# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
#For reading arguments
import sys
#To traverse directories
import os
#To execute a binary file(Doxygen)
import subprocess
#For logging purposes
import logging

logger = logging.getLogger(__name__)

def main():
    if(len(sys.argv) != 3):
        raise Exception("The programming language and location of the program is expected to be passed as an argument")
    else:
        language = sys.argv[1]
        directory = sys.argv[2]
        main = set_language(language)
        entry_file = search_file(directory, main)
        cfg = execute_binary(entry_file)
        if(cfg == 1):
            cfg_paths = get_cfg_paths(directory)
        else:
            raise Exception('Error getting paths from ".dot" file')
        print(cfg_paths)
        
def set_language(language):
    if(language == 'c++'):
        return 'main'
    elif(language == 'fortrand'):
        return 'open'
    else:
        raise Exception('The selected programming language is not supported by the application')
        
def search_file(directory, word):
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

def get_cfg_paths(directory):
    result = ''
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.dot'):
               result = directory + '\\' + file
               break
    if(result == ''):
        raise FileNotFoundError('.dot file not found')
    return result
    2
def execute_binary(entry_file):
    args = 'Doxygen ' + entry_file
    try:
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        result = popen.stdout.read()
        return result
    except ChildProcessError as e:
        logger.error(e)
        raise
    
main()
