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
pgc_brent         = table['PGC']

inFile = 'augment/a70_Tge1_ige60_Wge70_SNgt5.9832_has_SDSS.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']
sdss    = table['SDSS']


inFile = 'augment/a70_Tge1_ige60_Wge70_SNgt5.9832.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
lgd25     = table['lgd25']
d25 = 0.1*(10**lgd25)

N = 0 
for i in range(len(pgc)):
    
   if not pgc[i] in pgc_brent and sdss[i] == 1:
           
           N+=1
           pgc_dir = "pgc"+str(pgc[i])
           
           if True:
             directory = "/home/ehsan/db_esn/Alfalfa70_SDSS/"+pgc_dir
             isDirAvailable =  os.path.isdir(directory)
             
             #if isDirAvailable:
               #subprocess.check_output(["rm", "-rf" , directory])

             subprocess.check_output(["mkdir" , directory])
             
             size = (d25[i]*7)/60.
             if size < 0.1:
               size = 0.1  # degree
             if size>3:
               size = max(3., (d25[i]*5)/60.)
             
             with cd(directory):
               
               command =  ["sdssall", "pgc"+str(pgc[i]), '{:.4f}'.format(ra[i]), '{:.4f}'.format(dec[i]), '{:.2f}'.format(size), "0.396"]
               #print command
               subprocess.call(command)
               subprocess.call(["rm", "-rf", pgc_dir])
               time.sleep(60)

  
print "All Alfalfa 70% with SDSS: ", N    # 7514





