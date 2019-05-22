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


table = np.genfromtxt( 'availability.txt' , delimiter=',', filling_values=None, names=True, dtype=None)
navail_pgc = table['pgc']
g1 = table['g']
r1 = table['r']
i1 = table['i']
gri = g1 + r1 + i1
navail_indices = np.where(gri != 3)
navail_indices = navail_indices[0]

print len(all_indices), len(navail_indices)

for i in all_indices:
 if i>5678:  
   pgc_dir = "pgc"+str(pgc[i])
   
   do = False
   for j in navail_indices:
     if navail_pgc[j] == pgc_dir+' ':
       do = True
       break
   if do:
     #directory = "SDSS_ALL_Images/"+pgc_dir
     #isDirAvailable =  os.path.isdir(directory)
     
     #if isDirAvailable:
	 
       #subprocess.check_output(["rm", "-rf" , directory])
     #subprocess.check_output(["mkdir" , directory])
     
     size = (d25[i]*5)/60.
     if size < 0.1:
       size = 0.1  # degree
     if size>3:
       size = max(3., (d25[i]*3)/60.)
     
     with cd('/Users/ehsan/SDSS_db/SDSS_ALL_Images2'):
       
       command =  ["sdssall", "pgc"+str(pgc[i]), '{:.4f}'.format(ra[i]), '{:.4f}'.format(dec[i]), '{:.2f}'.format(size), "0.396"]
       print command
       subprocess.call(command)
       ###subprocess.call(["rm", "-rf", pgc_dir])
       time.sleep(60)

  
  





