#!/usr/bin/python
import sys
import os.path
import subprocess
import glob
import numpy as np
from astropy.table import Table, Column 
import pyfits
import pylab as py
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter



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


inFile = 'data_alf_test.plot.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc  = table['pgc']
g  = table['g']
r  = table['r']
ii  = table['i']
a_g  = table['a_g']  
a_r  = table['a_r']
a_i  = table['a_i'] 
quality  = table['quality']
g2  = table['g2']   
r2  = table['r2']
i2  = table['i2']   
quality2  = table['quality2']    
  
    
temp = np.chararray(len(pgc))

N = len(pgc)



no = 0

mag  = []
a    = []
mag2 = []
pgc_pk = []



for i in range(N):
  
  if (quality[i]>3 or quality[i]==-1) and quality2[i]>3:
      
      mag.append(ii[i])
      a.append(a_i[i])
      mag2.append(i2[i])
      pgc_pk.append(pgc[i])
      
mag = np.asarray(mag)
a = np.asarray(a)
a = a/60.
mag2 = np.asarray(mag2)
pgc_pk = np.asarray(pgc_pk)

fig = py.figure(figsize=(7, 5), dpi=100)
fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
ax = fig.add_subplot(111)
plt.tick_params(which='major', length=7, width=1.5)
plt.tick_params(which='minor', length=4, color='#000033', width=1.0) 


ax.plot([0,20], [-0.05,-0.05], ':', color='blue')
ax.plot([0,20], [+0.05,+0.05], ':', color='blue')
ax.plot([0,20], [-0.1,-0.1], ':', color='red')
ax.plot([0,20], [+0.1,+0.1], ':', color='red')
ax.plot([0,20], [0,0], '--', color='black')

ax.set_xlim([0,10])
#ax.set_ylim([5,20])

ax.set_xlabel('size-semimajor (arcmin)', fontsize=14)
ax.set_ylabel(r'$\Delta$'+'i (IPAC-SDSS)', fontsize=14)




ax.plot(a, mag-mag2, 'o', color='orange', markersize=4, picker=5)

print len(mag)

def onpick(event):
    ind = event.ind
    print 'pgc', pgc_pk[ind]

fig.canvas.mpl_connect('pick_event', onpick)


plt.show()

  
  
  
  
  
  
  
  



