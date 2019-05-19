#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import csv

def export_multiple_lists_csv(data, name):
    if os.path.exists(name):
        os.remove(name)
    with open(name, 'w') as file:
        data_writer = csv.writer(file, delimiter=',', dialect='excel')
        for index, path in enumerate(data):
            aux = [index]
            aux.extend(path)
            data_writer.writerow(aux)
        file.close()
        
def export_list_csv(data, name):
    if os.path.exists(name):
        os.remove(name)
    with open(name, 'w') as file:
        data_writer = csv.writer(file, delimiter=',', dialect='excel')
        for index, path in enumerate(data):
            aux = [index]
            aux.append(path)
            data_writer.writerow(aux)
        file.close()
        
def export_dict_csv(data, name):
    if os.path.exists(name):
        os.remove(name)
    csv_columns = ['Path']
    for values in data.values():
        for key, value in values.items():
            csv_columns.append(key)
        break
    with open(name, 'w') as file:
         data_writer = csv.writer(file, delimiter=',', dialect='excel')
         data_writer.writerow(csv_columns)
         for keys, values in data.items():
             aux = [keys]
             for key, value in values.items():
                 aux.append(value)
             data_writer.writerow(aux)
             
             data = list(instructions_per_path.values())
             name = '../results/instructions_per_path.csv'