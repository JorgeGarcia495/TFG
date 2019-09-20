# -*- coding: utf-8 -*-
"""
@author: Jorge García Villanueva <jorgeg09@ucm.es>
"""

class Data():
    def __init__(self, clase, code_directory, main_function, function_sintax, 
                 comment_sintax, binary_name, main_file_name, language, 
                 sequential, verbose):
        self.clase = clase
        self.code_directory = code_directory
        self.main_function = main_function
        self.function_sintax = function_sintax
        self.comment_sintax = comment_sintax
        self.binary_name = binary_name
        self.main_file_name = main_file_name
        self.language = language
        self.sequential = sequential
        self.verbose = verbose

    def __str__(self):
        return """Clase: {} \nCode Directory: {}\nMain Function: {}\nFunction sintax: {}\n
            Comment Sintax: {}\nBinary Name: {}\n Main File Name: {}\n
            Language: {}\nSequential: {}\nVerbose: {}""".format(self.clase, 
                    self.code_directory, self.main_function, self.function_sintax,
                    self.comment_sintax, self.binary_name, self.main_file_name, 
                    self.language, self.language, self.sequential, self.verbose)
        
    def set_source_directory(self, source_directory):
        self.source_directory = source_directory
        
    def set_results_directory(self, results_directory):
        self.results_directory = results_directory
