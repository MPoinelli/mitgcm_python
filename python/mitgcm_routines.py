"""
Main module to work with STDOUT files
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

    with open(PATH + 'STDOUT.437760', 'r') as std_file:
        column = []

        for line_number, line in enumerate(std_file.readlines()):

            # generate dataframe columns
            if (line_number > 4045 and line_number < 4277) and \
                    (line[25:27] != '==' and line[25:27] != 'd ' and line[25:27] != 'gi'):
                column.append(line[25:45].rstrip())

        with open('MonitorDiagnostics.txt', 'w') as std_var:
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

    with open(MonitorDiagnostics, 'r') as std_var:
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
    df : pandas dataframe containing diagnostics time series.

    """
    
    diagnostics = diagnosticsList()
    
    hash_table = {}
        
    counter = 0 
    
    for file in files:    
        counter += 1
        print('Reading file ' + str(counter) + '/' + str(len(files)))
        
        # Open STDOUT file
        with open(file, 'r') as std_file:
            
            # support arrays
            new_diags = list()
            new_value = list()
            
            # Read line by line
            for line in std_file.readlines():                
                
                # Store diagnostic and its associate value
                if line[25:45].rstrip() in diagnostics:
                    try:
                        new_value.append(float(line[57:].strip())) 
                        new_diags.append(line[25:45].rstrip())
                    except(ValueError, IndexError):
                        new_value.append(float('nan')) 
                        new_diags.append(line[25:45].rstrip())
                            
            # Find smaller list (obsolete, to be removed and tested)
            n = min(len(new_value),len(new_diags))
            
            # Build support hash
            for key, value in zip(new_diags[:n+1], new_value[:n+1]):
                if key not in hash_table:
                    hash_table[key] = [value]
                else:
                    hash_table[key].append(value)
    
    # Create dataframe so with equal column 
    df = pd.DataFrame({ key:pd.Series(value) for key, value in hash_table.items() })
    
    # remove duplicates and keep last value encountered (most recent file)
    df = df.drop_duplicates(subset='time_tsnumber', keep='last')
    print('DataFrame created')
    return df

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

    
    ## Velocities
    fig1, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    ax1.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_uvel_min"][-n:])
    ax1.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_uvel_max"][-n:])
    ax1.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_uvel_mean"][-n:])
    
    ax1.set(ylabel="dynstat_uvel")
        
    ax2.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_vvel_min"][-n:])
    ax2.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_vvel_max"][-n:])
    ax2.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_vvel_mean"][-n:])

    ax2.set(ylabel="dynstat_uvel")
    
    ax3.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_wvel_min"][-n:])
    ax3.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_wvel_max"][-n:])
    ax3.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_wvel_mean"][-n:])
    
    ax3.set(xlabel='time_secondsf', ylabel="dynstat_wvel")

    
    ## CFL condition
    fig2, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    ax1.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["advcfl_uvel_max"][-n:])
    ax1.set(ylabel="advcfl_uvel")
        
    ax2.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["advcfl_vvel_max"][-n:])
    ax2.set(ylabel="advcfl_uvel")
    
    ax3.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["advcfl_wvel_max"][-n:])
    ax3.set(xlabel='time_secondsf', ylabel="advcfl_wvel")

    
    ## Temp/SALINITY
    fig3, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    ax1.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_theta_min"][-n:])
    ax1.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_theta_max"][-n:])
    ax1.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_theta_mean"][-n:])
    
    ax1.set(ylabel="dynstat_theta")
        
    ax2.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_salt_min"][-n:])
    ax2.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_salt_max"][-n:])
    ax2.plot(df_STDOUT["time_secondsf"][-n:], df_STDOUT["dynstat_salt_mean"][-n:])
    
    ax2.set(xlabel='time_secondsf', ylabel="dynstat_salt")
                
if __name__ == "__main__":
    import sys
    mitgcm_routines(int(sys.argv[1]))      
