#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
import os
import subprocess
import shutil
from . import assembly_instructions_count as aic
from . import source_code_parser as parser
from . import loop_count as lc
from . import upperbound_functions as uf
from . import instruction_expression as iexp
from . import instruction_upperbounds as iupp


def main():
    """Entrypoint of the module
    """
    bin_location = '../../../nas_bt/bin/bt.B.x '
    directory = '../../results/instructions_estimation/'
    aic.create_asm(bin_location, directory)
    delete_files()
    parser.parse()
    #This file should be deleted togetger with 'upperbound.sh'
    subprocess.check_call('./upperbound2.sh')
    return execute_mains(bin_location, directory)
    
#TODO: Include tasks performed on ".sh" at this point
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
    lc.count()
    uf.functions(bin_location, directory)
    iupp.upperbounds(bin_location, directory)
    result = iexp.total_instructions(bin_location, directory)
    return result

if __name__ == '__main__':
    main()