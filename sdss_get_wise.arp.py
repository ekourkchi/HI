#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import time 


def find(pgc_list, p, q, pgc):
  
  if p>q: 
    return False
  r = (p+q)/2
  if pgc == pgc_list[r]:
    return True
  if pgc<pgc_list[r]:
    return find(pgc_list, p, r-1, pgc)
  if pgc>pgc_list[r]:
    return find(pgc_list, r+1, q, pgc)

  
###########################

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

inFile = 'wise_photometry.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc        = table['PGC']
ra         = table['RAJ']    # deg
dec        = table['DEJ']   # deg
a          = table['HA']     # arcmin

inFile = 'has_Hall.SDSS.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_ex      = table['pgc']
sdss        = table['SDSS']
all_indices = np.where(sdss == 1)
pgc_ex = pgc_ex[all_indices]

pgc_ex = pgc_ex[np.argsort(pgc_ex)]

n_ex = len(pgc_ex)

counter= 0
for i in range(len(pgc)):
  
  if not find(pgc_ex, 0, n_ex-1, pgc[i]):    ## pgc_ex must be sorted 
  
     pgc_dir = "pgc"+str(pgc[i])
     directory = "SDSS_ALL_Wise/"+pgc_dir
     isDirAvailable =  os.path.isdir(directory)
     
     if isDirAvailable:
       subprocess.check_output(["rm", "-rf" , directory])
     subprocess.check_output(["mkdir" , directory])
     
     size = (a[i]*5)/60.
     if size < 0.1:
       size = 0.1  # degree
     if size>3:
       size = max(3., (a[i]*3)/60.)
     
     with cd('/Users/ehsan/SDSS_db/SDSS_ALL_Wise'):
       
       
       command =  ["sdssall", "pgc"+str(pgc[i]), '{:.4f}'.format(ra[i]), '{:.4f}'.format(dec[i]), '{:.2f}'.format(size), "0.396"]
       print counter, command
       counter += 1 
       subprocess.call(command)
       time.sleep(60)
       #subprocess.call(["rm", "-rf", pgc_dir])

  
  





