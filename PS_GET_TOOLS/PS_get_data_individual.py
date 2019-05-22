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
from fits_prep import *
import glob

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
def radec_list(ra_min, ra_max, dec_min, dec_max, R):
  
  ra_lst  = []
  dec_lst = []
  
  if R<0.4:
    ra_lst.append(ra[i]) ; dec_lst.append(dec[i])
    ra_lst.append(ra[i]) ; dec_lst.append(dec[i]-0.4)
    ra_lst.append(ra[i]) ; dec_lst.append(dec[i]+0.4)
    ra_lst.append(ra[i]-0.4) ; dec_lst.append(dec[i])
    ra_lst.append(ra[i]+0.4) ; dec_lst.append(dec[i])

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
def file_info(fileID):
  
  suffix = ''
  if '.unconv.jpg' in fileID:
    suffix = '.unconv.jpg'
  if '.unconv.mk.fits' in fileID:
    suffix = '.unconv.mk.fits' 
  if '.unconv.fits' in fileID:
    suffix = '.unconv.fits'
  if '.unconv.wt.fits' in fileID:
    suffix = '.unconv.wt.fits'
    
  bands = ['g','r','i','z','y','w']
  filter = ''
  for band in bands:
    if '_'+band+'_' in  fileID:
      filter = band
      break
  
  i = 0
  while fileID[i]!='_':  
    i+=1
    j=i
    
  
  row_s = fileID[0:j]
  
  return int(row_s), filter, suffix
    
    
######################################
def download_pgc_band(URL_root, file_id, db_dir, pgc, band):
  
  pgc_root = db_dir # +'/pgc'+str(pgc)
  pgc_band_root = pgc_root+'/'+band
  URL_file = URL_root+'/'+file_id
  
  if not os.path.isdir(pgc_root):
    cmd = 'mkdir '+pgc_root
    xcmd(cmd, True)
  if not os.path.isdir(pgc_band_root):
    cmd = 'mkdir '+pgc_band_root  
    xcmd(cmd, True)

  with cd(pgc_band_root):
    xcmd('wget '+ URL_file, True)
######################################
######################################
def make_PS(db_dir, pgc, ra, dec, d25, coeff=5.):
  
  pgc_root = db_dir # +'/pgc'+str(pgc)
  
  
  for band in ['g','r','i', 'z']:
    
    pgc_band_root = pgc_root+'/'+band
    
    cmd = 'mkdir '+pgc_band_root+'/tmp'
    xcmd(cmd, True)
  
    cmd = 'mv '+pgc_band_root+'/*.unconv.fits '+pgc_band_root+'/tmp/.'
    xcmd(cmd, True)

    cmd = 'mv '+pgc_band_root+'/*.unconv.mk.fits '+pgc_band_root+'/tmp/.'
    xcmd(cmd, True)
    
    my_images =  glob.glob(pgc_band_root+'/tmp/*.unconv.fits')
    for i in range(len(my_images)):
      with cd(pgc_band_root):
        fits_prep(my_images[i], -32, edit_zp=True)
        
   
        
    xcmd('rm '+pgc_band_root+'/tmp/*.mk.fits', True)
    
    
###########################################################################
    with cd(pgc_band_root):
      fout=open('montage.csh','w')
      montage = '''
      rm *tbl
      rm -rf projected
      mkdir  projected
      mImgtbl tmp rimages.tbl
      mProjExec -p tmp rimages.tbl tmp.hdr projected stats.tbl
      mImgtbl projected pimages.tbl
      mAdd -p projected pimages.tbl tmp.hdr tmp.fits
      mConvert -b -32 tmp.fits tmp.fits
      rm *area*fits
      rm *tbl
      rm -rf projected
      '''
      fout.write(montage+'\n')
      fout.close()
      
      size = (d25*coeff)/60.
      if size < 0.1:
        size = 0.1  # degree
      if size>coeff:
        size = max(2., (d25*coeff)/60.)
      
      naxis = int(size*3600 / 0.250)
      crpix = naxis/2
      hdr = ''
      hdr += 'SIMPLE = T' + '\n'
      hdr += 'BITPIX = -32' + '\n'
      hdr += 'NAXIS = 2' + '\n'
      hdr += 'NAXIS1 = '+str(naxis) + '\n'
      hdr += 'NAXIS2 = '+str(naxis) + '\n'
      hdr += 'CTYPE1 = \'RA---TAN\'' + '\n'
      hdr += 'CTYPE2 = \'DEC--TAN\'' + '\n'
      hdr += 'CRVAL1 = ' +str(ra)+ '\n'
      hdr += 'CRVAL2 = ' +str(dec)+ '\n'
      hdr += 'CRPIX1 = '+str(crpix) + '\n'
      hdr += 'CRPIX2 = '+str(crpix) + '\n'
      hdr += 'CDELT1 = -6.94444444444444E-05' + '\n'
      hdr += 'CDELT2 = 6.94444444444444E-05' + '\n'
      hdr += 'CROTA2 = 0.000000' + '\n'
      hdr += 'EQUINOX = 2000.0' + '\n'
      hdr += 'BSCALE = 1' + '\n'
      hdr += 'BZERO = 0' + '\n'
      hdr += 'EXPTIME = 1.0' + '\n'
      hdr += 'ZP = 16.40006562 ' + '\n'
      hdr += 'OBJECT = ' + 'pgc'+str(pgc) + '\n'
      hdr += 'HISTORY = \'email: <ehsan@ifa.hawaii.edu>\'' + '\n'  
      hdr += 'HISTORY = \'by: PS_get_data.py\'' + '\n'  
      hdr += 'END' + '\n'

      fout=open('tmp.hdr','w')
      fout.write(hdr)
      fout.close()
      
      xcmd('csh montage.csh', True)
      xcmd('mv tmp.fits '+'../pgc'+str(pgc)+'_'+band+'.fits', True)
###########################################################################

      #xcmd('rm montage.csh', True)
      #xcmd('rm -rf tmp', True)
      
    #xcmd('rm -rf ' + pgc_band_root, True)
  
######################################
######################################
#URL_root = 'http://datastore.ipp.ifa.hawaii.edu/ifa-pstamp-results/all.9060.csv.151_300_603241'
db_dir = '/home/ehsan/db_esn/my_PS_db/'
##db_dir = '.'


pgc_in = sys.argv[1]
coeff = float(sys.argv[2])

inFile = 'pgc'+pgc_in
db_dir = db_dir+'/pgc'+pgc_in
if not os.path.isdir(db_dir):
  cmd = 'mkdir '+db_dir
  xcmd(cmd, True)


#all.9060.csv
table = np.genfromtxt('all.9060.csv', delimiter=',', filling_values=None, names=True, dtype=None)
pgc     = table['PGC']
d25     = table['d25']   # arcmin
ra      = table['RA']
dec     = table['DEC']

for i in range(len(pgc)):
  if pgc[i] == int(pgc_in):
    pgc_no = pgc[i]
    ra_no  = ra[i]
    dec_no = dec[i]
    d25_no = d25[i]
    break

#for j in range(3,len(sys.argv)): 
    #URL_root = str(sys.argv[j])+'/'
    #xcmd('wget '+URL_root+'/index.txt', True)
    #index_file = inFile+'.index.txt'
    #xcmd('mv index.txt '+index_file, True)
    #### index_file = 'index.txt'   # this what PSTARRS server provides
    #table = np.genfromtxt(index_file , delimiter='|', filling_values=None, names=True, dtype=None, skip_header=4)
    #fileID         = table['fileID']
    #xcmd('rm '+index_file, True)

    #for i in range(len(fileID)):

      #row_s, band, suffix =  file_info(fileID[i])
      #if band in ['g','r','i', 'z']:
	#download_pgc_band(URL_root, fileID[i], db_dir, pgc_no, band)
	#print pgc_no, band, fileID[i]
    
## Making postage stampe image - Last set
#make_PS(db_dir, pgc_no, ra_no, dec_no, d25_no, coeff=coeff)

print pgc_no,   ra_no, dec_no, d25_no
  








