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


inFile  = 'EDD_distance_cf4_v13.csv'
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
##################################################

inFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_ehsan_calib.lst.output'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_incout    = table['pgc']
inc_incout    = table['inc']
flag_incout   = table['flag']

pgc_common = []
my_inc     = []
th_inc     = []

for i in range(len(pgc_TFcalibrators)):
    
    if pgc_TFcalibrators[i] in pgc_incout:
        
        i_lst = np.where(pgc_incout == pgc_TFcalibrators[i])
        if flag_incout[i_lst][0]<=0:

           my_inc.append(inc_incout[i_lst][0])
           pgc_common.append(pgc_TFcalibrators[i])
           th_inc.append(inc_TFcalibrators[i])
           
           #print pgc_TFcalibrators[i]
        
        
        
fig = py.figure(figsize=(7, 5), dpi=100)
fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
ax = fig.add_subplot(111)    


p1, = ax.plot([0,100], [0,100], color='black', linestyle='-', label="equality")
p2, = ax.plot([0,100], [5,105], color='b', linestyle=':', label=r'$\pm5^o$')
ax.plot([0,100], [-5,95], color='b', linestyle=':')
p3, = ax.plot([0,100], [10,110], color='g', linestyle='--', label=r'$\pm10^o$')
ax.plot([0,100], [-10,90], color='g', linestyle='--')
ax.plot(th_inc, my_inc, 'r.')



th_inc = np.asarray(th_inc)
my_inc = np.asarray(my_inc)

N = len(th_inc)
a1 = np.zeros(N)
a2 = np.zeros(N)


a1[np.where(th_inc<80)] = 1
a2[np.where(th_inc>60)] = 1
a = a1 + a2

index = np.where(a==2)
th_inc = th_inc[index]
my_inc = my_inc[index]

delta = th_inc-my_inc
std = np.std(delta)
rms = np.sqrt(np.mean(delta**2))

ax.set_xlim([20,100])
ax.set_ylim([20,100])
ax.text(23,80, r'$RMS: $'+"%.1f" % (rms)+r'$^o$')
#ax.text(30,90, r'$\sigma: $'+"%.1f" % (std)+r'$^o$')
ax.set_xlabel('Inc. (RC3) [deg]', fontsize=14)
ax.set_ylabel('Inc. (Cf4) [deg]', fontsize=14)
ax.tick_params(which='major', length=5, width=2.0, direction='in')
ax.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')
ax.minorticks_on()

# Legend
lns = [p1, p2, p3]
ax.legend(handles=lns, loc='best')

plt.show()

    

    
    

   
   
   
   










