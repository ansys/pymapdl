import os
import numpy as np


def Run(inputfile, jobname='file', nproc=4, outname='output.txt', memory=0,
        batch=False):
    """ Runs ANSYS """

    # Check if input file exists
    if not os.path.isfile(inputfile):
        raise Exception('Input file does not exist')
        
    if os.path.isfile(jobname + '.lock'):
        raise Exception('Lock file exists for jobname: ' + jobname)
    
    options = ''
    options += '-j {:s} '.format(jobname)
    options += '-np {:d} '.format(nproc)
    options += '-o {:s} '.format(outname)
    options += '-i {:s} '.format(inputfile)
    if batch:
        options += '-b '        

    if memory:
        options += '-m {:d} '.format(memory)
    
    command = "unshare -n -m -- sh -c 'sudo ifconfig lo up; /usr/ansys_inc/v150/ansys/bin/ansys150 {:s}'".format(options)

    c = os.system(command)
    return c

