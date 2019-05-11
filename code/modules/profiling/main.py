#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import time
import subprocess
import signal
import multiprocessing

def multiprocess_func(binary):
    #Check command
    proc = subprocess.Popen('sudo ocount -e INST_RETIRED -i 1 -f temp_file '+binary)
    time.sleep(40)
    os.kill(proc.pid, signal.SIGHUP)

def run_binaries():
    starttime = time.time()
    processes = []
    directory = '../../results/cfg/source_code_paths/'
    for paths in os.listdir(directory):
        path = directory+paths+'/bin/'
        cwd = os.getcwd()
        os.chdir(path)
        p = multiprocessing.Process(target=multiprocess_func, args=(paths,))
        processes.append(p)
        p.start()
        os.chdir(cwd)
    
    for process in processes:
        process.join()
    
    print('All paths has been executed in {} seconds'.format(time.time() - starttime))
    
if __name__ == '__main__':
    run_binaries()