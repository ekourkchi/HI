#!/usr/bin/python
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import subprocess
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from astropy.table import Table, Column 
import pylab as py
import time
import datetime

inFile  = 'EDD_distance_cf4_v23.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgc = table['pgc']
inc     = table['inc']
inc_e   = table['inc_e']
inc_flg = table['inc_flg']
inc_n   = table['inc_n']

inFile  = 'EDD.inclination.All.Manoa.26Nov2018151327.txt'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgcID1 = table['pgcID']
checkinTime1 = [' '.join(dummy.split()) for dummy in table['checkinTime']]

inFile  = 'EDD.inclination.All.Guest.26Nov2018151255.txt'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgcID2 = table['pgcID']
inputTable2 = [' '.join(dummy.split()) for dummy in table['inputTable']]
email2 = [' '.join(dummy.split()) for dummy in table['email']]


pgcID = np.concatenate((pgcID1, pgcID2))

Na = len(pgc)
N3 = 0
N2 = 0
N1 = 0
N4 = 0 
N5 = 0

N0 = 0
for i in range(len(pgc)):
    
    if inc_flg[i]>0: N0+=1
    

for i in range(Na):
    
    if pgc[i] in pgcID:
        ind = np.where(pgcID==pgc[i])
        N =  len(ind[0])
        
        if N>=5: N5+=1
        if N>=4: N4+=1
        if N>=3: N3+=1
        if N>=2: N2+=1
        if N>=1: N1+=1

        
print Na, N1, N2, N3, N4, N5, len(pgcID)
        
fig = plt.figure(figsize=(6.7, 6), dpi=100)
ax = fig.add_axes([0.13, 0.1, 0.85,  0.85])
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='--', linewidth=1)

#n, bins, patches = ax.hist( [Na, N1, N2, N3], [0,1,2,3], histtype='bar',
			    #stacked=True)        

#ax.plot([0.5,0.5,6.5,6.5,0.5],[Na-N0,Na,Na,Na-N0,Na-N0], '..')

ax.add_patch(patches.Rectangle((0.5,Na-N0), 6, N0, color='black', alpha=0.2, linewidth=0))


rects1 = ax.bar([1], [Na], 0.5, color='blue')
rects2 = ax.bar([2], [N1], 0.5, color='red')
rects2 = ax.bar([3], [N2], 0.5, color='orange')
rects2 = ax.bar([4], [N3], 0.5, color='green')
rects2 = ax.bar([5], [N4], 0.5, color='dodgerblue')
rects2 = ax.bar([6], [N5], 0.5, color='darkorchid')

ax.annotate("%d"% (100.*N1/Na)+"%",(1.75,N1-1200), fontsize=10)
ax.annotate("%d"% (100.*N2/Na)+"%",(2.80,N2-1200), fontsize=12)
ax.annotate("%d"% (100.*N3/Na)+"%",(3.80,N3-1200), fontsize=12)
ax.annotate("%d"% (100.*N4/Na)+"%",(4.80,N4-1200), fontsize=12)
ax.annotate("%d"% (100.*N5/Na)+"%",(5.80,N5-1200), fontsize=12)

ax.annotate("Rejected Galaxies",(4, 18000), fontsize=14, color='gray')

ax.tick_params(bottom='off')
#py.setp(ax.get_xticklabels(), visible=False)
ax.set_xticks(range(1,7))
ax.set_xticklabels(['Total','N1','N2','N3', 'N4', 'N5'], fontsize=12)
ax.set_ylim([0, 20000])
ax.set_ylabel("No. of galaxies", fontsize=12)

date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")
ax.set_title("Last update: "+date)





plt.show()
        
        
        
        
