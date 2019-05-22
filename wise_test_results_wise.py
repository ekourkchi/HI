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
w1   = table['W1']
w2   = table['W2']
w3   = table['W3']
w4   = table['W4']

w1_lit = []
w2_lit = []
w3_lit = []
w4_lit = []
w1_esn = []
w2_esn = []
w3_esn = []
w4_esn = []
pgc_pk = []

temp = np.chararray(len(pgc))

N = len(pgc)
db_root = '/home/ehsan/db_esn/data/'

mags = np.zeros([N, 8])

no = 0
for i in range(N):
  
  db_id = ra_db(ra[i])
  pgc_id = 'pgc'+str(pgc[i])
  
  
  
  filters = ['w1','w2','w3','w4']
  
  for p in range(4):
    
    filter = filters[p]
    photometry =  db_root+db_id+'/photometry/'+pgc_id+'_'+filter+'_asymptotic.dat'
    if os.path.exists(photometry):

      with open(photometry) as f:
	counter = 1
	for line in f:
	  if counter == 17:
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
     s += " || " + str(w1[i])
     s += " || " + str(w2[i])
     s += " || " + str(w3[i])
     s += " || " + str(w4[i])
     s += " || " + ' * '
     for p  in range(4):
       s += " || " + str(mags[i][p])
     
     
     s += " || [http://www.ifa.hawaii.edu/~ehsan/test/" + pgc_id
     s += "_wise_profile.jpg profile]  ||  [http://www.ifa.hawaii.edu/~ehsan/test/" + pgc_id
     s += "_wise_images.jpg images]  || "
     
     #print s
     
     #fname1 = db_root+db_id+'/plots/'+pgc_id+'_wise_images.jpg'
     #command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/test/']
     #subprocess.call(command)
     #fname1 = db_root+db_id+'/plots/'+pgc_id+'_wise_profile.jpg'
     #command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/test/']
     #subprocess.call(command)
     
     w1_esn.append(w1[i])
     w2_esn.append(w2[i])
     w3_esn.append(w3[i])
     w4_esn.append(w4[i])
     
     w1_lit.append(mags[i][0])
     w2_lit.append(mags[i][1])
     w3_lit.append(mags[i][2])
     w4_lit.append(mags[i][3])
     
     pgc_pk.append(pgc[i])
     

w1_lit = np.asarray(w1_lit)
w2_lit = np.asarray(w2_lit)
w3_lit = np.asarray(w3_lit)
w4_lit = np.asarray(w4_lit)

w1_esn = np.asarray(w1_esn)
w2_esn = np.asarray(w2_esn)
w3_esn = np.asarray(w3_esn)
w4_esn = np.asarray(w4_esn)

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

#ax.set_ylim([-0.4,0.4])
#ax.set_xlim([5,20])

ax.set_xlabel('w1-mag (Neil)', fontsize=14)

ax.set_ylabel(r'$\Delta$'+'w1 (Neil-Ehan)', fontsize=14)



lit =  w1_lit
ehsan =  w1_esn
ax.plot(lit, lit-ehsan, 'o', color='green', markersize=4, picker=5)



def onpick(event):
    ind = event.ind
    print 'pgc', pgc_pk[ind]

fig.canvas.mpl_connect('pick_event', onpick)


plt.show()

  
  
  
  
  
  
  
  



