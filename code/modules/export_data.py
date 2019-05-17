#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import csv

def export_list_csv(data, name):
    directory = '../results/'
    if os.path.exists(directory+name):
        os.remove(directory+name)
    with open(directory+name, 'w') as file:
        for index, path in enumerate(data):
            path.insert(0, index)
        data_writer = csv.writer(file, delimiter=',', dialect='excel')
        data_writer.writerows(data)
        file.close()
