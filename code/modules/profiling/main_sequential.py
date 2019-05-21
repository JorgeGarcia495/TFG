# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import time
import shlex
import logging
import subprocess
import multiprocessing

logger = logging.getLogger(__name__)

def handle_queues(input, output):
    """  Function run by worker processes
    """
    for func, args in iter(input.get, 'STOP'):
        result = execute_command(func, args)
        output.put(result)
        
def execute_command(func, args):
    """ Function used to execute the processes (Queues requires to pass the functions by inheritance)
    """
    result = func(*args)
    return result

def multiprocess_func(path, directory):
    """ Creates subprocesses to execute the binaries of the different paths
    """
    #Path lo store the profiling data
    temp_directory = directory+path+"/bin/"
    #Binary to execute
    target = temp_directory+path
    counters = 'CPU_CLK_UNHALTED,INST_RETIRED,LLC_MISSES:0x41,LLC_REFS:0x4f,BR_INST_RETIRED,BR_MISS_PRED_RETIRED,misalign_mem_ref:0x01,misalign_mem_ref:0x02,arith:fpu_div_active,resource_stalls:any,uops_dispatched:core,mem_trans_retired:0x02,mem_uops_retired:all_stores,l1d:0x01,l2_rqsts:0x01,l2_rqsts:0x03,l2_rqsts:0x08,l2_rqsts:0x20'
    args = 'ocount -e %s -i 1 -f %stemp_file %s' % \
        (counters, temp_directory, target)
    try:
        proc = subprocess.Popen(shlex.split(args), shell=False)
        print('Sleeping')
        time.sleep(10)
        #Kill execution of binary
        proc.kill()
        pid = int(subprocess.check_output(['pidof', '-s', path]))
        os.system('kill -9 '+str(pid))
    except subprocess.CalledProcessError:
        print(path, "was finished before the limit time")
    return 'Folder %s was created ' % path
    
def main():
    """  Controller of the script
    """
    start_time = time.time()
    directory = '../../results/cg/source_code_paths/'
    paths = os.listdir(directory)
    #Create queues
    task_queue = multiprocessing.Queue()
    done_queue = multiprocessing.Queue()
    #Creates tasks
    tasks = [(multiprocess_func, (path, directory)) for path in paths]
    
    #Adding tasks to queue
    for task in tasks:
        task_queue.put(task)
        
    #Executing tasks
    multiprocessing.Process(target=handle_queues, args=(task_queue, done_queue)).start()
        
    #Display tasks results
    for i in range(len(tasks)):
        print(done_queue.get())
    
    #Stop children process
    task_queue.put('STOP')
        
    print('All paths has been executed in {} seconds'.format(time.time() - start_time))

    
if __name__ == '__main__':
    main()