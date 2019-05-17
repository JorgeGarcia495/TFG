#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import time
import subprocess
import multiprocessing

def multiprocess_func(path, directory):
    target = directory+path+"/bin/"+path
    proc = subprocess.Popen('ocount -e INST_RETIRED -i 1 -f temp_file '+target, shell=True)
    print('Profiling', path)
    time.sleep(10)
    proc.kill()

#TODO: Add documentation
def run_binaries():
    starttime = time.time()
    processors = multiprocessing.cpu_count()
    print('Number of processors:', processors)
    directory = '../../results/cg/source_code_paths/'
    files_number = os.listdir(directory)
    
    with multiprocessing.Pool(processors) as pool:
        processes = [pool.apply_async(multiprocess_func, (file,directory,)) for file in files_number]
        for proc in processes:
            print(proc.get())
    
    print('All paths has been executed in {} seconds'.format(time.time() - starttime))
    
if __name__ == '__main__':
    run_binaries()
