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

def get_ellipse(filename):
          
          ra_cen = -1
          dec_cen = -1
          semimajor = -1
          semiminor = -1
          PA = -1
          with open(filename) as f:
            counter = 1
            for line in f:
              if counter == 14:
                line_split = line.split(" ")
                not_void = 0 
                set_param = False
                for thing in line_split:
                  if thing != '': 
                      not_void+=1
                      set_param = True
                  if not_void==1 and set_param: 
                      set_param = False
                      ra_cen=np.float(thing) 
                  if not_void==2 and set_param: 
                      dec_cen=np.float(thing) 
                      set_param = False
                  if not_void==3 and set_param: 
                      semimajor=np.float(thing) 
                      set_param = False
                  if not_void==4 and set_param: 
                      semiminor=np.float(thing)
                      set_param = False
                  if not_void==5 and set_param: 
                      PA=np.float(thing) 
                      break
                return ra_cen, dec_cen, semimajor, semiminor, PA
              counter+=1   
#################################
def ra_db(ra):   # returns a string
  
     ra_id = str(int(np.floor(ra)))
     if ra < 10:
       ra_id = '00'+ra_id+'D'
     elif ra < 100:
       ra_id = '0'+ra_id+'D'
     else:
       ra_id = ra_id+'D'
  
     return ra_id
#################################
######################################
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

######################################


inFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_ehsan_calib.lst.output'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_ehsan    = table['pgc']
inc_ehsan    = table['inc']
flag_ehsan   = table['flag']


inFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_amber_calib.lst.output'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_amber    = table['pgc']
inc_amber    = table['inc']
flag_amber   = table['flag']


inFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_brent_calib.lst.output'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_brent    = table['pgc']
inc_brent    = table['inc']
flag_brent   = table['flag']


pgc_common = []
my_inc     = []
th_inc     = []  # brent

for i in range(len(pgc_brent)):
    
    if pgc_brent[i] in pgc_ehsan:
        
        i_lst = np.where(pgc_ehsan == pgc_brent[i])
        if flag_ehsan[i_lst][0]==0 and flag_brent[i]==0:
            if abs(inc_ehsan[i_lst][0]-inc_brent[i]) < 3 and inc_brent[i]<90 and inc_ehsan[i_lst][0]<90:
                my_inc.append(inc_ehsan[i_lst][0])
                pgc_common.append(pgc_brent[i])
                th_inc.append(inc_brent[i])


for i in range(len(pgc_common)):
    
    if pgc_common[i] in pgc_amber:
        i_lst = np.where(pgc_amber == pgc_common[i])
        
        if flag_amber[i_lst][0]==0:
            if abs(inc_amber[i_lst][0]-th_inc[i]) < 3 and inc_amber[i_lst][0]<90:
                brent = th_inc[i]
                ehsan = my_inc[i]
                amber = inc_amber[i_lst][0]
                print pgc_common[i], brent, ehsan, amber, np.median([brent, ehsan, amber]), np.std([brent, ehsan, amber])


