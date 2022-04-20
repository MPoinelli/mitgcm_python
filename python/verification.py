#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 17:20:49 2022

@author: mpoinell
"""

import mitgcm_routines


#file = 'tests/STDOUT.0000'
file = '/nobackupp11/mpoinell/larsen/run_larsen03c/STDOUT.0000'
df = mitgcm_routines.createDFfrommultipleSTD(file)
#mitgcm_routines.MonitorSTDOUT(file,1000)