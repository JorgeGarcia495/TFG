#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import time
import shlex
import psutil
import subprocess
import multiprocessing

def multiprocess_func(path, directory, binary_name, verbose):
    """ Starts the dynamic profiling for a determined period of time
    """
    #Path lo store the profiling data
    temp_directory = directory+path+"/bin/"
    binary_name = binary_name+'_'+path
    #Binary to execute
    target = temp_directory+binary_name
    #Metrics/counters to retrieves
    counters = 'CPU_CLK_UNHALTED,INST_RETIRED,LLC_MISSES:0x41,LLC_REFS:0x4f,BR_INST_RETIRED,BR_MISS_PRED_RETIRED,misalign_mem_ref:0x01,misalign_mem_ref:0x02,arith:fpu_div_active,resource_stalls:any,uops_dispatched:core,mem_trans_retired:0x02,mem_uops_retired:all_stores,l1d:0x01,l2_rqsts:0x01,l2_rqsts:0x03,l2_rqsts:0x08,l2_rqsts:0x20'
    args = 'ocount -e %s -i 1 -f %stemp_file_%s %s' % \
        (counters, temp_directory, path, target)
    print('Profiling', path)
    #Start of the profiling
    try:
        exec_time = time.time()
        proc = subprocess.Popen(shlex.split(args), stdout=subprocess.PIPE, shell=False)
        time.sleep(1)
        pid = int(subprocess.check_output(['pidof', '-s', binary_name]))
        binary_time = float('{}'.format(time.time() - exec_time))
        if verbose:
            print('Executing path: %s' % path)
        
        while pid and binary_time < 40:
            time.sleep(5)
            binary_time = float('{}'.format(time.time() - exec_time))
            if verbose:
                print('Time for path %s: %d seconds' % (path, binary_time))
            pid = int(subprocess.check_output(['pidof', '-s', binary_name]))

        #Kill subprocess
        proc.kill()
        if verbose:
            print('Time limit reached for path %s' % path)
        #Kill childs of the subprocess(Binary execution)
        os.system('kill -9 '+str(pid))
    except subprocess.CalledProcessError:
        if verbose:
            print(path, "was finished before the limit time")
        proc.kill()
    return 'Executed path %s ' % path
        
def run_binaries(data):
    """ Executes the existing binary to carry out a dynamic profiling
    """
    starttime = time.time()
    #Number of available physical processors
    processors = psutil.cpu_count(logical=False)
    print('Number of processors:', processors)
    #Location of binaries
    directory = data.results_directory
    files_number = os.listdir(directory)
    
    #Start of the tasks with parallelism
    with multiprocessing.Pool(processors) as pool:
        processes = [pool.apply_async(multiprocess_func, (name,directory, 
                    data.binary_name,data.verbose,)) for name in files_number]
        for proc in processes:
            print(proc.get())

        print('All paths has been executed in {} seconds'.format(time.time() - starttime))
