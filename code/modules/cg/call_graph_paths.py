#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

import pandas as pd

def main():
    """ Entrypoint of the module
    """
    paths, labels = get_paths()
    paths = complete_paths(paths)
    paths = delete_repeated_paths(paths)
    result = rename_dict(paths, labels)
    return result, labels

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

def complete_paths(paths):
    """ Gets the complete paths of the application to profile
    """
    result = []
    elements = 0
    minimum_number = min(paths.keys())
    for key, values in paths.items():
        elements += len(values)
    for i in range(elements):
        result.append(add_children(paths, minimum_number, i+1))
    return [res for res in result if len(res) > 0]

def add_children(graph, start, end, path=[]):
    """ Algorithm to retrieve the children of a node
    """
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph.keys():
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = add_children(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def delete_repeated_paths(paths):
    """ If there is a path contained on a bigger one, it is deleted
    """
    removal_list = []
    result = [item for lista in paths for item in lista]

    for path in result:
        for path2 in result:
            if path != path2 and all(x in path for x in path2):
                if path2 not in removal_list:
                    removal_list.append(path2)
    
    return [x for x in result if x not in removal_list]

def rename_dict(paths, labels):
    """ Modifies the values(numbers) of the paths(cg) to its label
    """
    df = pd.DataFrame(paths)
    return df.applymap(lambda x: labels.get(x))