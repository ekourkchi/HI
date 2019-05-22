#!/usr/bin/python
import sys
import os.path
import subprocess
import glob
import numpy as np
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




inFile = 'has_Hall.SDSS.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc      = table['pgc']
ra      = table['ra']
dec      = table['dec']
sdss = table['SDSS']
hall = table['Hall2012']

all_indices = np.where(sdss == 1)
#all_indices = np.where(hall == 1)


all_indices = all_indices[0]


db_dir = "/home/ehsan/db_esn/data/"



for i in all_indices:
   
   pgc_dir = "pgc"+str(pgc[i])
   directory = "SDSS_ALL_Images/"+pgc_dir
   isDirAvailable =  os.path.isdir(directory)
   
   if isDirAvailable:
     
     ra_id = str(int(np.floor(ra[i])))
     if ra[i] < 10:
       ra_id = '00'+ra_id+'D'
     elif ra[i] < 100:
       ra_id = '0'+ra_id+'D'
     else:
       ra_id = ra_id+'D'
     
     desitination = db_dir + ra_id + '/sdss/fits/'
     file_existence = 0
     
     for filters in ['u', 'g', 'r', 'i', 'z']:
        fname = directory+'/'+pgc_dir+'_'+filters+'.fits.gz'
        if os.path.exists(fname):
	   file_existence += 1

           
     
     if file_existence > 0:
       cmd = "run_sex_background " + desitination+pgc_dir + ' ' + str(ra[i]) + ' ' + str(dec[i])
       xcmd(cmd, True)
     
     
     
     
  