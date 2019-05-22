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
from astropy.stats import sigma_clip

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
    
def singlePlot(ax, pgc_ESN, pgc_ext, mag_ESN, mag_ext, qlt, color='red', xtitle='SDSS-r [mag]', ytitle='$\Delta [mag]$', xlim=[6,20], ylim=[-0.4,0.4]):

    magX = []
    magY = []
    for i in range(len(pgc_ext)):
        if pgc_ext[i] in pgc_ESN:
            j = np.where(pgc_ESN==pgc_ext[i])
            
            if qlt[j][0]>3  and mag_ext[i]>0:
                magX.append(np.float("%.2f"%mag_ext[i]))
                magY.append(mag_ESN[j][0])
    magX = np.asarray(magX)
    magY = np.asarray(magY)
    
    ax.plot(magY, magY-magX, '.', color=color, alpha=0.01)
    ax.plot(xlim, [0,0], 'k:')    
    add_axis(ax,xlim,ylim)
    ax.set_xlabel(xtitle, fontsize=14)
    ax.set_ylabel(ytitle, fontsize=14)
    
    indx = np.where(magY-magX>-0.2)
    magY_ = magY[indx]
    magX_ = magX[indx]
    
    indx = np.where(magY_-magX_<0.2)
    magY_ = magY_[indx]
    magX_ = magX_[indx]
    
    
    delta = magY_-magX_
    mean = np.mean(delta)
    medain = np.median(delta)
    stdev = np.std(delta)
    
    ax.text(7,-0.30, "median: "+'%.2f'%medain, fontsize=10)
    ax.text(7,-0.37, "$\mu$: "+'%.2f'%mean+"  $\sigma$: "+'%.2f'%stdev+' [mag]', fontsize=9)
    
    
    median_ = []
    stdev_= []
    X_ = []
    
    dd = 1.0
    begin = 7
    end = begin+dd
    
    while end<19:
        indx = np.where(magY>begin)
        magY_ = magY[indx]
        magX_ = magX[indx]
        
        indx = np.where(magY_<end)
        magY_ = magY_[indx]
        magX_ = magX_[indx]
        
        delta = magY_-magX_
        
        filtered_data = sigma_clip(delta, sigma=4, iters=5, copy=False)
        delta = filtered_data.data[np.logical_not(filtered_data.mask)]
        
        medain = np.median(delta)
        stdev = np.std(delta)
        if stdev<0.2:
            median_.append(medain)
            stdev_.append(stdev)
            X_.append(np.median(begin+0.5*dd))
        begin+=dd
        end+=dd
        
        if end<15:
            print medain, stdev
    
    median_= np.asarray(median_)
    stdev_ = np.asarray(stdev_)
    X_ = np.asarray(X_)
    
    ax.plot(X_, median_, 'k-')
    ax.plot(X_, median_+stdev_, 'k--')
    ax.plot(X_, median_-stdev_, 'k--')
        


########################################################### Begin
inFile  = 'EDD_distance_cf4_v24.csv'
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

m255_u  = table['m255_u']
m255_g  = table['m255_g']
m255_r  = table['m255_r']
m255_i  = table['m255_i']
m255_z  = table['m255_z']

d_m_ext_u   = table['d_m_ext_u']
d_m_ext_g   = table['d_m_ext_g']
d_m_ext_r   = table['d_m_ext_r']
d_m_ext_i   = table['d_m_ext_i']
d_m_ext_z   = table['d_m_ext_z']

u_mag_prime = m255_u + d_m_ext_u
g_mag_prime = m255_g + d_m_ext_g
r_mag_prime = m255_r + d_m_ext_r
i_mag_prime = m255_i + d_m_ext_i
z_mag_prime = m255_z + d_m_ext_z

m255_w1  = table['m255_w1']
d_m_ext_w1  = table['d_m_ext_w1']

m255_w2  = table['m255_w2']
d_m_ext_w2  = table['d_m_ext_w2']

w1_mag_prime = m255_w1 + d_m_ext_w1
w2_mag_prime = m255_w2 + d_m_ext_w2
################################################################# 
fig = py.figure(figsize=(13, 5), dpi=100)   
fig.subplots_adjust(wspace=0.4, hspace = 0.35, top=0.97, bottom=0.12, left=0.06, right=0.98)
gs = gridspec.GridSpec(2, 4) 
p = 0


ax = plt.subplot(gs[p]) ; p+=1 
singlePlot(ax, pgc_ESN, pgc_ESN, u_mag_ESN, u_mag_prime, Sqlt, color='blue', xtitle='$u_{iso}$', ytitle='$u_{iso}-(u_{25.5}+\Delta u_{ext})$')

ax = plt.subplot(gs[p]) ; p+=1 
singlePlot(ax, pgc_ESN, pgc_ESN, g_mag_ESN, g_mag_prime, Sqlt, color='green', xtitle='$g_{iso}$', ytitle='$g_{iso}-(g_{25.5}+\Delta g_{ext})$')

ax = plt.subplot(gs[p]) ; p+=1 
singlePlot(ax, pgc_ESN, pgc_ESN, r_mag_ESN, r_mag_prime, Sqlt, color='red', xtitle='$r_{iso}$', ytitle='$r_{iso}-(r_{25.5}+\Delta r_{ext})$')


ax = plt.subplot(gs[p]) ; p+=1 
singlePlot(ax, pgc_ESN, pgc_ESN, i_mag_ESN, i_mag_prime, Sqlt, color='orange', xtitle='$i_{iso}$', ytitle='$i_{iso}-(i_{25.5}+\Delta i_{ext})$')


ax = plt.subplot(gs[p]) ; p+=1 
singlePlot(ax, pgc_ESN, pgc_ESN, z_mag_ESN, z_mag_prime, Sqlt, color='maroon', xtitle='$z_{iso}$', ytitle='$z_{iso}-(z_{25.5}+\Delta z_{ext})$')

ax = plt.subplot(gs[p]) ; p+=1 
singlePlot(ax, pgc_ESN, pgc_ESN, w1_mag_ESN, w1_mag_prime, Wqlt, color='purple', xtitle='$W1_{iso}$', ytitle='$W1_{iso}-(W1_{25.5}+\Delta W1_{ext})$')


ax = plt.subplot(gs[p]) ; p+=1 
singlePlot(ax, pgc_ESN, pgc_ESN, w2_mag_ESN, w2_mag_prime, Wqlt, color='deeppink', xtitle='$W2_{iso}$', ytitle='$W2_{iso}-(W2_{25.5}+\Delta W2_{ext})$')

################################################################# 


plt.show()
















