#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

inFile = 'brent_list/edd_HI_ba_T_9060.short.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc         = table['PGC']
d25         = table['d25']   # arcmin

inFile = 'has_Hall.SDSS.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_ex      = table['pgc']
ra      = table['ra']
dec      = table['dec']
sdss = table['SDSS']


all_indices = np.where(sdss == 1)
all_indices = all_indices[0]


for i in all_indices:
  if i>177 and i < 7422:
    
     #if pgc[i]==37036:
        #print i, pgc[i]
     pgc_dir = "pgc"+str(pgc[i])
     directory = "SDSS_ALL_Images/"+pgc_dir
     isDirAvailable =  os.path.isdir(directory)
     
     if isDirAvailable:
       subprocess.check_output(["rm", "-rf" , directory])
     subprocess.check_output(["mkdir" , directory])
     
     size = (d25[i]*5)/60.
     if size < 0.1:
       size = 0.1  # degree
     
     with cd(directory):
       
       
       command =  ["sdssall", "pgc"+str(pgc[i]), str(ra[i]), str(dec[i]), str(size), "0.396"]
       print command
       subprocess.call(command)
       subprocess.call(["rm", "-rf", pgc_dir])

  
  





