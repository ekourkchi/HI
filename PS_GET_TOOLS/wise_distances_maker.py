#!/usr/bin/python
import sys
import os
import os.path
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import pyfits
from fits_prep import *
import glob

#################################

def xcmd(cmd,verbose):

  if verbose: print '\n'+cmd

  tmp=os.popen(cmd)
  output=''
  for x in tmp: output+=x
  if 'abort' in output:
    failure=True
  else:
    failure=tmp.close()
  if False:
    print 'execution of %s failed' % cmd
    print 'error is as follows',output
    sys.exit()
  else:
    return output

#################################
######################################

#all.9060.csv
table = np.genfromtxt('all.9060.csv', delimiter=',', filling_values=None, names=True, dtype=None)
pgc     = table['PGC']
d25     = table['d25']   # arcmin
ra      = table['RA']
dec     = table['DEC']
sdss    = table['Has_SDSS']

count = 0
pgc_wise = []
d25_wise = []
ra_wise  = []
dec_wise = []

for i in range(len(pgc)):
  
  
  if d25[i]>2 and sdss[i]==1 : # or dec[i]<-25:
    pgc_wise.append(pgc[i])
    d25_wise.append(d25[i])
    ra_wise.append(ra[i])
    dec_wise.append(dec[i])
    count+=1
    
#myTable = Table()
#myTable.add_column(Column(data=pgc_wise,name='pgc', dtype=np.dtype(int)))
#myTable.add_column(Column(data=ra_wise,name='ra', format='%0.4f'))
#myTable.add_column(Column(data=dec_wise,name='dec', format='%0.4f'))
#myTable.add_column(Column(data=d25_wise,name='d25', format='%0.2f'))
#myTable.write('wise_distance_candidates.csv', format='ascii.fixed_width',delimiter=',', bookend=False)

print count   
    





















