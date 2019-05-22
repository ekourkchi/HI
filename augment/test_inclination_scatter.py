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
def myPlot(ax, xFile, yFile, pcolor):

    table = np.genfromtxt(yFile , delimiter=',', filling_values=None, names=True, dtype=None)
    pgc_incout    = table['pgc']
    inc_incout    = table['inc']
    flag_incout   = table['flag']

    table = np.genfromtxt(xFile , delimiter=',', filling_values=None, names=True, dtype=None)
    pgc_brent    = table['pgc']
    inc_brent    = table['inc']
    flag_brent   = table['flag']

    pgc_common = []
    my_inc     = []
    th_inc     = []  # brent

    for i in range(len(pgc_brent)):
        
        if flag_brent[i]==0 and pgc_brent[i] in pgc_incout:
            
            i_lst = np.where(pgc_incout == pgc_brent[i])
            if flag_incout[i_lst][0]==0:

               my_inc.append(inc_incout[i_lst][0])
               pgc_common.append(pgc_brent[i])
               th_inc.append(inc_brent[i])


    th_inc = np.asarray(th_inc)
    my_inc = np.asarray(my_inc)
    ax.plot(th_inc, my_inc-th_inc, pcolor, ms=2, color='black')
    
    return th_inc, my_inc-th_inc
######################################


        
        
        
fig = py.figure(figsize=(7, 5), dpi=100)
fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
ax = fig.add_subplot(111)    


xFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_brent_calib.lst.output'


yFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_ehsan_calib.lst.output'
inc, delta=myPlot(ax, xFile, yFile, '.')

#yFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_arash_calib.lst.output'
#inc0, delta0=myPlot(ax, xFile, yFile, '.')
#delta = np.concatenate((delta, delta0)) 
#inc = np.concatenate((inc, inc0)) 

#yFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_amber_calib.lst.output'
#inc0, delta0=myPlot(ax, xFile, yFile, '.')
#delta = np.concatenate((delta, delta0)) 
#inc = np.concatenate((inc, inc0)) 

#yFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_lexie_calib.lst.output'
#inc0, delta0=myPlot(ax, xFile, yFile, '.')
#delta = np.concatenate((delta, delta0)) 
#inc = np.concatenate((inc, inc0)) 

#yFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_chase_calib.lst.output'
#inc0, delta0=myPlot(ax, xFile, yFile, '.')
#delta = np.concatenate((delta, delta0)) 
#inc = np.concatenate((inc, inc0)) 

delta=np.array(delta)
ave = np.median(delta)
std = np.std(delta)
ax.plot([0,100], [ave,ave], color='b', linestyle='--')   
ax.plot([0,100], [ave+std,ave+std], color='g', linestyle=':')  
ax.plot([0,100], [ave-std,ave-std], color='g', linestyle=':')  


ax.text(35,-24, r'$\sigma: \pm$'+"%.1f" % (std)+r'$^o$')
ax.text(35,-19, r'$offset: $'+"%.1f" % (ave)+r'$^o$')





Linc=[]
Linc_err=[]
LincY=[]
for incl in np.arange(40,90,2):
    Linc.append(incl+1)
    
    el=[]
    for i in range(len(inc)):
        if inc[i]>incl and inc[i]<=incl+2.:
            el.append(delta[i])
    el=np.asarray(el)
    Linc_err.append(np.std(el))
    LincY.append(np.median(el))
    
    
Linc=np.asarray(Linc) 
Linc_err=np.asarray(Linc_err) 
LincY=np.asarray(LincY)  
#ax.errorbar(Linc, 0.*Linc, yerr=Linc_err, fmt='o')    
ax.errorbar(Linc, LincY, yerr=Linc_err, fmt='o') 



ax.set_xlim([30,100])
ax.set_ylim([-30,30])


ax.set_xlabel('Inc. (Brent) [deg]', fontsize=14)
ax.set_ylabel('Inc. (Ehsan-Brent) [deg]', fontsize=14)
#ax.tick_params(which='major', length=5, width=2.0, direction='in')
#ax.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')
#ax.minorticks_on()



plt.show()

    

    
    

   
   
   
   










