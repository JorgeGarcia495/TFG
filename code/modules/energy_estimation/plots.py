# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import shutil
import matplotlib.pyplot as plt

def check_path(path):
    """ Creates the directory passed as argument; If it exists already, it is 
    deleted and created again
    """
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
    except:
        raise Exception("Error trying to reach energy estimation folder")

def get_power_plots(power_profile):
    """ Generates the plots associated to the power profile of the application being analyzed
    """
    path = '../../results/energy_estimation/plots/'
    check_path(path)
    generate_plot(power_profile.TIME, power_profile.POWER_CPU, 'cpu', path)
    generate_plot(power_profile.TIME, power_profile.POWER_MEM, 'memory', path)
    
def generate_plot(x_axis, values, name, path):
    """ Creates a plot with the data passed as arguments
    """
    plt.figure(figsize=(9,4))
    plt.plot(x_axis, values, label=name)
    plt.title('BT - CLASS B (Power %s profile)' % name)
    plt.xlabel('Time(s)')
    plt.legend()
    plt.ylabel(name)
    plt.xlim(xmin=0, xmax=x_axis.max()+5)
    save_path = path+name+'.png'
    plt.savefig(save_path.replace(':', '_'))
    plt.cla()
