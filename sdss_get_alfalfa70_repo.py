#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import pyfits

import sqlcl

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
###########################

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
###############################
def getSDSSfields(ra, dec, size):  # all in degree
  
  
  delta = 0.6*size+0.2
  
  #if size > 1:
      #delta = 1.2*size+0.4
  
  ra_max  =  ra+2*delta
  ra_min  =  ra-2*delta
  dec_max =  dec+delta
  dec_min =  dec-delta
  
  querry = """
  
 SELECT
 fieldID,
 run, 
 camCol, 
 field,
 ra, 
 dec,
 run,
 rerun 
 FROM Field   
  """
  
  querry += "WHERE ra BETWEEN "+str(ra_min)+" and "+str(ra_max)+" and dec BETWEEN "+str(dec_min)+" and "+str(dec_max)
  
  lines = sqlcl.query(querry).readlines()
  N = len(lines)

  
  field_lst = []
  for i in np.arange(2,N):
      line = lines[i]
      line = line.split(',')
      run    = line[1]
      camcol = line[2]
      field  = line[3]
      ra_    = line[4]
      dec_   = line[5]
      field_lst.append([run, camcol, field])
  
  
  return field_lst

###############################
## fieldInfo = [run, camcol, field]
## band = 'u', 'g', 'r', 'i', 'z'
## folde: <where to store files>
def getSDSSfiles(fieldInfo, band, folder):   
  
  run    = fieldInfo[0]
  camcol = fieldInfo[1]
  field  = fieldInfo[2]
  
  fileName = 'frame-'+band + '-''{0:06d}'.format(int(run))+'-'+camcol+'-'+'{0:04d}'.format(int(field))+'.fits.bz2'
  filename = 'frame-'+band + '-''{0:06d}'.format(int(run))+'-'+camcol+'-'+'{0:04d}'.format(int(field))+'.fits'
  http = 'https://dr12.sdss.org/sas/dr12/boss/photoObj/frames/301/'
  
  http += run + '/'
  http += camcol + '/'
  http += fileName
  
  with cd(folder):
    xcmd("wget " + http, True)
    xcmd("bzip2 -d " + fileName, True)
    fits_prep(filename, edit_zp=True)

################################################################# 

#################################
def removefix(filename):
  
  
  name_list = filename.split('.')
  N = len(name_list)
  if name_list[N-1] == 'fits':
    
    name =''
    for i in range(N-2):
      name = name + name_list[i] + '.'
    name += name_list[N-2]

  return name
#################################  

def fits_prep(filename, edit_zp=True):
  
  name = removefix(filename)
  xcmd("cp " + filename + ' ' + name+'.tmp.fits', True) 
  
  hdulist = pyfits.open(filename)
  prihdr = hdulist[1].header    
      
  if edit_zp:
     
     hdulist = pyfits.open(name+'.tmp.fits', mode='update')
     prihdr = hdulist[0].header
     prihdr['BSCALE'] = 1.
     prihdr['BZERO'] = 0.

     expTime = float(prihdr['EXPTIME'])
     nMgy = float(prihdr['NMGY'])

     new_zp = 16.40006562  # mJy / pix
     
     
     ### https://data.sdss.org/datamodel/files/BOSS_PHOTOOBJ/frames/RERUN/RUN/CAMCOL/frame.html
     ### http://www.sdss.org/dr12/imaging/images/
     zeroPoint = 22.5
     alpha = 10**(-0.4*(zeroPoint-new_zp))
     
     #hdulist[0].data = data = hdulist[0].data * (3631E-6 )
     hdulist[0].data = data = hdulist[0].data * (alpha )

     prihdr['EXPTIME'] = 1.0
     prihdr['ZP'] = new_zp

     hdulist.flush() 

     cmd = 'mv '+name+'.tmp.fits ' + filename
     xcmd(cmd, True)    
     
######################################
def make_sdss(pgc, ra, dec, size, band):
    
    pgc_band_root ='.'
    cmd = 'mkdir '+pgc_band_root+'/tmp'
    xcmd(cmd, True)
    
    cmd = 'mv '+pgc_band_root+'/frame-'+band+'*.fits '+pgc_band_root+'/tmp/.'
    xcmd(cmd, True)
    
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
      
      if size > 1.1:
          size = 1.1
      
      naxis = int(size*3600 / 0.396)
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
      hdr += 'CDELT1 = -1.1E-04' + '\n'
      hdr += 'CDELT2 = 1.1E-04' + '\n'
      hdr += 'CROTA2 = 0.000000' + '\n'
      hdr += 'EQUINOX = 2000.0' + '\n'
      hdr += 'BSCALE = 1' + '\n'
      hdr += 'BZERO = 0' + '\n'
      hdr += 'EXPTIME = 1.0' + '\n'
      hdr += 'ZP = 16.40006562 ' + '\n'
      hdr += 'OBJECT = ' + 'pgc'+str(pgc) + '\n'
      hdr += 'HISTORY = \'email: <ehsan@ifa.hawaii.edu>\'' + '\n'  
      hdr += 'HISTORY = \'by: esnsdssget.py\'' + '\n'  
      hdr += 'END' + '\n'

      fout=open('tmp.hdr','w')
      fout.write(hdr)
      fout.close()
      
      xcmd('csh montage.csh', True)
      xcmd('mv tmp.fits '+'pgc'+str(pgc)+'_'+band+'.fits', True)
      xcmd('rm montage.csh', True)
      xcmd('rm tmp.hdr', True)
      xcmd('rm -rf tmp', True)
      
###########################################################################        
def get_sdss(pgc, ra, dec, size, repository): 
    
    
  fields = getSDSSfields(ra, dec, size)
  
  folder = repository+'tmp'
  if os.path.isdir(folder):
      xcmd('rm -rf '+folder, True)
  xcmd('mkdir '+folder, True)
  
  if not os.path.isdir(repository+'pgc'+str(pgc)):
      xcmd('mkdir '+repository+'pgc'+str(pgc), True)
  
  for band in ['u','g','r','i','z']:
      
      for i in range(len(fields)):
        print ' '  
        print ' # '+str(i+1)+'/'+str(len(fields))+'  ... obj: '+'pgc'+str(pgc)+'  band: '+band
        
        getSDSSfiles(fields[i], band, folder)
      
      with cd(folder):
        make_sdss(pgc, ra, dec, size, band)       
      
      xcmd('mv '+folder+'/*fits '+repository+'pgc'+str(pgc), True)
      xcmd('gzip '+repository+'pgc'+str(pgc)+'/*fits ', True)

  xcmd('rm -rf '+folder, True)
################################################################# 
def find(pgc_list, p, q, pgc):
  
  if p>q: 
    return False
  r = (p+q)/2
  if pgc == pgc_list[r]:
    return True
  if pgc<pgc_list[r]:
    return find(pgc_list, p, r-1, pgc)
  if pgc>pgc_list[r]:
    return find(pgc_list, r+1, q, pgc)

  
###########################
if __name__ == '__main__':
   
  repository = '/home/ehsan/db_esn/Alfalfa70_SDSS_REPO/'  

  inFile = 'brent_list/edd_HI_ba_T_9060.short.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
  pgc_brent         = table['PGC']

  inFile = 'augment/a70_Tge1_ige60_Wge70_SNgt5.9832_has_SDSS.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
  pgc     = table['pgc']
  ra      = table['ra']
  dec     = table['dec']
  sdss    = table['SDSS']

  inFile = 'augment/a70_Tge1_ige60_Wge70_SNgt5.9832.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
  lgd25     = table['lgd25']
  
  N = len(pgc)
  j = 0
  # pgc1262971  was the galaxy when the crash happened
  while pgc[j] != 1262971 and j<N: j+=1
  
  for i in range(j,N):
     
    if lgd25[i]!=0 and lgd25[i]<3:
     
      d25 = 0.1*(10**lgd25[i])
      size = (d25*3.)/60.
      if size < 0.1:
        size = 0.1  # degree
      if size>1.1:
        size = 1.1
        
      get_sdss(pgc[i], ra[i], dec[i], size, repository)


    
  








