#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 

#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.


def exclude(pgc, pgc_ex):
  
  pgc = np.asarray(pgc)
  pgc_ex = np.asarray(pgc_ex)
  pgc_ex = np.sort(pgc_ex)
  
  n0 = len(pgc)
  n_ex = len(pgc_ex)
  
  indices = np.arange(n0)
  ind_srot = np.argsort(pgc)
  indices = indices[ind_srot]
  pgc = pgc[ind_srot]
  
  j = 0 
  for i in range(n_ex):
    while(pgc[j] < pgc_ex[i]):
      j+=1
    if pgc[j] == pgc_ex[i]:
      indices[j] = -1   # will be excluded
      j+=1
  
  return (indices[np.where(indices > -1)],)
  

#################

p1 = [10,34,5,2,6,12,7,278,25,4,72]
p2 = [5,278,10,34]




inFile = 'edd_HI_ba_T_9060.short.csv'
#inFile = 'EDDtable14Jan2016022406.txt'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc         = table['PGC']
d25      = table['d25']
#Wmx_av      = table['Wmx_av']
#eW_av       = table['eW_av']

#indices = np.where(eW_av<20)
#pgc = pgc[indices]
#logd25 = logd25[indices]



#cfd2_file = 'CF2D2.1_allsky.csv'
#table = np.genfromtxt( cfd2_file , delimiter=',', filling_values=0, names=True, dtype=None)
#pgc_ext = table['pgc']


#### To exclude cosmic-Flows2 catalog #######
#ex_ind = exclude(pgc, pgc_ext)
#logd25 = logd25[ex_ind]
#####################


#print len(logd25)





#d25 = 0.1*(10**logd25)


# [20 --> 0]
edges = np.arange(0,21,0.1)
hist, bin_edges = np.histogram(d25, bins = edges)
hist = hist[::-1]
cumulative_hist = np.cumsum(hist)
cumulative_hist = cumulative_hist[::-1]


fig = py.figure(figsize=(6, 5), dpi=100)
fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)

ax = fig.add_subplot(111)
plt.minorticks_on()
plt.tick_params(which='major', length=7, width=1.5)
plt.tick_params(which='minor', length=4, color='#000033', width=1.0) 


ax.plot(edges[:-1], cumulative_hist, '-', markersize = 4, color='blue',  lw=2) #linestyle="dotted"

ax.plot([10,10], [15,50], '--', markersize = 4, color='red',  lw=2)
print "# > 10 -->  ", len(np.where(d25>10)[0])
ax.annotate(r'$35$',(10.25,60), fontsize=12)


ax.plot([5,5], [80,320], '--', markersize = 4, color='red',  lw=2)
print "# > 5 -->  ", len(np.where(d25>5)[0])
ax.annotate(r'$145$',(5.45,350), fontsize=12)


ax.plot([2,2], [700,2400], '--', markersize = 4, color='red',  lw=2)
print "# > 2 -->  ", len(np.where(d25>=2)[0])
ax.annotate(r'$1305$',(3,2800), fontsize=12)

print "# all  -->  ", len(d25)
ax.annotate(r'$9060$',(2,9900), fontsize=12)

#plt.xscale('log')
plt.yscale('log')
plt.xlim(20,0)
plt.ylim(0.1,2E4)

ax.set_xlabel('Diameter at B 25mag / as'+r'$^2$', fontsize=14)
ax.set_ylabel('# of galaxies', fontsize=14)
#ax.legend( loc=1 )
 
plt.show()

