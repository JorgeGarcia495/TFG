#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

#Importing libraries
import subprocess
import shutil
import assembly_instructions_count as aic
import source_code_parser as parser
import loop_count as lc
import upperbound_functions as uf
import instruction_expression as iexp
import instruction_upperbounds as iupp


def main():
    """Entrypoint of the module
    """
    aic.create_asm()
    delete_files()
    parser.parse()
    #This file should be deleted togetger with 'upperbound.sh'
    subprocess.check_call('./upperbound2.sh')
    return execute_mains()
    
#TODO: Include tasks performed on ".sh" at this point
def delete_files():
    """ Cleans the directory where the instructions are going to be calculated
    """
    shutil.rmtree('../results/upper_bound/nas_bt_upper_bound')
    #os.remove('upper_bound/upperbound_bt')
    shutil.copytree('../../nas_bt', '../results/upper_bound/nas_bt_upper_bound')
    #subprocess.Popen(["make", "clean"], stdout=subprocess.PIPE, cwd="./upper_bound/nas_bt_upper_bound")
    
def execute_mains():
    """ Executes the differents steps to estimate the instructions of a program
    """
    lc.count()
    uf.functions()
    iupp.upperbounds()
    result = iexp.total_instructions()
    return result

if __name__ == '__main__':
    main()