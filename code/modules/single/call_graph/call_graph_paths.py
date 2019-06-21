#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""
import os
import pandas as pd

def main():
    """ Entrypoint of the module
    """
    paths, labels = get_paths()
    paths = complete_paths(paths)
    paths = delete_repeated_paths(paths)
    result = rename_dict(paths, labels)
    export_paths(result)

def get_paths():
    """ Analyze the cg and returns the paths contained on it
    """
    paths = {}
    labels = {}
    with open('cgraph.dot') as file:
        for line in file:
            #Delete blank spaces
            line = line.strip()
            #Filter to find the paths
            if line.startswith('Node'):
                words = line.split()
                label = get_labels(words)
                first = int(words[0].split('Node')[1])
                if label != None:
                    labels[first] = label.lower()
                if words[2].find('Node') != -1:
                    second = int(words[2].split('Node')[1].lower())
                    if paths.get(first) == None:
                        paths[first] = [second]
                    else:
                        paths[first].append(second)
    return paths, labels


def get_labels(words):
    """ Based on the array passed as an argument, determines the label of each element
    """
    if words[1] != '->':
        labels = words[1].split('"')
        return labels[1]
    return None

def delete_repeated_paths(paths):
    """ If there is a path contained on a bigger one, it is deleted
    """
    result = []
    removal_list = []
    for path in paths:
        for values in path:
                result.append(values)        

    for path in result:
        for path2 in result:
            if path != path2 and all(x in path for x in path2):
                if path2 not in removal_list:
                    removal_list.append(path2)
    for rem in removal_list:
        result.remove(rem)
    return result


#TODO: Remove magic number '1000'
def complete_paths(paths):
    minimum_number = min(paths.keys())
    result = []
    for i in range(1000):
        result.append(add_children(paths, minimum_number, i+1))
    return [res for res in result if len(res) > 0]
    
def add_children(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph.keys():
        return []
    result = []
    for node in graph[start]:
        if node not in path:
            newpaths = add_children(graph, node, end, path)
            result = result + newpaths
    return result

def rename_dict(paths, labels):
    """ Modifies the values(numbers) of the paths(cg) to its label
    """
    df = pd.DataFrame(paths)
    return df.applymap(lambda x: labels.get(x))

def export_paths(paths):
    directory = '../../../results/single/call_graph/'
    if not os.path.exists(directory):
        os.mkdir(directory)
    paths.to_csv(directory+'paths.csv')
    paths.to_excel(directory+'paths.xlsx', header = False, index = True)