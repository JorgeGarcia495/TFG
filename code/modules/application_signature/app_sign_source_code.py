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

def main(cg, labels, function_sintax, comment_sintax, code_directory, clase):
    """Locates the main file of the application to analyze
    """
    functions = list(labels.values())
    try:
        workspace = '../../results/'+code_directory + '/' + clase + '/application_signature/'
        #Delete existing files
        if os.path.exists(workspace):
            shutil.rmtree(workspace)
        os.mkdir(workspace)
        required_files = ['Makefile', 'header.h']
        for index, row in cg.iterrows():
            directory = workspace+str(index)
            #Copy source code
            shutil.copytree('../../../source_code', directory)
            directory = directory+'/'+code_directory+'/'
            #Iterate source code files
            for file in os.listdir(directory):
                #Delete if not needed 
                if not file.endswith('.f') and not file.endswith('.h') and file not in required_files:
                    os.remove(directory+file)
                    #Comment not needed functions on main file
            remove_unneeded_functions(directory, functions, row, function_sintax, comment_sintax)
    except FileNotFoundError as e:
        logger.error(e)
        raise
        
def remove_unneeded_functions(directory, functions, path, function_sintax, comment_sintax):
    """Removes the functions not needed on each path from the main file of the application
    """
    for files in os.listdir(directory):
        if files.split('.')[0].lower() in path.values:
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
                            if function in functions and function not in path.values:
                                tmp.write(comment_sintax)
                            #Check if there is a function
                        if line_no_blank.startswith(function_sintax) :
                            #Get name of the function to call
                            index = line_no_blank.index(" ")
                            function = line_no_blank[index+1:]
                            #Remove parenthesis if they exists on the function name
                            if function.find('(') != -1:
                                #Check if closing parenthesis of the functions is on the same line
                                open_parenthesis = open_parenthesis + function.count('(') - function.count(')')
                                function = function.split('(')[0]
                            if function in functions and function not in path.values:
                                tmp.write(comment_sintax)
                        tmp.write(line)
            os.remove(directory+files)
            os.rename(directory+'tempfile.txt', directory+files)
    
    
if __name__ == '__main__':
    main()
