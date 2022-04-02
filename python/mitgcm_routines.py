#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 09:48:24 2022

@author: mpoinell

"""

import pandas as pd

def GenMonitorDiagnostics():
    """
    Write MonitorDiagnostics.txt based on a specific STDOUT file

    Returns
    -------
    None.

    """
    
    PATH = '/nobackupp11/mpoinell/larsen/run_larsen00e/output/'

    with open(PATH + 'STDOUT.437760','r') as std_file:
        column = []    
    
        for line_number, line in enumerate(std_file.readlines()):
        
            # generate dataframe columns
            if (line_number > 4045 and line_number < 4277) and \
                (line[25:27] != '==' and line[25:27] != 'd ' and line[25:27] != 'gi'):
                    column.append(line[25:45].rstrip())
            
        with open('MonitorDiagnostics.txt','w') as std_var:
            for variable in column:
                std_var.write(variable + '\n') 


def diagnosticsList():
    """
    Routine to read MonitorDiagnostics.txt

    Returns
    -------
    column : list of diagnostics to monitor
    """
    
    # set the path to MonitorDiagnostics.txt, created with genmonitorDiagnostics
    MonitorDiagnostics = '/nobackupp11/mpoinell/larsen/python/MonitorDiagnostics.txt'
    
    # Initialize empy list
    diagnostics_list = list()
    
    with open(MonitorDiagnostics,'r') as std_var:
        
        # read line and append it to 
        for line in std_var.readlines():
            diagnostics_list.append(line.rstrip())
    
    return diagnostics_list



    
def createDFfrommultipleSTD(*files):
    
    
    diagnostics = diagnosticsList()
    
    dictionary_STDOUT = dict()
        

    for file in files:    
        print('Open file!')
        with open(file, 'r') as std_file:
            
            new_diags = list()
            new_value = list()
            
            print('Read line!')
            for line in std_file.readlines():                
            
                if line[25:45].rstrip() in diagnostics:
                    try:
                        new_value.append(float(line[-20:].strip())) 
                        new_diags.append(line[25:45].rstrip())
                    except(ValueError, IndexError):
                        new_value.append(float('nan')) 
                        new_diags.append(line[25:45].rstrip())
                            
            # build support dictionary
            print('Gen Dictionary!')
            for key, value in zip(new_diags, new_value):
                if key not in dictionary_STDOUT:
                    dictionary_STDOUT[key] = [value]
                else:
                    dictionary_STDOUT[key].append(value)
    
    # returns dataframe 
    return dictionary_STDOUT