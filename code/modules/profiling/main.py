#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import time
import signal
import shlex
import subprocess
import multiprocessing

def multiprocess_func(path, directory):
    """ Starts the dynamic profiling for a determined period of time
    """
    #Path lo store the profiling data
    temp_directory = directory+path+"/bin/"
    #Binary to execute
    target = temp_directory+path
    print('Profiling', path)
    #Metrics/counters to retrieves
    args = 'ocount -e INST_RETIRED -i 1 -f '+temp_directory+'temp_file'+target
    #Start of the profiling
    proc = subprocess.Popen(shlex.split(args), shell=False)
    time.sleep(40)
    #Kill subprocess
    proc.kill()
    try:
        #Kill childs of the subprocess(Binary execution)
        pid = int(subprocess.check_output(['pidof', '-s', path]))
        os.kill(pid, signal.SIGKILL)
    except subprocess.CalledProcessError:
        print('Nothing to do')

def run_binaries():
    """ Executes the existing binary to carry out a dynamic profiling
    """
    starttime = time.time()
    #Number of available processors
    processors = multiprocessing.cpu_count()
    print('Number of processors:', processors)
    #Location of binaries
    directory = '../../results/cg/source_code_paths/'
    files_number = os.listdir(directory)
    
    #Start of the tasks with parallelism
    with multiprocessing.Pool(processors) as pool:
        processes = [pool.apply_async(multiprocess_func, (file,directory,)) for file in files_number]
        for proc in processes:
            print(proc.get())
    
    print('All paths has been executed in {} seconds'.format(time.time() - starttime))
    
if __name__ == '__main__':
    run_binaries()
