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
    
  
  inFile  = 'EDD_distance_cf4_v21.csv'
  table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)

  pgc = table['pgc']
  ra = table['ra']
  dec = table['dec']
  SDSS = table['sdss']
  alfa100 = table['alfa100']
  QA_sdss = table['QA_sdss']
  QA_wise = table['QA_wise']
  Sqlt = table['Sqlt']
  Wqlt = table['Wqlt']
  inc = table['inc']
  
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
  
 
  
  
  X_sdss  = []
  Y_sdss  = []
  X_Nsdss = []
  Y_Nsdss = []
  sd = 0
  Nsd = 0
  Nwise = 0 
  
  X_SW  = []
  Y_SW  = []  
  N_SW = 0
 
  for i in range(len(pgc)):
        
    x, y = xymap_aitoff(ra[i], dec[i])

    
    
    sdss = int(SDSS[i])
    
    if QA_wise[i]>0:
      #X_Nsdss.append(x)
      #Y_Nsdss.append(y)   
      Nwise+=1
    
    if QA_wise[i]>0 and QA_sdss[i]>0:
      X_SW.append(x)
      Y_SW.append(y)   
      N_SW+=1    
    
    
    if sdss == 0:
      X_Nsdss.append(x)
      Y_Nsdss.append(y)
      Nsd+=1
    else:
      X_sdss.append(x)
      Y_sdss.append(y)
      sd+=1
  
  point, = ax.plot(X_sdss, Y_sdss, 'o', markersize = 1, color='green', markeredgecolor = 'green')
  point, = ax.plot(X_Nsdss, Y_Nsdss, 'o', markersize = 1, color='red', markeredgecolor = 'red')
  
  #point, = ax.plot(X_SW, Y_SW, 'o', markersize = 2, color='orange', markeredgecolor = 'orange')
    
  
  add_plane(ax, color='black', plane='galactic', projection='equatorial')
  add_psborder(ax, color='Cyan', plane='galactic', projection='equatorial')


  ax3 = fig.add_axes([0.65, 0.03, 0.29, 0.29])
  labels = 'SDSS', 'No SDSS !'
  f_sdss = 100.*sd/(sd+Nsd)
  f_other = 100.*(Nsd)/(sd+Nsd)
  fracs = [f_sdss, f_other]
  explode=(0.07, 0)
  colors = ['green','red']
  

  pie(fracs, explode=explode, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=90,colors=colors)

  

  width = 0.2       # the width of the bars

  ax2 = fig.add_axes([0.1, 0.05, 0.2, 0.2])
  ax2.set_xticks([1,2,3]) # ,4]) # ,5])
  ax2.set_xticklabels(['total', 'SDSS', 'No SDSS']) # , 'WISE']) # , 'S/D']) 
  ax2.set_ylabel("Number", fontsize=12)
  ax2.bar([1], [sd+Nsd], width, color='blue')             
  ax2.bar([2], [sd], width, color='green')
  ax2.bar([3], [Nsd], width, color='red')
  #ax2.bar([4], [Nwise], width, color='brown')
  #ax2.bar([5], [N_SW], width, color='orange')

  
  
  print sd+Nsd, sd, Nsd, Nwise, N_SW 
  
  
  plt.show()

  
