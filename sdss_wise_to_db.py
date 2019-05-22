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

def fits32(filename):
  
      if '.' not in filename:
	prefix=filename
	endfix='fits'
      else:
	prefix=filename.split('.')[0]
	endfix=filename.split('.')[1]
	if endfix == '': endfix='fits'


      filename = prefix+'.'+endfix


      hdulist = pyfits.open(filename)
      prihdr = hdulist[0].header

      #bscale =  prihdr['BSCALE'] 
      #bzero =   prihdr['BZERO']
      ## don't turn it on -- for general use (python bug)
      #print "checksum1: ", np.sum(hdulist[0].data)
      print "Current BITPIX: ", prihdr['bitpix']

      if prihdr['bitpix'] != -32:
	  prihdr['bitpix'] = -32
	  
	  # take a bakcup
	  cmd = 'cp ' + filename +'  '+ filename+'.back'
	  xcmd(cmd, True)
	
	  date = subprocess.check_output(["date"])
	  date = date[0:len(date)-1]
	  prihdr['history'] = 'File modified by \'ehsan\' with \"fits_bitpix32.py\"'
	  prihdr['history'] = 'on ' + date   
	  prihdr['history'] = 'email: <ehsan@ifa.hawaii.edu>' 
	  
	  #hdulist.flush()
	  if os.path.isfile('tmp.fits'):
	    xcmd('rm tmp.fits', True)

	  hdulist.writeto('tmp.fits')
	  
	  hdulist = pyfits.open('tmp.fits', mode='update')
	  prihdr = hdulist[0].header
	  prihdr['BSCALE'] = 1.
	  prihdr['BZERO'] = 0.
	  hdulist.flush() 
	  
	  ## don't turn it on -- for general use (python bug)
	  #print "checksum2: ", np.sum(hdulist[0].data)
	  cmd = 'mv tmp.fits ' + prefix+'.'+endfix
	  xcmd(cmd, True)


#################################

inFile = 'wise_photometry.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc  = table['PGC']
ra   = table['RAJ']   # deg
dec  = table['DEJ']   # deg


db_dir = "/home/ehsan/db_esn/data/"



for i in range(len(pgc)):
   
   pgc_dir = "pgc"+str(pgc[i])
   directory = "SDSS_ALL_Images/"+pgc_dir
   #isDirAvailable =  os.path.isdir(directory)
   
   if True:
     
     ra_id = str(int(np.floor(ra[i])))
     if ra[i] < 10:
       ra_id = '00'+ra_id+'D'
     elif ra[i] < 100:
       ra_id = '0'+ra_id+'D'
     else:
       ra_id = ra_id+'D'
     
     #print pgc[i], ra_id
     desitination = db_dir + ra_id + '/sdss/fits/'
     file_existence = 0
     
     for filters in ['u', 'g', 'r', 'i', 'z']:
        fname = directory+'/'+pgc_dir+'_'+filters+'.fits.gz'
        fname2 = '/home/ehsan/Dropbox/Home/PanStarrs/Jan/HI/SDSS+/'+pgc_dir+'_'+filters+'.fits.gz'
        #if os.path.exists(fname):
	   
	   #file_existence += 1
           #command = ["cp", fname, desitination]
           #subprocess.call(command)
           #subprocess.call(['gunzip', '-f', desitination+pgc_dir+'_'+filters+'.fits.gz'])
           #fits32(desitination+pgc_dir+'_'+filters+'.fits')
           
        if os.path.exists(fname2):
	   file_existence += 1
           command = ["cp", fname2, desitination]
           subprocess.call(command)
           subprocess.call(['gunzip', '-f', desitination+pgc_dir+'_'+filters+'.fits.gz'])
           fits32(desitination+pgc_dir+'_'+filters+'.fits')
	   
	   
     if file_existence > 0:
       cmd = "run_sex " + desitination+pgc_dir + ' ' + str(ra[i]) + ' ' + str(dec[i])
       xcmd(cmd, True)
     
     
     
     
  
