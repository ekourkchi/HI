#!/usr/bin/python
import sys
import os.path
import subprocess
import glob

from time import time

import numpy as np
from math import *
from astrometry.util.starutil_numpy import * 
from astrometry.libkd import spherematch
import random 

import pyfits
#from pyfits import *
from numpy import radians, degrees, sin, cos, arctan2, hypot
#from k3match import *
from astropy.io import fits


##########################################

def read_glga(filename):
  
  pgc_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    pgc = columns[0]
    pgc_ID = pgc[3:len(pgc)]
    pgc_lst.append(int(pgc_ID))
  
  return pgc_lst 

##########################################

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

##########################################

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
#################################################################
def SDSS_db_avilability(pgc, ra, dec, Filters=['u', 'g', 'r', 'i', 'z'], db_dir='', toDbase=False):
   
   pgc_dir = "pgc"+str(pgc)
   
   ra_id = ra_db(ra)
   desitination = db_dir + ra_id + '/sdss/fits/'
   
   
   file_existence = 0
   
   if True:

    
     for filters in Filters:
         
        fname = "/home/ehsan/db_esn/SDSS_Additional/"+pgc_dir+'/'+pgc_dir+'_'+filters+'.fits.gz'
        
        if os.path.exists(fname):
	   
	   file_existence += 1
	   if toDbase:
	      command = ["cp", fname, desitination]
	      subprocess.call(command)
	      print command

           

   

   return file_existence


#################################################################

 
if __name__ == '__main__':


  inFile  = '../augment/EDD_distance_cf4_v08.csv'
  table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
  pgc     = table['pgc']
  ra      = table['ra']
  dec     = table['dec']  
  sdss    = table['sdss']  
  d25     = table['d25']
  b_a     = table['b_a']
  PA      = table['pa']
  Ty      = table['ty']  
  N = len(pgc)
  
  
  PGC = [56487,56705,56718,57194,1487317]
  
  
  db_dir = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/cf4_sdss/data/'
  print '# This is the glga qa file ....'
  
  if True:
      
     for j in range(len(PGC)):
        i = 0
        while i<N and pgc[i] != int(PGC[j]): i+=1   
        
        if SDSS_db_avilability(pgc[i], ra[i], dec[i], Filters=['g','r','i']) == 3:

           SDSS_db_avilability(pgc[i], ra[i], dec[i], db_dir=db_dir, toDbase=True)
        


  

    
   
  






     
  
