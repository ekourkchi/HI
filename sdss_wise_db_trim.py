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
# Galaxy size in arcmin
def fits32_cut(filename, ra, dec, size):
  
      if '.' not in filename:
	prefix=filename
	endfix='fits'
      else:
	prefix=filename.split('.')[0]
	endfix=filename.split('.')[1]
	if endfix == '': endfix='fits'


      filename = prefix+'.'+endfix


      hdulist = pyfits.open(filename+'.back')
      prihdr = hdulist[0].header
      data = hdulist[0].data
      nx, ny =  np.shape(data)
      
      cmd =  '/home/ehsan/bin/sky2xy -j ' + filename+'.back' + ' ' + str(ra) + ' ' + str(dec)
      #print nx, ny
      outstring =  xcmd(cmd, False)
      
      print 'esn1:' , outstring
      
      outstring =  outstring.split('\n')[0]
      outstring = outstring.split(' ')
      
      print 'esn2:' , outstring
      
      
      m = len(outstring) - 1
      while(outstring[m] == ''): m-=1
      yc = np.float(outstring[m])
      
      m-=1
      while(outstring[m] == ''): m-=1
      xc = np.float(outstring[m])
      
      
      deltx = np.abs(np.float(prihdr['CDELT1']))
      delty = np.abs(np.float(prihdr['CDELT2']))
      print 'esn3:', xc, yc, deltx, delty
      
      
      x_max = min(nx, np.round(xc + 1.50*size/60./deltx))
      x_min = max(0, np.round(xc - 1.50*size/60./deltx))
      
      y_max = min(ny, np.round(yc + 1.50*size/60./delty))
      y_min = max(0, np.round(yc - 1.50*size/60./delty))     
      
      
      #print x_min, x_max, y_min, y_max
      data =  data[x_min:x_max,y_min:y_max]
      hdulist[0].data = data
      #print np.shape(data)
      nx_new = x_max - x_min
      ny_new = y_max - y_min
      
      #print nx_new, ny_new
      
      prihdr['NAXIS1'] = nx_new
      prihdr['NAXIS2'] = ny_new
      
      prihdr['CRPIX1'] = np.float(prihdr['CRPIX1']) - x_min
      prihdr['CRPIX2'] = np.float(prihdr['CRPIX2']) - y_min
      
      
      #print filename, prefix, endfix

      #print "Current BITPIX: ", prihdr['bitpix']

      if prihdr['bitpix'] != -32:
	  prihdr['bitpix'] = -32
	  
      
      if True:
	
	  date = subprocess.check_output(["date"])
	  date = date[0:len(date)-1]
	  prihdr['history'] = 'File modified by \'ehsan\' with \"sdss_wise_db_trim.py\"'
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
	  
          
          if os.path.isfile(filename):
	    xcmd('rm ' + filename, True)
	  cmd = 'mv tmp.fits ' + filename
	  xcmd(cmd, True)


#################################






inFile = 'wise_photometry.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc  = table['PGC']
ra   = table['RAJ']   # deg
dec  = table['DEJ']   # deg
maj  = table['MAJ']   # semi-major

db_dir = "/home/ehsan/db_esn/data/"



for i in range(1,len(pgc)):
   
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
        
        backup = desitination+pgc_dir+'_'+filters+'.fits'
        
        if os.path.exists(backup+'.back'):
	   file_existence += 1
           fits32_cut(backup, ra[i], dec[i] ,maj[i])
	   
	   
     if file_existence > 0:
       
       cmd =  'rm -rf ' + db_dir + ra_id + '/sdss/jpg/'+pgc_dir+'_*.jpg'
       xcmd(cmd, True)
	    
       cmd =  'rm -rf ' + db_dir + ra_id + '/aux/'+pgc_dir+'_ellipse.dat*'  
       xcmd(cmd, True)
	    
       cmd = "run_sex " + desitination+pgc_dir + ' ' + str(ra[i]) + ' ' + str(dec[i])
       xcmd(cmd, True)
     
     
     
     
  