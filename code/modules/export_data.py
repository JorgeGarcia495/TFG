#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import csv
import pandas as pd

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
             
def export_multi_index_dataframe_to_excel(name, data, cols):
    aux = pd.DataFrame(data)
    multi_index = [aux.iloc[:, 0], aux.iloc[:,1]]
    data = pd.DataFrame(aux.iloc[:, 2:])
    data.columns = cols
    data.index = multi_index
    data.to_excel(name, header = True, index = True)