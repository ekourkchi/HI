#!/usr/bin/python
import sys
import os.path
import subprocess
import glob
import numpy as np
from astropy.table import Table, Column 
import pyfits
import pylab as py
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter



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
def read_file(fname, n_skip = 1, seprator = ','):
  
                # how columns are seprated
  
  list_name = []
  list_ra   = []
  list_dec  = []
  list_a    = []
  list_b    = []
  list_pa   = []
  list_ty   = []
  
  line_no = 0
  for line in open(fname, 'r+'):
    
    columns = line.split(seprator)
    
    line_no+=1
    if len(columns) >= 2:
        
        if line_no>n_skip: 
	  
	  n = 0
	  i = 0
	  while n < len(columns):
	    
	    if columns[n] != '' and i==0:
	       list_name.append(columns[n])
	       i+=1
	       n+=1
	       continue
	    
	    if columns[n] != '' and i==1:
	       list_ra.append(float(columns[n]))
	       i+=1
	       n+=1
	       continue       
	    if columns[n] != '' and i==2:
	       list_dec.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue
	    if columns[n] != '' and i==3:
	       list_a.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==4:
	       list_b.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==5:
	       list_pa.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==6:
	       type = columns[n]
	       type = type[0:len(type)-1]
	       list_ty.append(type)
	       i+=1
	       n+=1
	       continue	     	     
	    n+=1

  
  list_name = np.asarray(list_name)
  list_ra   = np.asarray(list_ra)
  list_dec  = np.asarray(list_dec)
  list_a    = np.asarray(list_a)
  list_b    = np.asarray(list_b)
  list_pa   = np.asarray(list_pa)
  list_ty   = np.asarray(list_ty)
  
  return list_name, list_ra, list_dec, list_a, list_b, list_pa, list_ty
#################################################################

inFile = 'New_era/pan_starrs_calib.glga'

pgc, ra, dec, a_cal, b_cal, pa_cal, ty_cal = read_file(inFile, n_skip = 2, seprator = ' ')



temp = np.chararray(len(pgc))

N = len(pgc)
db_root = '/home/ehsan/db_esn/data/'

mags = np.zeros([N, 5])

no = 0
for i in range(N):
  
  db_id = ra_db(ra[i])
  pgc_id = pgc[i]
  
  
  
  filters = ['g','r','i','z']
  
  for p in range(4):
    
    filter = filters[p]
    photometry =  db_root+db_id+'/photometry/'+pgc_id+'_'+filter+'_asymptotic.dat'
    if os.path.exists(photometry):
      with open(photometry) as f:
	counter = 1
	for line in f:
	  if counter == 14:
	    line_split = line.split(" ")
	    not_void = 0 
	    for thing in line_split:
	      if thing != '': not_void+=1
	      if not_void==2: 
		break
	    mags[i][p] = np.float(thing)
	  counter+=1
    else: mags[i][p] = 0
      
  if True :
    
     no+=1
     
     s = '|| ' + str(no) + ' || ' + pgc_id
     for p  in range(4):
       if mags[i][p] != 0 :
         s += " || " + str(mags[i][p])
       else: s += " || " + ' '
     
     s += " || [http://www.ifa.hawaii.edu/~ehsan/test/" + pgc_id
     s += "_panstarrs_profile.jpg profile]  ||  [http://www.ifa.hawaii.edu/~ehsan/test/" + pgc_id
     s += "_panstarrs_images.jpg images]  || "

     
     #print s
     
     
     
     m = len(pgc_id)
     if float(pgc_id[6:m]) in [93031,23567,142820,42081,40692,41608,46427,40516,36825,5132,4596,71501,70927,44795,36825,410692]: 
       for filter in filters:
         fitsFile =  db_root+db_id+'/panstarrs/fits/'+pgc_id+'_'+filter+'.fits'
         if os.path.exists(fitsFile):
            #print fitsFile
            command = ["cp", fitsFile, '/home/ehsan/PanStarrs/Jan/HI/tarbal/']
            subprocess.call(command)
            
            
     
     
     
       fname1 = db_root+db_id+'/plots/'+pgc_id+'_panstarrs_images.jpg'
       command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/tarbal/']
       subprocess.call(command)
       fname1 = db_root+db_id+'/plots/'+pgc_id+'_panstarrs_profile.jpg'
       command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/tarbal/']
       subprocess.call(command)
  
  
 