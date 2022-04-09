"""
Main module to create & manipulate diagnostics list.
"""

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