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
######################################
def make_small_PS(db_dir_sdss, pgc, ra, dec, d25, angle):
  
  pgc_root = db_dir_sdss
  
  
  for band in ['g','r','i']:
    
    pgc_band_root = pgc_root
    
    #fileout =  pgc_band_root+'/pgc'+str(pgc)+'_d25x2_rot_'+band+'.fits'
    #if os.path.exists(fileout):
      #continue
      
    
    
    cmd = 'mkdir '+pgc_band_root+'/tmp'
    xcmd(cmd, True)
  
    cmd = 'cp '+pgc_band_root+'/pgc'+str(pgc)+'_'+band+'.fits.gz '+pgc_band_root+'/tmp/.'
    xcmd(cmd, True)
    
    cmd = 'gunzip '+pgc_band_root+'/tmp/pgc'+str(pgc)+'_'+band+'.fits.gz'
    xcmd(cmd, True)
    
    file = pgc_band_root+'/tmp/pgc'+str(pgc)+'_'+band+'.fits'
    cmd = 'mRotate -r '+str(angle)+' '+file+' '+file
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
      
      if np.isnan(d25):
          d25 = 2.
      
      size = (d25*2)/60.
      if size < 0.1:
        size = 0.1  # degree
      if size>3:
        size = 3.
      
      
      
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
      
      size = (d25*3)/60.
      if size < 0.1:
        size = 0.1  # degree
      if size>3:
        size = 3.
      file = 'tmp.fits'
      cmd = 'mRotate -r '+str(angle)+' '+file+' '+file+' '+str(ra)+' '+str(dec)+' '+str(size)
      xcmd(cmd, True)
      
      
      xcmd('mv tmp.fits '+'pgc'+str(pgc)+'_d25x2_rot_'+band+'.fits', True)
      
      
      #size = (d25*2)/60.
      #naxis2 = int(size*3600 / 0.250)
      #x_min = crpix - naxis2/2
      #x_max = crpix + naxis2/2
      #y_min = crpix - naxis2/2
      #y_max = crpix + naxis2/2
      
      #output = 'pgc'+str(pgc)+'_d25x2_rot_'+band+'.fits'
      #input  = 'tmp.fits'
      #xstring = 'imcopy '+input+'"['+str(x_min)+':"'+str(x_max)+'",'+str(y_min)+':"'+str(y_max)+'"]" '+output
      #xcmd(xstring, True)
      

      xcmd('rm -rf tmp*', True)  
      xcmd('rm -rf montage.csh', True) 
      
      
###########################################################################    
      
### Example: python make_png.py hall_list_ps.csv
##################################################

inFile  = 'EDD_distance_cf4_v16.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  
sdss    = table['sdss']  
d25     = table['d25']
b_a     = table['b_a']
PA      = table['pa']
Ty      = table['ty']  
QA_wise = table['QA_wise']  
inc     = table['inc'] 
inc_flag = table['inc_flg'] 
##################################################
inFile = 'TFcalibrators.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_TFcalibrators    = table['PGC']
##################################################
inFile = 'TFcalibrators_Arecibo.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_TF_arecibo    = table['PGC']
RADE_TF_arecibo   = table['RADE']
TY_TF_arecibo     = table['T']
logr25_TF_arecibo = table['logr25']
Glon_TF_arecibo = table['Glon']
Glat_TF_arecibo = table['Glat']
SGL_TF_arecibo = table['SGL']
SGB_TF_arecibo = table['SGB']
b_a_TF_arecibo = 1./(10**logr25_TF_arecibo)
######################################





p = 0 
db_dir_sdss = '/home/ehsan/db_esn/cf4_sdss/'
db_dir_wise = '/home/ehsan/db_esn/cf4_wise/'
destination = '/home/ehsan/PanStarrs/INConline/galpool/'
path = '/home/ehsan/db_esn/cf4_sdss/SDSS_PNG_rotate/'

path1 = '/home/ehsan/db_esn/curtis/PNG_rotate/'
path2 = '/home/ehsan/PanStarrs/INClinationCode/PNG_rotate/'
path3 = '/home/ehsan/db_esn/my_PS_db/PNG_rotate/'
path5 = '/home/ehsan/db_esn/curtis/DSS/DSS_PNG_rotate/'
path6 = '/home/ehsan/db_esn/DSS/DSS_PNG_rotate/'

paths = [path]
paths_ = [path1, path2, path3, path5, path6]

for i in range(0, len(pgc)):
    
  #if not pgc[i] in pgc_TFcalibrators and not pgc[i] in pgc_TF_arecibo:
  
       hasSDSS_gri = False
       hasElse = False
       fileRoot = 'pgc'+str(pgc[i])+'_d25x2_rot'
       for sfx in ['_g.png','_r.png','_i.png','_gri.jpg','_g.back.png','_r.back.png','_i.back.png','_gri.back.jpg']:
       #for sfx in ['_gri.jpg']:    
           for path in paths:
               
               File = path + fileRoot + sfx

               if os.path.isfile(File):
                   
                   #cmd = 'cp '+File+' '+destination+'/.'  ### +fileRoot+'_gri.sdss.jpg'
                   #xcmd(cmd, True)
                   if sfx=='_gri.jpg': hasSDSS_gri=True
                   if sfx!='_gri.jpg': hasElse=True
                   
       if hasSDSS_gri and not hasElse:
           
           for path__ in paths_:
               File_ = path__ + fileRoot + '_gri.jpg'
               if os.path.isfile(File_):
                   cmd = 'cp '+File_+' '+destination+'/.'  ### +fileRoot+'_gri.sdss.jpg'
                   xcmd(cmd, True)
                   break
           
           
           print pgc[i]
           p+=1


print p    

    

    
    

   
   
   
   










