#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import os
import csv

def export(data):
    directory = '../results/paths.csv'
    if os.path.exists(directory):
        os.remove(directory)
    with open(directory, 'w') as file:
        for index, path in enumerate(data):
            data_writer = csv.writer(file, delimiter=',')
            path.insert(0, index)
            data_writer.writerow(data)
        file.close()

