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
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
 
######################################
def str_dec(dec):
  if dec < 0:
    sgn = '-'
  else: sgn = '+'
  
  zero = ''
  if dec < 10 and dec > -10: zero = '0'
  dec = np.abs(dec)
  
  return sgn+zero+str(np.int(dec))
  
######################################
def str_ra(ra):
 
  if ra < 10:
    zero = '00'
  elif ra < 100:
    zero = '0'
  else:
    zero = ''
  
  return zero+str(np.int(ra))

######################################
def ra_folder(ra):
  ra_id = str(int(np.floor(ra)))
  if ra < 10:
     ra_id = '00'+ra_id+'D'
  elif ra < 100:
     ra_id = '0'+ra_id+'D'
  else:
     ra_id = ra_id+'D'
  
  return ra_id

######################################
def ra_modify(ra):
  
  while ra>360.:
    ra-=360.
  while ra<0.:
    ra+=360.     
  
  return ra

######################################
def radec_list(ra, dec):
  
  ra_lst  = []
  dec_lst = []
  delta = 0.45
  
  ra_lst.append(ra) ; dec_lst.append(dec)
  ra_lst.append(ra) ; dec_lst.append(dec-delta)
  ra_lst.append(ra) ; dec_lst.append(dec+delta)
  ra_lst.append(ra_modify(ra-delta)) ; dec_lst.append(dec)
  ra_lst.append(ra_modify(ra+delta)) ; dec_lst.append(dec)
  ra_lst.append(ra_modify(ra-delta)) ; dec_lst.append(dec-delta)
  ra_lst.append(ra_modify(ra+delta)) ; dec_lst.append(dec+delta)
  ra_lst.append(ra_modify(ra-delta)) ; dec_lst.append(dec+delta)
  ra_lst.append(ra_modify(ra+delta)) ; dec_lst.append(dec-delta)
  
  return ra_lst, dec_lst

######################################
#################################
def removefix(filename, suffix):
  
  
  name_list = filename.split('.')
  N = len(name_list)
  if name_list[N-1] == suffix:
    
    name =''
    for i in range(N-2):
      name = name + name_list[i] + '.'
    name += name_list[N-2]

  return name

######################################
inFile = str(sys.argv[1])

pgc_in = sys.argv[1]


inFile = 'all.9060.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc     = table['PGC']
d25     = table['d25']   # arcmin
ra      = table['RA']
dec     = table['DEC']

available = False
for i in range(len(pgc)):
  if pgc[i] == int(pgc_in):
    pgc_no = pgc[i]
    ra_no  = ra[i]
    dec_no = dec[i]
    d25_no = d25[i]
    available = True
    break

if available:
  
  ra_lst, dec_lst = radec_list(ra_no, dec_no)
  filename = 'pgc'+pgc_in+'.query'
  if os.path.isfile(filename):
    xcmd('rm '+filename, True)
  with open(filename, 'w') as file:
    for i in range(len(ra_lst)):
       print ra_lst[i], dec_lst[i], 'a'
       file.write('{0} {1} {2}\n'.format(ra_lst[i], dec_lst[i], 'a'))

else:
  
  print 'Could not find pgc'+pgc_in+'  ... Try again !'
    
    
    

    

    

    

    
    

   
   
   
   










