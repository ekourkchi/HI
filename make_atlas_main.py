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

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
 

def str_dec(dec):
  if dec < 0:
    sgn = '-'
  else: sgn = '+'
  
  zero = ''
  if dec < 10 and dec > -10: zero = '0'
  dec = np.abs(dec)
  
  return sgn+zero+str(np.int(dec))
  
  
def str_ra(ra):
 
  if ra < 10:
    zero = '00'
  elif ra < 100:
    zero = '0'
  else:
    zero = ''
  
  return zero+str(np.int(ra))


def ra_folder(ra):
  ra_id = str(int(np.floor(ra)))
  if ra < 10:
     ra_id = '00'+ra_id+'D'
  elif ra < 100:
     ra_id = '0'+ra_id+'D'
  else:
     ra_id = ra_id+'D'
  
  return ra_id




 
inFile = 'brent_list/edd_HI_ba_T_9060.short.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc         = table['PGC']
d25         = table['d25']   # arcmin
              
inFile = 'has_Hall.SDSS.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_ex      = table['pgc']
ra      = table['ra']
dec      = table['dec']


root = '/run/media/ehsan/ifa1_esn/atlas/ref/02a/'
filters = ['c', 'o']
db_dir = "/home/ehsan/db_esn/data/"





for i in range(len(pgc)):
 if i>3776: 
 
  R = 5.0 * d25[i]/60  # degree
  if R > 7: R = 7
  if R < 0.1: R = 0.1
  scale = 2./3600   # 2" / pixel
  
  ra_min = np.floor(ra[i] - R)
  ra_max = np.floor(ra[i] + R)
    
  dec_min = np.floor(dec[i] - R)
  dec_max = np.floor(dec[i] + R) 
    
    
  R_pix = str(np.int(np.ceil(R / scale)))
  r_str = str(ra[i])
  d_str = str(dec[i])
  scale = str(scale)
    
  #print pgc[i], ra_min, ra_max, dec_min, dec_max, d25[i]
    
  bin = 1 + max(ra_max-ra_min, dec_max-dec_min)
  print "pgc #:", pgc[i], R
  
  
  for filter in  filters:

    
    
    
    im_list = []
    
    r = ra_min
    p = 0
    while r <= ra_max:
      d = dec_min
      q = 0
      while d <= dec_max:
	filename = '02a'+str_ra(r)+'wp'+str_dec(d)+filter+'.fits'
	in_filder = 'dec'+str_dec(d)
	image = [root+filter+'/'+in_filder+'/'+filename, p, q]
	if os.path.exists(image[0]):
	    im_list.append(image)
	d += 1
	q += 1
      r += 1
      p += 1 
    
    
    desitination = db_dir + ra_folder(ra[i]) + '/atlas_big/fits/'
    out_File = desitination +'pgc' + str(np.int(pgc[i])) + '_02a_' + filter + '.fits'
    
    if len(im_list) != 0:
      
      string = ''
      string +=  'rd 1 ' + im_list[0][0] + ' cnpix silent' +'\n'
      string +=  'cop 2 1 bin=-'+str(np.int(bin)) +'\n'
      string +=  'mc 2 0' +'\n'
      
      for n in range(len(im_list)):
	string +=  'rd 1 ' + im_list[n][0] + ' cnpix silent' +'\n'
	p = im_list[n][1]
	q = im_list[n][2]
	string +=  'ai 2 1 dx=' + str(np.int(p*1800)) + '  dy=' + str(np.int(q*1800)) +'\n'
	
      string +=  'cop 3 2' +'\n'
      string +=  'map 3 xtpcd=(2, '+r_str+', '+d_str+', '+scale+')' +'\n'
      string +=  'cop 4 2' +'\n'
      string +=  'map 4 ytpcd=(2, '+r_str+', '+d_str+', '+scale+')' +'\n'
      
      string +=  'ac 3 '+R_pix +'\n'
      string +=  'ac 4 '+R_pix +'\n'
      string +=  'open 5 nx=2*'+R_pix+' ny=2*'+R_pix +'\n'
      string +=  'warp 5 2 3 4 old' +'\n'
      string +=  'wd 5 ' + out_File +'\n'
      string += 'Q\n'
      
      with open('tmp.monsta.pro', 'w') as file:    # '.pro' is necessary
	file.write(string)
	
      subprocess.call(['monsta', 'tmp.monsta.pro'])
      subprocess.call(['rm', 'tmp.monsta.pro'])
      
      hdulist = pyfits.open(out_File, mode='update')
      prihdr = hdulist[0].header   # Promary Header
      
      prihdr.append(('OBJ', 'pgc' + str(np.int(pgc[i])), 'Object Name'), end=True)
      prihdr.append(('CRPIX1', R_pix, 'Ref pix x'), end=True)
      prihdr.append(('CRPIX2', R_pix, 'Ref pix y'), end=True)
      prihdr.append(('CRVAL1', r_str, 'Ref val x'), end=True)
      prihdr.append(('CRVAL2', d_str, 'Ref val y'), end=True)
      prihdr.append(('CD1_1', scale, 'CD11'), end=True)
      prihdr.append(('CD1_2', '0.0', 'CD12'), end=True)
      prihdr.append(('CD2_1', '0.0', 'CD21'), end=True)
      prihdr.append(('CD2_2', scale, 'CD22'), end=True)
      prihdr.append(('CTYPE1', 'RA---TAN'), end=True)
      prihdr.append(('CTYPE2', 'DEC--TAN'), end=True)
      date = subprocess.check_output(["date"])
      date = date[0:len(date)-1]
      prihdr['history'] = 'HISTORY File modified by user \'ehsan\' with \"make_atlas_main.py\"'
      prihdr['history'] = 'on ' + date

      hdulist.flush() # changes are written back to original.fits

    
    

   
   
   
   










