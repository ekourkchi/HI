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


inFile  = 'EDD_distance_cf4_v15.csv'
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
QA_SDSS = table['QA_sdss']

Squality = table['Sqlt']
Wquality = table['Wqlt']
Sba = table['Sba']
Wba = table['Wba']
##################################################
inFile = 'TFcalibrators.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_TFcalibrators    = table['PGC']
inc_TFcalibrators    = table['Inc']
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
##################################################
inFile = 'Wise_calib_visier.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_wise_vizier    = table['PGC']
inc_wise_vizier    = table['i']
b_a_wise_vizier    = table['b_a']
##################################################
# this is the Inclination code output
inFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_ehsan_calib.lst.output'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_incout    = table['pgc']
inc_incout    = table['inc']
flag_incout   = table['flag']

pgc_common = []
bas_common = []
baw_common = []
ba_wise_vizier = []
b_a_leda = []

for i in range(len(pgc)):
          
        if Squality[i]>3:# and Wquality[i]>3:
           
           #if pgc[i] in pgc_wise_vizier:
               
               #i_ind = np.where(pgc_wise_vizier==pgc[i])
               #ba_wise_vizier.append(b_a_wise_vizier[i_ind][0])
               
               pgc_common.append(pgc[i])
               bas_common.append(Sba[i])
               #baw_common.append(Wba[i])
               b_a_leda.append(b_a[i])

#bas_common = ba_wise_vizier
baw_common = b_a_leda
        
fig = py.figure(figsize=(7, 5), dpi=100)
fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
ax = fig.add_subplot(111)    



ax.plot(bas_common, baw_common, 'r.', color='orange')
p1, = ax.plot([0,1], [0,1], color='black', linestyle='-', label="equality")


bas_common = np.asarray(bas_common)
baw_common = np.asarray(baw_common)



delta = bas_common-baw_common
std = np.std(delta)
rms = np.sqrt(np.mean(delta**2))

ax.set_xlim([0,1])
ax.set_ylim([0,1])
ax.text(0.05,0.85, r'$RMS: $'+"%.1f" % (rms))
#ax.text(30,90, r'$\sigma: $'+"%.1f" % (std))
ax.set_xlabel('b/a (SDSS) [Cf4]', fontsize=14)
#ax.set_ylabel('b/a (WISE) [Cf4] ', fontsize=14)
#ax.set_xlabel('b/a (WISE) [Neil+14] ', fontsize=14)
ax.set_ylabel('b/a (LEDA] ', fontsize=14)
ax.tick_params(which='major', length=5, width=2.0, direction='in')
ax.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')
ax.minorticks_on()

# Legend
lns = [p1]
ax.legend(handles=lns, loc='best')

plt.show()

    

    
    

   
   
   
   










