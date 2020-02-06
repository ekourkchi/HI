#!/usr/bin/python
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table, Column 
from scipy.stats import linregress
from scipy import interpolate
from scipy import polyval, polyfit
from scipy import odr
import pylab as py
from matplotlib import gridspec

################################################################# 
def add_axis(ax, xlim, ylim):
    
    x1, x2 = xlim[0], xlim[1]
    y1, y2 = ylim[0], ylim[1]
    ax.set_xlim(x1, x2)
    ax.set_ylim(y1, y2)

    ax.minorticks_on()
    ax.tick_params(which='major', length=5, width=1.0)
    ax.tick_params(which='minor', length=2, color='#000033', width=1.0)     
    
    # additional Y-axis (on the right)
    y_ax = ax.twinx()
    y_ax.set_ylim(y1, y2)
    y_ax.set_yticklabels([])
    y_ax.minorticks_on()
    y_ax.tick_params(which='major', length=5, width=1.0, direction='in')
    y_ax.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')

    # additional X-axis (on the top)
    x_ax = ax.twiny()
    x_ax.set_xlim(x1, x2)
    x_ax.set_xticklabels([])
    x_ax.minorticks_on()
    x_ax.tick_params(which='major', length=5, width=1.0, direction='in')
    x_ax.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')
################################################################# 
    
def singlePlot(ax, pgc_ESN, pgc_ext, mag_ESN, mag_ext, qlt, color='red', xtitle='SDSS-r [mag]', ytitle='$\Delta [mag]$', exinct=False, A=None, xlim=[6,20], ylim=[-0.3,0.3]):

    magX = []
    magY = []
    for i in range(len(pgc_ext)):
        if pgc_ext[i] in pgc_ESN:
            j = np.where(pgc_ESN==pgc_ext[i])
            
            if qlt[j][0]>4  and mag_ext[i]>0:
                magX.append(np.float("%.2f"%mag_ext[i]))
                if exinct:
                    magY.append(mag_ESN[j][0]-A[j][0])
                else:
                    magY.append(mag_ESN[j][0])
    magX = np.asarray(magX)
    magY = np.asarray(magY)
    
    ax.plot(magX, magY-magX, '.', color=color, alpha=0.4)
    ax.plot(xlim, [0,0], 'k:')    
    add_axis(ax,xlim,ylim)
    ax.set_xlabel(xtitle, fontsize=14)
    ax.set_ylabel(ytitle, fontsize=14)
    
    indx = np.where(magY-magX>-0.2)
    magY = magY[indx]
    magX = magX[indx]
    
    indx = np.where(magY-magX<0.2)
    magY = magY[indx]
    magX = magX[indx]
    
    
    delta = magY-magX
    mean = np.mean(delta)
    medain = np.median(delta)
    stdev = np.std(delta)
    
    ax.text(7,-0.22, "median: "+'%.2f'%medain, fontsize=10)
    ax.text(7,-0.28, "$\mu$: "+'%.2f'%mean+"  $\sigma$: "+'%.2f'%stdev+' [mag]', fontsize=10)
    

########################################################### Begin
inFile  = 'EDD_distance_cf4_v27.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)

pgc_ESN = table['pgc']
u_mag_ESN = table['u_mag']
g_mag_ESN = table['g_mag']
r_mag_ESN = table['r_mag']
i_mag_ESN = table['i_mag']
z_mag_ESN = table['z_mag']
w1_mag_ESN = table['w1_mag']
w2_mag_ESN = table['w2_mag']
Sqlt = table['Sqlt']
Wqlt = table['Wqlt']
A_u_ESN = table['A_u']
A_g_ESN = table['A_g']
A_r_ESN = table['A_r']
A_i_ESN = table['A_i']
A_z_ESN = table['A_z']
A_w1_ESN = table['A_w1']
A_w2_ESN = table['A_w2']


inFile  = 'Neil+14_EDDphot.csv'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=-1, names=True, dtype=None)
pgc_neil = table['PGC']
u_mag_neil = table['u']
g_mag_neil = table['g']
r_mag_neil = table['r']
i_mag_neil = table['i']
z_mag_neil = table['z']
w1_mag_neil = table['W1']
w2_mag_neil = table['W2']


inFile  = 'Neil+14_table1.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgc_Ntab = table['PGC']
I_mag_Ntab = table['Imag'] # Vega
#I_mag_Ntab += 0.342   # AB
W1mag_Ntab = table['W1mag']
W2mag_Ntab = table['W2mag']

inFile  = 'PoFeng_wise.csv'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=-1, names=True, dtype=None)
pgc_feng = table['PGC']
u_mag_feng = table['u']
g_mag_feng = table['g']
r_mag_feng = table['r']
i_mag_feng = table['i']
z_mag_feng = table['z']
w1_mag_feng = table['W1']
w2_mag_feng = table['W2']

inFile  = 'hall2012.csv'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=-1, names=True, dtype=None)
pgc_hall = table['PGC']
i_mag_hall = table['m_ext']
g_r = table['g_r']
g_i = table['g_i']
g_mag_hall = g_i+i_mag_hall
r_mag_hall = g_mag_hall-g_r
BT = table['BT']
IT = table['IT']







################################################################# 
#fig = py.figure(figsize=(11, 3), dpi=100)   
#fig.subplots_adjust(wspace=0.4, hspace = 0.2, top=0.95, bottom=0.20, left=0.09, right=0.98)
#gs = gridspec.GridSpec(1, 3) 
#p = 0


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_hall, g_mag_ESN, g_mag_hall, Sqlt, color='green', xtitle='$[g]_{Hall12}$', ytitle='$g-[g]_{Hall12}$', exinct=False, A=A_g_ESN, ylim=[-0.75,0.75], xlim=[9,17])

#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_hall, r_mag_ESN, r_mag_hall, Sqlt, color='red', xtitle='$[r]_{Hall12}$', ytitle='$r-[r]_{Hall12}$', exinct=False, A=A_r_ESN, ylim=[-0.75,0.75], xlim=[9,17])

#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_hall, i_mag_ESN, i_mag_hall, Sqlt, color='orange', xtitle='$[i]_{Hall12}$', ytitle='$i-[i]_{Hall12}$', exinct=False, A=A_i_ESN, ylim=[-0.75,0.75], xlim=[9,17])



magX = []
magY = []

for i in range(len(pgc_hall)):
    if pgc_hall[i] in pgc_ESN:
        j = np.where(pgc_ESN==pgc_hall[i])
        
        if Sqlt[j][0]>3:
           magX.append(np.float("%.2f"%i_mag_hall[i]))
           magY.append(np.float("%.2f"%i_mag_ESN[j][0]))

magX = np.asarray(magX)
magY = np.asarray(magY)

fig = plt.figure(figsize=(6,4), dpi=100)
fig.subplots_adjust(top=0.95, bottom=0.15, left=0.2, right=0.98)
ax = fig.add_subplot(111)


ax.plot(magY, magX-magY, '.', color='k', alpha=0.15)
ax.plot([7,17], [0,0], 'k:')

xlim=[7,17]; ylim=[-0.75,0.75]
add_axis(ax,xlim,ylim)
ax.set_xlabel('$[i]_{this\/\/ study}$', fontsize=16)
ax.set_ylabel('$[i]_{Hall12}-[i]_{this\/\/ study}$', fontsize=16)

delta = magY-magX
mean = np.mean(delta)
medain = np.median(delta)
stdev = np.std(delta)

ax.text(8,-0.4, "median: "+'%.2f'%medain, fontsize=12)
ax.text(8,-0.5, "mean: "+'%.2f'%mean, fontsize=12)
ax.text(8,-0.6, "$\sigma$: "+'%.2f'%stdev+'  mag' , fontsize=12)

################################################################# 
#fig = py.figure(figsize=(13, 5), dpi=100)   
#fig.subplots_adjust(wspace=0.4, hspace = 0.35, top=0.97, bottom=0.12, left=0.06, right=0.98)
#gs = gridspec.GridSpec(2, 4) 
#p = 0


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_feng, u_mag_ESN, u_mag_feng, Sqlt, color='blue', xtitle='$[u]_{Wu15}$', ytitle='$u-[u]_{Wu15}$', exinct=True, A=A_u_ESN)

#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_feng, g_mag_ESN, g_mag_feng, Sqlt, color='green', xtitle='$[g]_{Wu15}$', ytitle='$g-[g]_{Wu15}$', exinct=True, A=A_g_ESN)

#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_feng, r_mag_ESN, r_mag_feng, Sqlt, color='red', xtitle='$[r]_{Wu15}$', ytitle='$r-[r]_{Wu15}$', exinct=True, A=A_r_ESN)


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_feng, i_mag_ESN, i_mag_feng, Sqlt, color='orange', xtitle='$[i]_{Wu15}$', ytitle='$i-[i]_{Wu15}$', exinct=True, A=A_i_ESN)


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_feng, z_mag_ESN, z_mag_feng, Sqlt, color='maroon', xtitle='$[z]_{Wu15}$', ytitle='$z-[z]_{Wu15}$', exinct=True, A=A_z_ESN)

#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_feng, w1_mag_ESN, w1_mag_feng, Wqlt, color='purple', xtitle='$[W1]_{Wu15}$', ytitle='$W1-[W1]_{Wu15}$', exinct=True, A=A_w1_ESN)


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_feng, w2_mag_ESN, w2_mag_feng, Wqlt, color='black', xtitle='$[W2]_{Wu15}$', ytitle='$W2-[W2]_{Wu15}$', exinct=True, A=A_w2_ESN)

################################################################# 
#fig = py.figure(figsize=(13, 5), dpi=100)   
#fig.subplots_adjust(wspace=0.4, hspace = 0.35, top=0.97, bottom=0.12, left=0.06, right=0.98)
#gs = gridspec.GridSpec(2, 4) 
#p = 0


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_neil, u_mag_ESN, u_mag_neil, Sqlt, color='blue', xtitle='$[u]_{Neil14}$', ytitle='$u-[u]_{Neil14}$')

#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_neil, g_mag_ESN, g_mag_neil, Sqlt, color='green', xtitle='$[g]_{Neil14}$', ytitle='$g-[g]_{Neil14}$')

#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_neil, r_mag_ESN, r_mag_neil, Sqlt, color='red', xtitle='$[r]_{Neil14}$', ytitle='$r-[r]_{Neil14}$')


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_neil, i_mag_ESN, i_mag_neil, Sqlt, color='orange', xtitle='$[i]_{Neil14}$', ytitle='$i-[i]_{Neil14}$')


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_neil, z_mag_ESN, z_mag_neil, Sqlt, color='maroon', xtitle='$[z]_{Neil14}$', ytitle='$z-[z]_{Neil14}$')

#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_Ntab, w1_mag_ESN, W1mag_Ntab, Wqlt, color='purple', xtitle='$[W1]_{Neil14}$', ytitle='$W1-[W1]_{Neil14}$')


#ax = plt.subplot(gs[p]) ; p+=1 
#singlePlot(ax, pgc_ESN, pgc_Ntab, w2_mag_ESN, W2mag_Ntab, Wqlt, color='black', xtitle='$[W2]_{Neil14}$', ytitle='$W2-[W2]_{Neil14}$')

################################################################# 




################################################################# 
################################################################# 
############END################################################## 
################################################################# 
################################################################# 



#magX = []
#magY = []

#for i in range(len(pgc_hall)):
    #if pgc_hall[i] in pgc_neil:
        #j = np.where(pgc_neil==pgc_hall[i])
        
        #magX.append(np.float("%.2f"%i_mag_hall[i]))
        #magY.append(np.float("%.2f"%i_mag_neil[j][0]))

#magX = np.asarray(magX)
#magY = np.asarray(magY)

#fig = plt.figure(figsize=(6,4), dpi=100)
#fig.subplots_adjust(top=0.95, bottom=0.15, left=0.2, right=0.98)
#ax = fig.add_subplot(111)


#ax.plot(magX, magX-magY, '.', color='k')
#ax.plot([7,17], [0,0], 'k:')

#xlim=[7,17]; ylim=[-0.75,0.75]
#add_axis(ax,xlim,ylim)
#ax.set_xlabel('$[i]_{Hall12}$', fontsize=14)
#ax.set_ylabel('$[i]_{Hall12}-[i]_{Neil14}$', fontsize=14)
    
    
    
    
    

















#magX = []
#magY = []

#for i in range(len(pgc_Ntab)):
    #if pgc_Ntab[i] in pgc_ESN:
        #j = np.where(pgc_ESN==pgc_Ntab[i])
        
        #if Sqlt[j][0]>3 and Wqlt[j][0]>3 and I_mag_Ntab[i]>0:
           
           #g = g_mag_ESN[j][0]
           #r = r_mag_ESN[j][0]
           #ii = i_mag_ESN[j][0]
           #z = z_mag_ESN[j][0]

           ##magX.append(np.float("%.2f"%I_mag_Ntab[i]))
           ##I1 = r - 1.2444*(r - ii) - 0.3820 #  sigma = 0.0078
           ##I2 = ii - 0.3780*(ii - z)  -0.3974 #  sigma = 0.0063           
           ##magY.append(0.5*(I1+I2))
           
           #if r-ii<0.95:
                #magX.append(np.float("%.2f"%I_mag_Ntab[i]))
                #I = ii-0.14*(g-r)-0.35
                ###I = 1.017*I-0.221
                #magY.append(I)

#magX = np.asarray(magX)
#magY = np.asarray(magY)

#fig = plt.figure(figsize=(6,4), dpi=100)
#fig.subplots_adjust(top=0.95, bottom=0.15, left=0.2, right=0.98)
#ax = fig.add_subplot(111)


#ax.plot(magX, magX-magY, '.', color='g', alpha=0.5)
#ax.plot([7,16], [0,0], 'k:')

#xlim=[7,16]; ylim=[-0.75,0.75]
#add_axis(ax,xlim,ylim)
#ax.set_xlabel('$[I]_{Neil14}$'+'  [mag]', fontsize=16)
#ax.set_ylabel('$[I]_{Neil14}-I^c_{sdss}$'+'  [mag]', fontsize=16)

#delta = magX-magY
#mean = np.mean(delta)
#medain = np.median(delta)
#stdev = np.std(delta)

#ax.text(8,-0.4, "median: "+'%.2f'%medain, fontsize=11)
#ax.text(8,-0.5, "mean: "+'%.2f'%mean, fontsize=11)
#ax.text(8,-0.6, "$\sigma$: "+'%.2f'%stdev, fontsize=11)
#ax.text(8,0.5, "$I^c_{sdss}=i-0.14(g-r)-0.35$", fontsize=13)
##ax.text(8,0.6, "$I^c_{sdss}$: Lupton (2005)", fontsize=11)


for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(14) 
for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(14) 

#print len(magX)

plt.show()












#magX = []
#magY = []

#for i in range(len(pgc_Ntab)):
    #if pgc_Ntab[i] in pgc_ESN:
        #j = np.where(pgc_ESN==pgc_Ntab[i])
        
        #if Sqlt[j][0]>3 and Wqlt[j][0]>3 and I_mag_Ntab[i]>0:
           #magX.append(np.float("%.2f"%I_mag_Ntab[i]))
           #r = r_mag_ESN[j][0]
           #i = i_mag_ESN[j][0]
           #z = z_mag_ESN[j][0]
           #I1 = r - 1.2444*(r - i) - 0.3820 #  sigma = 0.0078
           #I2 = i - 0.3780*(i - z)  -0.3974 #  sigma = 0.0063           
           #magY.append(0.5*(I1+I2))
           ##magY.append(i)

#magX = np.asarray(magX)
#magY = np.asarray(magY)

#plt.plot(magX, magY-magX, '.', color='black', alpha=0.5)
#plt.plot([6,16], [0,0], 'k:')




































