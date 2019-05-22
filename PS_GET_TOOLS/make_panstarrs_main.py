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
def radec_list(ra_min, ra_max, dec_min, dec_max, R):
  
  ra_lst  = []
  dec_lst = []
  
  if R<0.4:
    ra_lst.append(ra[i]) ; dec_lst.append(dec[i])
    ra_lst.append(ra[i]) ; dec_lst.append(dec[i]-0.4)
    ra_lst.append(ra[i]) ; dec_lst.append(dec[i]+0.4)
    ra_lst.append(ra_modify(ra[i]-0.4)) ; dec_lst.append(dec[i])
    ra_lst.append(ra_modify(ra[i]+0.4)) ; dec_lst.append(dec[i])

  else :

    r = ra_min
    p = 0
    while r <= ra_max:
      d = dec_min
      q = 0
      while d <= dec_max:
	ra_lst.append(r) ; dec_lst.append(d)
	d += 0.4
	q += 0.4
      r += 0.4
      p += 0.4
      
  
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
inFile  = '../augment/EDD_distance_cf4_v25.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  
sdss    = table['sdss']  
d25     = table['d25']
b_a     = table['b_a']
PA      = table['pa']
Ty      = table['ty']  


#inFile = str(sys.argv[1])
#action = str(sys.argv[2])

#row_min = int(sys.argv[3])
#row_max = int(sys.argv[4])

inFile = '../augment/new_gals.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
id_    = table['PGC']

action = 'catal'


if action=='catal':
  print 'row pgc row_s ra dec'

row_no = 0
gal_counter = 0 
for i in range(len(pgc)): #range(row_min-1, row_max):


  if pgc[i] in id_ and dec[i]>-30. and not pgc[i] in [2557] and d25[i]<10:
    
    R = 5. * d25[i]/60  # degree !!!!!
    if R > 7: R = 7
    if R < 0.1: R = 0.1
    scale = 0.25/3600   # 0.25" / pixel
    
    ra_min = ra_modify(np.floor(ra[i] - R)-0.4)
    ra_max = ra_modify(np.floor(ra[i] + R)+0.4)
      
    dec_min = np.floor(dec[i] - R)-0.4
    dec_max = np.floor(dec[i] + R)+0.4
    
    ra_lst, dec_lst = radec_list(ra_min, ra_max, dec_min, dec_max, R)
    gal_counter += 1 
    
    
    for j in range(len(ra_lst)):
      row_no += 1
      
      if action=='catal': 
	     print i+1, pgc[i], row_no, ra_lst[j], dec_lst[j]
      elif action=='query':
	     print ra_lst[j], dec_lst[j], 'a'
    
#print "No. of galaxies: ", gal_counter
    

    

    

    
    

   
   
   
   










