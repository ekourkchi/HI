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
              if line.split(" ")[0]!= '#' and line.split(" ")[0]!='#\n': # counter == 17:
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
def make_small(db_dir, pgc, ra, dec, d25, angle):
  
  pgc_root = db_dir
  name = 'pgc'+str(pgc)
  
  for band in ['g','r','i']:
    
    pgc_band_root = pgc_root
    

    
    cmd = 'mkdir '+pgc_band_root+'/tmp'
    xcmd(cmd, True)
  
    cmd = 'cp '+pgc_band_root+name+'_'+band+'.fits '+pgc_band_root+'/tmp/.'
    xcmd(cmd, True)
    
    #cmd = 'gunzip '+pgc_band_root+'/tmp/pgc'+str(pgc)+'_'+band+'.fits.gz'
    #xcmd(cmd, True)
    
    #file = pgc_band_root+'/tmp/pgc'+str(pgc)+'_'+band+'.fits'
    #cmd = 'mRotate -r '+str(angle)+' '+file+' '+file
    #xcmd(cmd, True)
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
      
      #sys.exit()
      
      xcmd('tcsh montage.csh', True)
      
      size = (d25*3)/60.
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
# removing all spaces in front of a string
def trimstr(string):
    
    n = 0 
    N = len(string)
    m = N-1
    
    while string[n] == ' ':
        n+=1
    while string[m] == ' ':
        m-=1        
    
    return string[n:m+1]
    
      
###########################################################################    
##################################################

inFile  = '../augment/EDD_distance_cf4_v25.csv'
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
#inFile = '../augment/TFcalibrators.csv'
#table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#pgc_TFcalibrators    = table['PGC']
###################################################
#inFile = '../augment/TFcalibrators_Arecibo.csv'
#table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
#pgc_TF_arecibo    = table['PGC']
#RADE_TF_arecibo   = table['RADE']
#TY_TF_arecibo     = table['T']
#logr25_TF_arecibo = table['logr25']
#Glon_TF_arecibo = table['Glon']
#Glat_TF_arecibo = table['Glat']
#SGL_TF_arecibo = table['SGL']
#SGB_TF_arecibo = table['SGB']
#b_a_TF_arecibo = 1./(10**logr25_TF_arecibo)
######################################
##################################################
repository = '/home/ehsan/db_esn/DSS/' 

db_dir_sdss = '/home/ehsan/db_esn/cf4_sdss/'
db_dir_wise = '/home/ehsan/db_esn/cf4_wise/'

inFile = '/home/ehsan/PanStarrs/Jan/HI/augment/wise_all.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
ID_all  = table['ID']
PGC_all = table['PGC']

inFile = '/home/ehsan/PanStarrs/Jan/HI/augment/go4WISE.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
go4WISE    = table['PGC']

p = 0 
for i in range(0, len(pgc)):
  
    if pgc[i] in go4WISE: #pgc_TFcalibrators or pgc[i] in pgc_TF_arecibo:
        
        #if dec[i] <= -30 and sdss[i]==0:
            
            #dataDir = db_dir_wise+'/data/'+ra_db(ra[i])+'/wise/fits/'
            #name = 'pgc'+str(pgc[i])
            #ellipsefile = db_dir_wise+'/data/'+ra_db(ra[i])+'/photometry/'+name+'_w1_ellipsepar.dat'
            #if not os.path.isfile(ellipsefile) and pgc[i] in PGC_all:
                #i_lst = np.where(pgc[i] == PGC_all)   
                #name = ID_all[i_lst[0]][0]
                #ellipsefile = db_dir_wise+'/data/'+ra_db(ra[i])+'/photometry/'+name+'_w1_ellipsepar.dat'
            
            #if os.path.isfile(ellipsefile):
                  #ra_cen, dec_cen, semimajor, semiminor, PA_gal = get_ellipse(ellipsefile)
                  #d25[i] = 1.2*semimajor/60.
            #else:
            if True:
                PA_gal  = PA[i]
                ra_cen  = ra[i] 
                dec_cen = dec[i]
            
            
            if np.isnan(d25[i]):
               d25[i] = 2.
            size = (d25[i]*3)/60.
            if size>3:
               size = 3.           
            
            print "===================================================="
            print i, pgc[i], ra_cen, dec_cen, d25[i], 90.-PA_gal
            #print semimajor, semiminor, ellipsefile
            print "===================================================="
       
            name = 'pgc'+str(pgc[i])
            if True:
                             
               for filter in ['2b','2r','2i']:
                  
                  if filter=='2b': band='g'
                  if filter=='2r': band='r'
                  if filter=='2i': band='i'
                  outFits = repository+name+'_'+band+'.fits'
                  
                  cmd = 'sh get_DSS.sh '+str(ra[i])+' '+str(dec[i])+' '+filter+' '+outFits+' '+str(size*60.)
                  xcmd(cmd, True)

               
               make_small(repository, pgc[i], ra_cen, dec_cen, d25[i], 90.-PA_gal)
               cmd = 'sh ds9_fits2jpeg_rotate_dss.sh '+repository+ ' pgc'+str(pgc[i])+ ' '+  str(d25[i])+ ' '+  str(90.-PA_gal)
               xcmd(cmd, True)

               
               xcmd('rm -rf '+ repository+'/*fits', True)
               
               p+=1
               
            
    
print "New TF gals: #", p

