# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:45:30 2019

@author: jga6170
"""

import pandas as pd

def main():
    df_decimate = diezmado(counters_metrics)
    
def power_model(df_decimate, counters_metrics):
    CPU_COUNTERS = ['INST_RETIRED', 'l2_rqsts:0x1', 'l2_rqsts:0x3', 'l2_rqsts:0x8', 'l2_rqsts:0x20', \
    'uops_dispatched:core', 'LLC_MISSES:0x41', 'LLC_REFS:0x4f', 'l1d:0x1', 'resource_stalls:any']
    df_cpu_decimate = df_decimate.loc[:, CPU_COUNTERS]
    for index, row in df_cpu_decimate.iterrows():
        print(index, row)
    
def diezmado(counters_metrics):
    df = counters_metrics.reset_index()
    result = pd.DataFrame(columns=df.columns)
    cycle = 0
    
    for path in range(df.Path.max() + 1):
        start = 0
        end = 100
        df_path = pd.DataFrame(df[df.Path == path])
        df_size = len(df_path)
        for i in range(int(df_size/ 100)+1):
            data = df_path.iloc[start:end, 2:]
            if len(data) != 100:
                end = (end - 100 + len(data))
                cycle += (len(data) / 10)
            else:
                cycle += 10
            data = data.sum()
            data["Path"] = path
            data["Cycles(s)"] = cycle
            result = result.append(data, ignore_index=True)
            start += 100 
            end += 100
    return result
    
def power_formula(data):
    result = (data['l1d:0x1'].item() + 1 / data['l2_rqsts:0x20'].item() +1) + \
             ((data['resource_stalls:any'].item()+1 * data['LLC_REFS:0x4f'].item()+1 * \
             (data['INST_RETIRED'].item()+1)**2) \ data['uops_dispatched:core'].item()+1)