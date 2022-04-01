#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 13:47:56 2021

@author: mpoinell

Handy routines to work with MITgcm outputs

"""
import pandas as pd

class STDOUTtoDF:
    """
        This class takes a STDOUT file and generates a pandas Dataframe
    """
    
    def __init__(self,PATH):
        """
        Class constructor to initialize PATH to STDOUT directory
        """
        assert type(PATH) == str, 'PATH is not a string'
        assert 'STDOUT' in PATH, 'PATH does not lead to STDOUT file'

        self.PATH = PATH
        
    
    def getPATH(self):
        """
        Returns PATH to STDOUT
        """
        return self.PATH
    
    def diagnosticsList(self):
        
        column = list()
        with open('monitor_diagnostics.txt','r') as std_var:
            for line in std_var.readlines():
                column.append(line.rstrip())
    
        return column
    
    def createDF(self):
        
        # Load column name
        diagnostics = self.diagnosticsList()

        # initialize support dictionary     
        new_index = list()
        new_value = list()
        
        dictionary_STDOUT = dict()
        with open(self.PATH,'r') as std_file:
    
            for line in std_file.readlines():
                # read and append values that are referring to monitored diagnostics
                
                if line[25:45].rstrip() in diagnostics:
                    try:
                        new_value.append(float(line[-20:].strip())) 
                        new_index.append(line[25:45].rstrip())
                    except(ValueError, IndexError):
                        new_value.append(float('nan')) 
                        new_index.append(line[25:45].rstrip())
            
            # build support dictionary
            for key, value in zip(new_index, new_value):
                if key not in dictionary_STDOUT:
                    dictionary_STDOUT[key] = [value]
                else:
                   dictionary_STDOUT[key].append(value)
        
        # returns dataframe 
        return pd.DataFrame(dictionary_STDOUT)
    
    def createDFfrommultipleSTD(self,*files):
        
        diagnostics = self.diagnosticsList()
        dictionary_STDOUT = dict()
        
        for file in files:
            with open(file, 'r') as std_file:
                new_index = list()
                new_value = list()
                
                for line in std_file.readlines():
                    if line[25:45].rstrip() in diagnostics:
                        try:
                            new_value.append(float(line[-20:].strip())) 
                            new_index.append(line[25:45].rstrip())
                        except(ValueError, IndexError):
                            new_value.append(float('nan')) 
                            new_index.append(line[25:45].rstrip())
                            
                # build support dictionary
                for key, value in zip(new_index, new_value):
                    if key not in dictionary_STDOUT:
                        dictionary_STDOUT[key] = [value]
                    else:
                        dictionary_STDOUT[key].append(value)
                        
        # returns dataframe 
        return pd.DataFrame(dictionary_STDOUT)