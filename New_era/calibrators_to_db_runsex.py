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

def angleto3Dradius(angle, isDegree=True):
  
  if isDegree:
    angle = angle*pi/180.
  
  
  return sqrt((sin(angle))**2 + (1-cos(angle))**2)

#################################################################
##########################################
if __name__ == '__main__':

  inFile = 'has_Hall.SDSS.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
  pgc     = table['pgc']
  ra      = table['ra']
  dec     = table['dec']
  sdss    = table['SDSS']
  hall    = table['Hall2012']
  
  inFile = 'edd_HI_ba_T_9060.short.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
  d25     = table['d25']
  
  
  name_cal, ra_cal, dec_cal, a_cal, b_cal, pa_cal, ty_cal = read_file('sample_tfc_all.glga', n_skip = 4, seprator = ' ')
  #print name_cal
  #print ra_cal
  #print dec_cal


  # Python equivalent of matchlength
  radius_in_deg = 1./60.  # 1 arcmin match
  (m1, m2, d)  = spherematch.match_radec(ra_cal, dec_cal, ra, dec, radius_in_deg, notself=False, nearest=True)

  print len(m1)
  
  #for m in range(len(m1)):
    
    #i = m1[m]
    #j = m2[m]
    #if d[m]*3600>=30.:
      #print name_cal[i], ra_cal[i], dec_cal[i], pgc[j], ra[j], dec[j], d[m]*3600


  


  db_dir = "/home/ehsan/db_esn/data/"


  count = 0
  for m in range(len(m1)):
    
    i = m1[m]
    j = m2[m]
    
    pgc_dir = "pgc"+str(pgc[j])
    directory = "/run/media/ehsan/ifa2_esn/my_PS_db/PS_pool/"+pgc_dir
    isDirAvailable =  os.path.isdir(directory)
    
    #if not isDirAvailable and dec[j]>-30:
      #print name_cal[i], pgc[j], isDirAvailable, dec[j], j+1, d25[j]
    
    if isDirAvailable : #and d25[j]<=2:
      count+=1
      #print 'PS_pgc'+str(pgc[j]), ra_cal[i], dec_cal[i], a_cal[i], b_cal[i], pa_cal[i], ty_cal[i]
      
      s = 'pgc'+str(pgc[j])
      s = s + ', ' + str(ra_cal[i])
      s = s + ', ' + str(dec_cal[i])
      s = s + ', ' + str(a_cal[i])
      s = s + ', ' + str(b_cal[i])
      s = s + ', ' + str(pa_cal[i])
      print s

      #ra_id = str(int(np.floor(ra[j])))
      #if ra[j] < 10:
	#ra_id = '00'+ra_id+'D'
      #elif ra[j] < 100:
	#ra_id = '0'+ra_id+'D'
      #else:
	#ra_id = ra_id+'D'
      
      #desitination = db_dir + ra_id + '/panstarrs/fits/'
      #file_existence = 0
      
      #for filters in ['g', 'r', 'i', 'z']:
	  #fname = directory+'/'+pgc_dir+'_'+filters+'.fits'
	  #destin_fname = desitination+'PS_'+pgc_dir+'_'+filters+'.fits'
	  #if os.path.exists(fname):
	    #print fname, destin_fname
	    #cmd = "cp "+fname+" "+destin_fname
	    #xcmd(cmd, True)
	    #file_existence+=1

           
     
      #if file_existence > 0:
        #cmd = "run_sex_pstarrs " + desitination+'PS_'+pgc_dir + ' ' + str(ra[j]) + ' ' + str(dec[j])
        #xcmd(cmd, True)
  
  print count  
     
     
     
  