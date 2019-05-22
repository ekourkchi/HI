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
def make_small_PS(db_dir, pgc, ra, dec, d25, angle):
  
  pgc_root = db_dir
  
  
  for band in ['g','r','i']:
    
    pgc_band_root = pgc_root
    
    #fileout =  pgc_band_root+'/pgc'+str(pgc)+'_d25x2_rot_'+band+'.fits'
    #if os.path.exists(fileout):
      #continue
      
    
    
    cmd = 'mkdir '+pgc_band_root+'/tmp'
    xcmd(cmd, True)
  
    cmd = 'cp '+pgc_band_root+'/pgc'+str(pgc)+'_'+band+'.fits '+pgc_band_root+'/tmp/.'
    xcmd(cmd, True)
    
    #cmd = 'gunzip '+pgc_band_root+'/tmp/pgc'+str(pgc)+'_'+band+'.fits.gz'
    #xcmd(cmd, True)
    
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

      
      size = (d25*7)/60.
      #if size < 0.1:
        #size = 0.1  # degree
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
      
      xcmd('tcsh montage.csh', True)
      
      size = (d25*3.)/60.
      #if size < 0.1:
        #size = 0.1  # degree
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


inFile  = 'EDD_distance_cf4_v25.csv'
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
##################################################
inFile = 'new_gals.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
id_lexi    = table['PGC']


db_dir = '/home/ehsan/db_esn/cf4_sdss/'



if not os.path.isdir(db_dir):
  print db_dir+' does not exist ... !'
  sys.exit()

if not os.path.isdir(db_dir+'/SDSS_PNG_rotate_finale'):
   xcmd('mkdir '+db_dir+'/SDSS_PNG_rotate_finale', True)



p = 0 
for i in range(0, len(pgc)):

  if pgc[i] in id_lexi and sdss[i]==1:
    
  
    dataDir = db_dir+'/data/'+ra_db(ra[i])+'/sdss/fits/'
    ellipsefile = db_dir+'/data/'+ra_db(ra[i])+'/photometry/'+'/pgc'+str(pgc[i])+'_i_ellipsepar.dat'
    
    if sdss[i] == 0: # or not os.path.isfile(ellipsefile):
      continue
    
    if os.path.isfile(ellipsefile):
        ra_cen, dec_cen, semimajor, semiminor, PA_gal = get_ellipse(ellipsefile)
        d25[i] = 1.2*semimajor/60.
    else:
        PA_gal=PA[i]
        ra_cen  = ra[i] 
        dec_cen = dec[i]
        
    if True:
       xcmd('cp -rf '+dataDir+'/pgc'+str(pgc[i])+'_*.fits '+db_dir+'/.', True)
       xcmd('cp -rf '+dataDir+'/pgc'+str(pgc[i])+'_*.fits.gz '+db_dir+'/.', True)
       xcmd('gunzip '+db_dir+'/pgc'+str(pgc[i])+'_*.fits.gz ', True)
       p+=1
       

       print "===================================================="
       print i, pgc[i], ra[i], dec[i], d25[i], 90.-PA_gal
       #print semimajor, semiminor, ellipsefile
       print "===================================================="
       make_small_PS(db_dir, pgc[i], ra_cen, dec_cen, d25[i], 90.-PA_gal)
     
       cmd = 'sh ds9_fits2jpeg_rotate.sh '+db_dir+ ' pgc'+str(pgc[i])+ ' '+  str(d25[i])+ ' '+  str(90.-PA_gal)+' &'
       
       print cmd
       xcmd(cmd, True)
 
       xcmd('rm '+db_dir+'/pgc'+str(pgc[i])+'*fits* ', True)


################################ BEGIN Get Colorful images directly from SDSS
       if np.isnan(d25[i]):
          d25[i] = 2.
       size = (d25[i]*3)/60.
       if size>3:
          size = 3.

       npix = int(size*3600 / 0.250)

       cmd = 'bash cutoutFromSDSS.bash '+str(ra_cen)+' '+str(dec_cen)+' '+str(npix)+' '+str(90.-PA_gal)+' '+db_dir+' &'
       
       print cmd
       
       xcmd(cmd, True)
       xcmd('mv '+db_dir+'/test.jpg '+db_dir+'/SDSS_PNG_rotate_finale/'+'pgc'+str(pgc[i])+'_d25x2_rot_gri.jpg', True)
################################ END Get Colorful images directly from SDSS
       
       #####sys.exit()
    
    ### NOTE: run this in csh

print p    

    

    
    

   
   
   
   










