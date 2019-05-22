## Importing Important Python Libraries
import sys
import os
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import  lines
from matplotlib import rc, rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.patches import Polygon, Ellipse
import numpy as np
from math import *
from time import time
import wl_to_rgb as col
import random
from astropy.io import ascii
from astropy.table import Table, Column 
import pyfits
import pylab as py

from astropy import coordinates as coord
from astropy import units as unit

import matplotlib.colors as colors
import matplotlib.cm as cmx

import matplotlib.patches as mpatches

from kapteyn import wcs
from matplotlib import *

from pylab import *


################################################################ 
def xymap_aitoff(x,y):
  
  while x > 360:
    x-=360
  while x < 0:
    x+=360
    
  x0 = (180.-x)*pi/180.
  y0 = y*pi/180.
  
  return x0, y0
################################################################   
## Adding Pan-STARRS dec > -30 deg border 
def add_psborder(ax, color='black', plane=None, projection=None):
    
  if plane==None or projection==None:
    return
  
  alpha = np.arange(0.,360,2)
  delta = alpha*0.-30.   

  #tran = wcs.Transformation(plane + " j2000 j2000", projection)
  #alpha, delta = tran((alpha,delta))
  
  for i in range(len(alpha)):
    if alpha[i] >180:
      alpha[i] -= 360.
  
  ind = np.argsort(alpha)
  alpha = alpha[ind]
  delta = delta[ind]
  
  X = []
  Y = [] 
  
  for i in range(len(alpha)/2):
      x, y = xymap_aitoff(alpha[i], delta[i])
      X.append(x)
      Y.append(y)
      
  ax.plot(X, Y, '-', color=color,linewidth=3)   
  X = []
  Y = []    
  for i in range(len(alpha)/2, len(alpha)):
      x, y = xymap_aitoff(alpha[i], delta[i])
      X.append(x)
      Y.append(y)     
  ax.plot(X, Y, '-', color=color,linewidth=3)   

#################################################################

def add_plane(ax, color='black', plane=None, projection=None):
  
  if plane==None or projection==None:
    return
  
  alpha = np.arange(0.,360,2)
  delta = alpha*0.
  
  tran = wcs.Transformation(plane + " j2000 j2000", projection)
  alpha, delta = tran((alpha,delta))
  
  for i in range(len(alpha)):
    if alpha[i] >180:
      alpha[i] -= 360.
  
  ind = np.argsort(alpha)
  alpha = alpha[ind]
  delta = delta[ind]
  
  X = []
  Y = [] 
  
  for i in range(len(alpha)/2):
      x, y = xymap_aitoff(alpha[i], delta[i])
      X.append(x)
      Y.append(y)
      
  ax.plot(X, Y, '-', color=color)   
  X = []
  Y = []    
  for i in range(len(alpha)/2, len(alpha)):
      x, y = xymap_aitoff(alpha[i], delta[i])
      X.append(x)
      Y.append(y)     
  ax.plot(X, Y, '-', color=color)   

  
  
  
##########################################################################   
  
########################################################################## 
########################################################################## 
########################################################################## 
    
if __name__ == '__main__':
    
  
  inFile = 'Leda_Logd25.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)  
  all_pgc = table['PGC']
  all_logd25 = table['logd25']
  
  
  fig = plt.figure(figsize=(13, 8), dpi=100)
  ax = fig.add_subplot(111, projection="aitoff")
  plt.title("Equatorial Aitoff Projection", y=1.08)
  ax.grid(True)
  ax.set_xticklabels([])
  plt.subplots_adjust(top=0.90, bottom=0.3, right=0.95, left=0.05)
  
  ax.annotate(r'$0^o$', (pi-0.1,pi/3.), size=11, color='black')
  ax.annotate(r'$90^o$', (pi/2.-0.2,pi/3.), size=11, color='black')
  ax.annotate(r'$180^o$', (-0.2,pi/3.), size=11, color='black')
  ax.annotate(r'$270^o$', (-pi/2.-0.2,pi/3.), size=11, color='black')
  
  
  ax.annotate(r'$0^o$', (pi-0.1,pi/3.), size=11, color='black')
  ax.annotate(r'$90^o$', (pi/2.-0.2,pi/3.), size=11, color='black')
  ax.annotate(r'$180^o$', (-0.2,pi/3.), size=11, color='black')
  ax.annotate(r'$270^o$', (-pi/2.-0.2,pi/3.), size=11, color='black')  
  
  
  inFile = '../has_Hall.SDSS.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

  pgc         = table['pgc']
  ra          = table['ra']
  dec         = table['dec']
  SDSS        = table['SDSS']
  

  #pgc=[]
  #ra=[]
  #dec=[]
  #SDSS=[]
  
  # Augmentation part
  if True:
      inFile = 'a70_Tge1_ige60_Wge70_SNgt5.9832_has_SDSS.csv'
      table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
      pgc_aug         = table['pgc']
      ra_aug          = table['ra']
      dec_aug         = table['dec']
      SDSS_aug        = table['SDSS']
      

      
      pgc_1  = []
      ra_1   = []
      dec_1  = []
      SDSS_1 = []
      common = 0
      for i in range(len(pgc_aug)):
          if not pgc_aug[i] in pgc:
             pgc_1.append(pgc_aug[i])
             ra_1.append(ra_aug[i])
             dec_1.append(dec_aug[i])
             SDSS_1.append(SDSS_aug[i])
          else: 
              common += 1
              #print pgc_aug[i]
      
      #print 'common Galaxies: ',  common  
      pgc_1  = np.asarray(pgc_1)     
      ra_1   = np.asarray(ra_1)
      dec_1  = np.asarray(dec_1)
      SDSS_1 = np.asarray(SDSS_1)
      
      pgc = np.concatenate((pgc, pgc_1))
      ra = np.concatenate((ra, ra_1))
      dec = np.concatenate((dec, dec_1))
      SDSS = np.concatenate((SDSS, SDSS_1))
      
  #d25=[]
  #N = len(all_pgc)
  #for i in range(len(pgc)):
      #j = 0 
      #while j < N and pgc[i] != all_pgc[j]: j+=1
      #if j==N: d25_ = None
      #else: d25_ = 10**all_logd25[j]*0.1
      #d25.append(d25_)
      #if SDSS[i] == 1: 
         #print i, pgc[i],  d25_, 's'
      #elif SDSS[i] == 0 and dec[i]> -30:
         #print i, pgc[i],  d25_, 'p'
      #else: print i, pgc[i], d25_, 'o'
  
  #d25 = np.asarray(d25)
      
  
  
  
  X_sdss  = []
  Y_sdss  = []
  X_Nsdss = []
  Y_Nsdss = []
  sd = 0
  Nsd = 0
  
  pan = 0
  
  for i in range(len(pgc)):
        
    x, y = xymap_aitoff(ra[i], dec[i])

    
    
    sdss = int(SDSS[i])
    
    if sdss==0 and dec[i] > -30: pan+=1
        
    
    if sdss == 0:
      X_Nsdss.append(x)
      Y_Nsdss.append(y)
      Nsd+=1
    else:
      X_sdss.append(x)
      Y_sdss.append(y)
      sd+=1
  
  point, = ax.plot(X_sdss, Y_sdss, 'o', markersize = 1, color='blue', markeredgecolor = 'blue')
  point, = ax.plot(X_Nsdss, Y_Nsdss, 'o', markersize = 1, color='red', markeredgecolor = 'red')
  add_plane(ax, color='black', plane='galactic', projection='equatorial')
  add_psborder(ax, color='Orange', plane='galactic', projection='equatorial')


  ax3 = fig.add_axes([0.65, 0.03, 0.29, 0.29])
  labels = 'SDSS', 'Other !', 'Pan-STARRS'
  f_sdss = 100.*sd/(sd+Nsd)
  f_other = 100.*(Nsd-pan)/(sd+Nsd)
  f_pan = 100.*(pan)/(sd+Nsd)
  fracs = [f_sdss, f_other, f_pan]
  explode=(0.07, 0, 0)
  colors = ['blue','red','yellow']
  

  pie(fracs, explode=explode, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=90,colors=colors)
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.

  #title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})
  

  width = 0.35       # the width of the bars

  ax2 = fig.add_axes([0.1, 0.05, 0.2, 0.2])
  ax2.set_xticks([0,1.175,1.675,2.175,3])
  ax2.set_xticklabels(['','SDSS', 'Pan-STARRS','Other','']) 
  ax2.set_ylabel("Number", fontsize=12)
  ax2.bar([1], [sd], width, color='blue')             
  ax2.bar([1.5], [pan], width, color='yellow')
  ax2.bar([2], [Nsd-pan], width, color='red')
  #ax2.set_xticks([])
  #ax2.xaxis.set_ticks_position('none')
  
  plt.show()

  
