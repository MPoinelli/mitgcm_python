#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 09:48:24 2022

@author: mpoinell

"""

import pandas as pd

from matplotlib import pyplot as plt

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
    column : list of diagnostics
    """
    
    # set the path to MonitorDiagnostics.txt, created with genmonitorDiagnostics
    MonitorDiagnostics = 'MonitorDiagnostics.txt'
    
    # Initialize empy list
    diagnostics_list = list()
    
    with open(MonitorDiagnostics,'r') as std_var:
        
        # read line and append it to 
        for line in std_var.readlines():
            diagnostics_list.append(line.rstrip())
    
    return diagnostics_list



    
def createDFfrommultipleSTD(*files):
    """
    Parameters
    ----------
    *files : Single or multiple paths to STDOUT files.

    Returns
    -------
    dictionary_STDOUT : pandas dataframe containing diagnostics time series.

    """
    
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
                        new_value.append(float(line[57:].strip())) 
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
    
    return pd.DataFrame(dictionary_STDOUT)

def MonitorSTDOUT(file, n=None):
    """
    Parameters
    ----------
    file : Single path to a single STDOUT file
    n    : number of timestamps you want to plot
    
    Returns
    -------
    None.

    """
    
    df_STDOUT = createDFfrommultipleSTD(file)
       
    if n == None:
        n = len(df_STDOUT)
        
    # plt.plot(df_STDOUT["time_secondsf"],df_STDOUT["dynstat_uvel_min"])
    # plt.plot(df_STDOUT["time_secondsf"],df_STDOUT["dynstat_uvel_max"])

    
    plt.figure(1,figsize=(6,6))

    plt.subplot(3,1,1)
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_uvel_min"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_uvel_max"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_uvel_mean"][-n:])
    
    plt.xlabel("time_secondsf")
    plt.ylabel("dynstat_uvel")
        
    plt.subplot(3,1,2)
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_vvel_min"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_vvel_max"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_vvel_mean"][-n:])

    plt.xlabel("time_secondsf")
    plt.ylabel("dynstat_vvel")

    plt.subplot(3,1,3)
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_wvel_min"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_wvel_max"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_wvel_mean"][-n:])
    
    
    plt.figure(2,figsize=(6,6)) 

    plt.subplot(2,1,1)
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_theta_min"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_theta_max"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_theta_mean"][-n:])

    plt.xlabel("time_secondsf")
    plt.ylabel("dynstat_theta")

    plt.subplot(2,1,2)
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_salt_min"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_salt_max"][-n:])
    plt.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_salt_mean"][-n:])

    plt.xlabel("time_secondsf")
    plt.ylabel("dynstat_salt")
                
        