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



########################################################################## 
########################################################################## 
########################################################################## 
    
if __name__ == '__main__':
    
  
  inFile = 'pgc_d25.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)  
  
  all_pgc     = table['pgc']
  all_d25     = table['d25']
  all_survey  = table['survey']
  

  
  edges = np.arange(0,21,0.1)



  fig = py.figure(figsize=(6, 5), dpi=100)
  fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)

  ax = fig.add_subplot(111)
  plt.minorticks_on()
  plt.tick_params(which='major', length=7, width=1.5)
  plt.tick_params(which='minor', length=4, color='#000033', width=1.0) 

 
  d25=[]
  for i in range(len(all_pgc)):
      if all_d25[i]<30 :   # sdss
          d25.append(all_d25[i])
  d25=np.asarray(d25)
  print len(d25)

  hist, bin_edges = np.histogram(d25, bins = edges)
  hist = hist[::-1]
  cumulative_hist = np.cumsum(hist)
  cumulative_hist = cumulative_hist[::-1]
  ax.plot(edges[:-1], cumulative_hist, '-', markersize = 4, color='green',  lw=2, label="All") #linestyle="dotted"
  print "#all > 2 -->  ", len(np.where(d25>=2)[0])
  ax.annotate(r'$1246$',(2.38,2285), fontsize=12) 
  
 
  d25=[]
  for i in range(len(all_pgc)):
      if all_d25[i]<30 and all_survey[i] == 0:   # sdss
          d25.append(all_d25[i])
  d25=np.asarray(d25)
  print len(d25)

  hist, bin_edges = np.histogram(d25, bins = edges)
  hist = hist[::-1]
  cumulative_hist = np.cumsum(hist)
  cumulative_hist = cumulative_hist[::-1]
  ax.plot(edges[:-1], cumulative_hist, '-', markersize = 4, color='blue',  lw=2, label="SDSS") #linestyle="dotted"  
 
 
  d25=[]
  for i in range(len(all_pgc)):
      if all_d25[i]<30 and all_survey[i] == 1:  # pan-starrs
          d25.append(all_d25[i])
  d25=np.asarray(d25)
  print len(d25)

  hist, bin_edges = np.histogram(d25, bins = edges)
  hist = hist[::-1]
  cumulative_hist = np.cumsum(hist)
  cumulative_hist = cumulative_hist[::-1]
  ax.plot(edges[:-1], cumulative_hist, '-', markersize = 4, color='orange',  lw=2, label="Pan-STARRS") #linestyle="dotted" 
   
  print "#sdss > 2 -->  ", len(np.where(d25>=2)[0])
  ax.annotate(r'$372$',(2.38,169), fontsize=12)
  ax.annotate(r'$2 arcmin$',(1.88,0.13), fontsize=12)
  
  
  ax.annotate('2 arcmin',(2.30,1.25), fontsize=12, rotation=90)
  
   
   
  ax.plot([2,2],[0,2E4], ':', color='black')
  
  plt.xscale('log')
  plt.yscale('log')
  plt.xlim(20,0.4)
  plt.ylim(0.1,2E4)

  ax.set_xlabel('Diameter at B 25mag / as'+r'$^2$', fontsize=14)
  ax.set_ylabel('# of galaxies', fontsize=14)
  ax.legend( loc=2 )
  
  plt.show()
  
  
  
  
  
  



