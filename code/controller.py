# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import time
import pandas as pd

from modules import export_data as export
from modules.cg import call_graph as call_graph
from modules.application_signature import app_sign_source_code as as_source_code
from modules.application_signature import app_sign_binaries as as_binaries
from modules.instruction_estimation import estimate_instructions as estimate
from modules.profiling import main as profiling
from modules.profiling import main_sequential as sequential_profiling
from modules.signals_reconstruction import main as signal_rec
from modules.energy_estimation import main as energy_estim


def run(data):
    """ Runs every module to estimate the energy consumption of the application to analyze
    """
    modules_time = pd.DataFrame({}, columns=['Module', 'Time'])
    cg, labels, modules_time = execute_call_graph_module(data, modules_time)
    #inst_est, modules_time =  execute_instruction_estimation_module(binary_name, code_directory, modules_time, verbose)
    modules_time = execute_application_signature(cg, labels, data, modules_time)
    modules_time = execute_dynamic_profiling(data, modules_time)
    ipc, counter_means, counters_metrics, execution_times, modules_time = execute_signals_reconstruction(cg, modules_time, data)
    df_decimate, power_profile, energy, modules_time = execute_energy_estimation(counter_means, execution_times, modules_time, data)
    export_results(cg, ipc, counter_means, counters_metrics, execution_times, df_decimate, power_profile, energy, modules_time, data)
    return energy
    
    
def execute_call_graph_module(data, modules_time):
    """ Runs the call graph module
    """
    print('Started execution of Call Graph Module')
    starttime = time.time()
    os.chdir('modules/cg')
    cg, labels = call_graph.main(data.main_file_name, data.verbose, data.code_directory, data.clase)
    if cg.empty:
        raise Exception('Error executing CFG module')
    os.chdir('../..')
    exec_time = time.time() - starttime
    modules_time = modules_time.append({'Time' : round(exec_time, 2), 'Module' : 'Call_Graph'}, ignore_index=True)
    print('Call Graph module executed in {} seconds'.format(exec_time))
    return cg, labels, modules_time

def execute_instruction_estimation_module(binary_name, code_directory, modules_time, verbose):
    """ Runs the instruction estimation module
    """
    print('Started execution of Instruction Estimation Module')
    starttime = time.time()
    os.chdir('modules/instruction_estimation')
    result = estimate.main(binary_name, code_directory, verbose)
    os.chdir('../..')
    exec_time = time.time() - starttime
    modules_time =  modules_time.append({'Time' : round(exec_time, 2), 'Module' : 'Instruction_estimation'}, ignore_index=True)
    print('Instructions estimation module executed in {} seconds'.format(exec_time))
    return result, modules_time

def execute_application_signature(cg, labels, data, modules_time):
    print('Started execution of Application Signature Module')
    starttime = time.time()
    os.chdir('modules/application_signature')
    as_source_code.main(cg, labels, data)
    as_binaries.main(data) 
    os.chdir('../..')
    exec_time = time.time() - starttime
    modules_time =  modules_time.append({'Time' : round(exec_time, 2), 'Module' : 'Application_Signature'}, ignore_index=True)
    print('Instructions estimation module executed in {} seconds'.format(exec_time))
    return modules_time

def execute_dynamic_profiling(data, modules_time):
    """ Runs the profiling module
    """
    print('Started execution of Dynamic Profiling')
    starttime = time.time()
    os.chdir('modules/profiling')
    if(data.sequential):
        sequential_profiling.main(data)
    else:
        profiling.run_binaries(data)
    os.chdir('../..')
    exec_time = time.time() - starttime
    modules_time = modules_time.append({'Time' : round(exec_time, 2), 'Module' : 'Profiling'}, ignore_index=True)
    print('Profiling executed in {} seconds'.format(exec_time))
    return modules_time
    
def execute_signals_reconstruction(cg, modules_time, data):
    """ Runs the signals reconstruction module
    """
    print('Started execution of Signal Reconstruction')
    starttime = time.time()
    os.chdir('modules/signals_reconstruction')
    ipc, counters_means, counters_metrics, execution_times = signal_rec.reconstruct(cg, data)
    os.chdir('../..')
    exec_time = time.time() - starttime
    modules_time = modules_time.append({'Time' : round(exec_time, 2), 'Module' : 'Signal_Reconstruction'}, ignore_index=True)
    print('Signal Reconstruction executed in {} seconds'.format(exec_time))
    return ipc, counters_means, counters_metrics, execution_times, modules_time

def execute_energy_estimation(means, execution_times, modules_time, data):
    """ Runs the energy consumption estimation module
    """
    print('Started execution of Energy Estimation Module')
    starttime = time.time()
    os.chdir('modules/energy_estimation')
    df_decimate, power_profile, energy = energy_estim.main(means, execution_times, data.code_directory, data.clase)
    os.chdir('../..')
    exec_time = time.time() - starttime
    modules_time = modules_time.append({'Time' : round(exec_time, 2), 'Module' : 'Energy_Estimation'}, ignore_index=True)
    print('Energy Estimation module executed in {} seconds'.format(exec_time))
    return df_decimate, power_profile, energy, modules_time

def export_results(cg, ipc, counters_means, counters_metrics, execution_times, df_decimate, power_profile, energy, modules_time, code_directory, clase):
    """ Exports the results obtained by the framework
    """
    print('Start of results exportation')
    starttime = time.time()
    results_dir = 'results/'
    signal = results_dir+code_directory+'/'+clase+'/signal_reconstruction/'
    energy_estimation_path = results_dir+code_directory+'/'+clase+'/energy_estimation/'
    if not os.path.exists(signal):
        os.mkdir(signal)
    export.export_dataframe(cg, results_dir+code_directory+'/'+clase+'/paths')
    export.export_dataframe(execution_times, signal+'execution_times')
    export.export_dataframe(ipc, signal+'ipc')
    export.export_dataframe(counters_metrics, signal+'counters_metrics')
    export.export_dataframe(counters_means, signal+'counters_means')
    export.export_dataframe(df_decimate, energy_estimation_path+'decimate')
    export.export_dataframe(power_profile, energy_estimation_path+'power_profile')
    export.export_dataframe(energy, energy_estimation_path+'energy')
    exec_time = time.time() - starttime
    modules_time = modules_time.append({'Time' : round(exec_time, 2), 'Module' : 'Export_Results'}, ignore_index=True)
    modules_time = modules_time.set_index(['Time'])
    export.export_dataframe(modules_time, results_dir+code_directory+'/'+clase+'/modules_time')
    print('Results exported in {} seconds'.format(exec_time))
