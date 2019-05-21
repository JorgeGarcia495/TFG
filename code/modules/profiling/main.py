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

def multiprocess_func(path, directory):
    """ Starts the dynamic profiling for a determined period of time
    """
    #Path lo store the profiling data
    temp_directory = directory+path+"/bin/"
    #Binary to execute
    target = temp_directory+path
    counters = 'CPU_CLK_UNHALTED,INST_RETIRED,LLC_MISSES:0x41,LLC_REFS:0x4f,BR_INST_RETIRED,BR_MISS_PRED_RETIRED,misalign_mem_ref:0x01,misalign_mem_ref:0x02,arith:fpu_div_active,resource_stalls:any,uops_dispatched:core,mem_trans_retired:0x02,mem_uops_retired:all_stores,l1d:0x01,l2_rqsts:0x01,l2_rqsts:0x03,l2_rqsts:0x08,l2_rqsts:0x20'
    print('Profiling', path)
    #Metrics/counters to retrieves
    args = 'ocount -e ' + counters + ' -i 1 -f '+temp_directory+'temp_file '+target
    #Start of the profiling
    proc = subprocess.Popen(shlex.split(args), shell=False)
    time.sleep(10)
    #Kill subprocess
    proc.kill()
    try:
        #Kill childs of the subprocess(Binary execution)
        pid = int(subprocess.check_output(['pidof', '-s', path]))
        os.system('kill -9 '+str(pid))
    except subprocess.CalledProcessError:
        print(path, "was finished before the limit time")
        
def run_binaries():
    """ Executes the existing binary to carry out a dynamic profiling
    """
    starttime = time.time()
    #Number of available physical processors
    processors = psutil.cpu_count(logical=False)
    print('Number of processors:', processors)
    #Location of binaries
    directory = '../../results/cg/source_code_paths/'
    files_number = os.listdir(directory)
    
    #Start of the tasks with parallelism
    with multiprocessing.Pool(processors) as pool:
        processes = [pool.apply_async(multiprocess_func, (name,directory,)) for name in files_number]
        for proc in processes:
            print(proc.get())

        print('All paths has been executed in {} seconds'.format(time.time() - starttime))
        
    
if __name__ == '__main__':
    run_binaries()
