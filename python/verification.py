#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 17:20:49 2022

@author: mpoinell
"""

import mitgcm_routines
import matplotlib.pyplot as plt

#file = 'tests/STDOUT.0000'
file1 = '/nobackupp11/mpoinell/larsen/run_larsen03c/output/STDOUT.345600'
file2 = '/nobackupp11/mpoinell/larsen/run_larsen03c/output/STDOUT.347400'
file3 = '/nobackupp11/mpoinell/larsen/run_larsen03c/output/STDOUT.375600'
file4 = '/nobackupp11/mpoinell/larsen/run_larsen03c/output/STDOUT.405600'
file5 = '/nobackupp11/mpoinell/larsen/run_larsen03c/output/STDOUT.448800'
file6 = '/nobackupp11/mpoinell/larsen/run_larsen03c/output/STDOUT.691200'
file7 = '/nobackupp11/mpoinell/larsen/run_larsen03c/STDOUT.0000'

df = mitgcm_routines.createDFfrommultipleSTD(file1,file2,file3,file4,file5,file6,file7)
#mitgcm_routines.MonitorSTDOUT(file6)

df.plot(x='time_tsnumber',y='seaice_heff_mean')