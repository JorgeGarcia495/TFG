#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import logging
import subprocess

logger = logging.getLogger(__name__)

#TODO: Check privileges on creating '.sh' file
def main(binary_name, code_directory, verbose):
    """Creates and executes a script to generate a binary for every path
    """
    print("Start of binaries generation")
    #Directory to iterate
    directory = '../../results/cg/source_code_paths/'
    #Directory to store the binaries to generate
    bin_directory = './bin/'
    #Task to performed on the new script
    make_clean = 'make clean\n'
    for dirs in os.listdir(directory):
        print('Generating binary for path', dirs)
        if os.path.exists(directory+dirs+'/bin/'+dirs):
            os.remove(directory+dirs+'/bin/'+dirs)
        #Creation of the script
        with open(directory+dirs+'/make_bin.sh', 'w') as bin_file:
            bin_file.write('#! /bin/bash\n')
            bin_file.write(make_clean+'\n')
            bin_file.write('make '+code_directory+' CLASS=B\n')
            bin_file.write('mv '+bin_directory+binary_name+' '+bin_directory+binary_name+'_'+dirs+'\n')
            bin_file.write(make_clean)
        bin_file.close()
        try:
            #Changing privileges so script can be executed automatically
            os.chmod(directory+dirs+'/make_bin.sh', 0o777)
            #Move to directory where script is to be executed
            cwd = os.getcwd()
            #Change cwd to execute script generating the binary
            os.chdir(directory+dirs)
            if verbose:
                subprocess.check_call('./make_bin.sh')
            else:
                subprocess.check_call('./make_bin.sh', stdout=subprocess.PIPE, shell=False)
                
            os.chdir(cwd)
        except FileNotFoundError as e:
            logger.error(e)
            raise
    print('End of binaries generation')

if __name__ == '__main__':
    main()
