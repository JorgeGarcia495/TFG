#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva
"""

import os
import logging
import subprocess

logger = logging.getLogger(__name__)

#TODO: Delete 'bt.B.x' by a parameter name
#TODO: Check privileges on creating '.sh' file
def main():
    """Creates and executes a script to generate a binary for every path
    """
    #Directory to iterate
    directory = '../../results/cfg/source_code_paths/'
    #Directory to store the binaries to generate
    bin_directory = './bin/'
    #Task to performed on the new script
    make_clean = 'make clean\n'
    for dirs in os.listdir(directory):
        #Creation of the script
        with open(directory+dirs+'/make_bin.sh', 'w') as bin_file:
            bin_file.write('#! /bin/bash\n')
            #bin_file.write(make_clean+'\n')
            bin_file.write('make BT CLASS=B\n')
            bin_file.write('mv '+bin_directory+'bt.B.x '+bin_directory+dirs+'\n')
            bin_file.write(make_clean)
        bin_file.close()
        try:
            #Changing privileges so script can be executed automatically
            os.chmod(directory+dirs+'/make_bin.sh', 0o777)
            #Move to directory where script is to be executed
            cwd = os.getcwd()
            #Change cwd to execute script generating the binary
            os.chdir(directory+dirs)
            subprocess.check_call('./make_bin.sh')
            #Back to original cwd
            os.chdir(cwd)
        except FileNotFoundError as e:
            logger.error(e)
            raise

    
if __name__ == '__main__':
    main()
