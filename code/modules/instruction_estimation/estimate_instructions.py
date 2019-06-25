#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
import os
import logging
import shutil
import shlex
import subprocess
from . import assembly_instructions_count as aic
from . import source_code_parser as parser
from . import loop_count as lc
from . import upperbound_functions as uf
from . import instruction_expression as iexp
from . import instruction_upperbounds as iupp

logger = logging.getLogger(__name__)

def main(binary_name):
    """Entrypoint of the module
    """
    bin_location = '../../../nas_bt/bin/'+binary_name
    directory = '../../results/instructions_estimation/'
    upperbound_directory = '../../results/upper_bound/upperbound_source_code/'
    aic.create_asm(bin_location, directory)
    delete_files(upperbound_directory)
    parser.parse(upperbound_directory)
    execute_commands(upperbound_directory, binary_name)
    return execute_mains(bin_location, directory)
    
def delete_files(directory):
    """ Cleans the directory where the instructions are going to be calculated
    """
    if os.path.exists(directory):
            shutil.rmtree(directory)
    #os.remove('upper_bound/upperbound_bt')
    shutil.copytree('../../../nas_bt', directory)
    #subprocess.Popen(["make", "clean"], stdout=subprocess.PIPE, cwd="./upper_bound/nas_bt_upper_bound")
    
def execute_mains(bin_location, directory):
    """ Executes the differents steps to estimate the instructions of a program
    """
    lc.count(directory)
    uf.functions(bin_location, directory)
    iupp.upperbounds(bin_location, directory)
    result = iexp.total_instructions(bin_location, directory)
    return result

def execute_commands(directory, binary_name):
    command_list = []
    command_list.append('make -C '+directory+' clean')
    command_list.append('make -C '+directory+' BT CLASS=B')
    command_list.append('make -C '+directory+' clean')
    command_list.append(directory+'bin/'+binary_name+' > ../../results/upper_bound/upperbound_sc')
    for command in command_list:
        try:
            subprocess.check_call(shlex.split(command))
        except subprocess.CalledProcessError as e:
            logger.error(e)
            raise

if __name__ == '__main__':
    main()