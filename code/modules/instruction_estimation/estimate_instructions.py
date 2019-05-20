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

#TODO: Create parameter for bin file
def main():
    """Entrypoint of the module
    """
    bin_location = '../../../nas_bt/bin/bt.B.x '
    directory = '../../results/instructions_estimation/'
    aic.create_asm(bin_location, directory)
    delete_files()
    parser.parse()
    execute_commands()
    return execute_mains(bin_location, directory)
    
def delete_files():
    """ Cleans the directory where the instructions are going to be calculated
    """
    directory = '../../results/upper_bound/nas_bt_upper_bound'
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

def execute_commands():
    command_list = []
    command_list.append('make -C ../../results/upper_bound/nas_bt_upper_bound/ clean')
    command_list.append('make -C ../../results/upper_bound/nas_bt_upper_bound/ BT CLASS=B')
    command_list.append('make -C ../../results/upper_bound/nas_bt_upper_bound/ clean')
    command_list.append('../../results/upper_bound/nas_bt_upper_bound/bin/bt.B.x > ../../results/upper_bound/upperbound_sc')
    for command in command_list:
        try:
            subprocess.check_call(shlex.split(command))
        except subprocess.CalledProcessError as e:
            logger.error(e)
            raise

if __name__ == '__main__':
    main()