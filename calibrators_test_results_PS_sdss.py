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


inFile = 'wise_photometry.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc  = table['PGC']
ra   = table['RAJ']   # deg
dec  = table['DEJ']   # deg
d1   = table['MAJ']   # arcmin
d2   = table['MIN']   # arcmin
pa   = table['PA']
ty   = table['Type']
uu   = table['u']
gg   = table['g']
rr   = table['r']
ii   = table['i']
zz   = table['z']



temp = np.chararray(len(pgc))

N = len(pgc)
db_root = '/home/ehsan/db_esn/data/'

mags = np.zeros([N, 5])

no = 0
for i in range(N):
  
  db_id = ra_db(ra[i])
  pgc_id = 'PS_pgc'+str(pgc[i])
  
  
  
  filters = ['g','r','i','z']
  
  for p in range(4):
    
    filter = filters[p]
    photometry =  db_root+db_id+'/photometry/'+pgc_id+'_'+filter+'_asymptotic.dat'
    if os.path.exists(photometry):
      with open(photometry) as f:
	counter = 1
	for line in f:
	  if counter == 14:
	    line_split = line.split(" ")
	    not_void = 0 
	    for thing in line_split:
	      if thing != '': not_void+=1
	      if not_void==2: 
		break
	    mags[i][p] = np.float(thing)
	  counter+=1
  
  if mags[i][0] !=0 :
    
     no+=1
     
     s = ''
     s += "|| " + str(no) + " " 
     s += " || " + str(pgc[i])
     #s += " || " + str(uu[i])
     s += " || " + str(gg[i])
     s += " || " + str(rr[i])
     s += " || " + str(ii[i])
     s += " || " + str(zz[i])
     s += " || " + ' * '
     for p  in range(4):
       s += " || " + str(mags[i][p])
     
     s += " || [http://www.ifa.hawaii.edu/~ehsan/test/" + pgc_id
     s += "_panstarrs_profile.jpg profile]  ||  [http://www.ifa.hawaii.edu/~ehsan/test/" + pgc_id
     s += "_panstarrs_images.jpg images]  || "

     
     #print s
     #print ra[i], dec[i]
     
     
     
     #fname1 = db_root+db_id+'/plots/'+pgc_id+'_panstarrs_images.jpg'
     #command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/test/']
     #subprocess.call(command)
     #fname1 = db_root+db_id+'/plots/'+pgc_id+'_panstarrs_profile.jpg'
     #command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/test/']
     #subprocess.call(command)
  
  
  
###################################################
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

ax.set_ylim([-0.4,0.4])
ax.set_xlim([9,18])

ax.set_xlabel('g-mag (Don SDSS)', fontsize=14)

ax.set_ylabel(r'$\Delta$'+'g (Don SDSS - Ehsan PS)', fontsize=14)



lit =  gg[0:N]
ehsan =  mags[0:N,0]
ax.plot(lit, lit-ehsan, 'o', color='green', markersize=4, picker=5)



def onpick(event):
    ind = event.ind
    print 'pgc', pgc[ind]

fig.canvas.mpl_connect('pick_event', onpick)


plt.show()
###################################################

  
  
  
  
  
  
  
  



