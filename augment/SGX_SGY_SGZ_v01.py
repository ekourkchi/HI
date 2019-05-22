#!/home/ehsan/Ureka/Ureka/variants/common/bin/python


import sys
import os
import random
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
from numpy import cos, sin
import astropy.coordinates as coord
import astropy.units as u
from math import *
from time import time
from astropy.io import ascii
from astropy.table import Table, Column 
import pyfits
import pylab as py
from itertools import chain
from astropy import coordinates as coord
from astropy import units as unit

# **************************************
# returns radian
def SGxy(l, b, Vls):
   
   H0 = 1.
   cl = cos(l*pi/180.)
   sl = sin(l*pi/180.)
   cb = cos(b*pi/180.)
   sb = sin(b*pi/180.)
   
   x = cl * cb
   y = sl * cb
   z = sb
   
   SGX = x*Vls/H0
   SGY = y*Vls/H0
   SGZ = z*Vls/H0
   
   return SGX, SGY, SGZ
 
# **************************************
# Vls[i] = Vh2Vls(gl[i], gb[i], Vhel3[i])
def Vh2Vls(el,b, Vh):
  
    alpha = pi / 180.
    cosb = cos(b*alpha)
    sinb = sin(b*alpha)
    cosl = cos(el*alpha)
    sinl = sin(el*alpha)
    
    vls = float(Vh)-26.*cosl*cosb+317.*sinl*cosb-8.*sinb

    
    return vls
################################################################# 
### (another "Vlg" has been given by Courteau and van den Bergh; another by Yahil et al.)
### The Vlg used in MKgroups is their own version. 
### The following function just works fine for MK-groups
def Vlg2Vh(el,b, Vlg):
  
    alpha = pi / 180.
    
    cosb = cos(b*alpha)
    sinb = sin(b*alpha)
    cosl = cos(el*alpha)
    sinl = sin(el*alpha)
    

    Vh=float(Vlg)+16.*cosl*cosb-315.*sinl*cosb+22.*sinb
    #vls = float(Vh)-26.*cosl*cosb+317.*sinl*cosb-8.*sinb
    
    
    return Vh

if __name__ == '__main__':

  #empty = []
  #myTable = Table()
  #myTable.add_column(Column(data=empty,name='SGX', dtype=np.dtype(int)))
  #myTable.add_column(Column(data=empty,name='SGY', dtype=np.dtype(int)))
  #myTable.add_column(Column(data=empty,name='SGZ', dtype=np.dtype(int)))

  
  TMRS = np.genfromtxt('2MRS.csv' , delimiter=',', filling_values="-100000", names=True, dtype=None )

  TMRS_pgc = TMRS['PGC']  # 2MRS
  TMRS_sgl = TMRS['SGL']
  TMRS_sgb = TMRS['SGB']
  TMRS_gl = TMRS['Glon']
  TMRS_gb = TMRS['Glat']
  TMRS_vh = TMRS['Vhel']
  
  CF2D = np.genfromtxt('CF3.csv' , delimiter=',', filling_values="-100000", names=True, dtype=None )

  CF2D_pgc = CF2D['PGC']  # CF2D
  CF2D_sgl = CF2D['SGL']
  CF2D_sgb = CF2D['SGB']
  CF2D_gl = CF2D['Glon']
  CF2D_gb = CF2D['Glat']
  CF2D_vls = CF2D['Vls']


  # PGC,l2,b2,sgl,sgb,Vhel1,Wm501
  HI = np.genfromtxt('HI.csv' , delimiter=',', filling_values="-100000", names=True, dtype=None )
    
  HI_pgc = HI['PGC']  # 2MRS
  HI_sgl = HI['sgl']
  HI_sgb = HI['sgb']
  HI_gl = HI['l2']
  HI_gb = HI['b2']
  HI_vh = HI['Vhel1']
  
  
  Alfalfa = np.genfromtxt('Alfa100_EDD.csv' , delimiter='|', filling_values="-100000", names=True, dtype=None )
  
  Alfalfa_pgc_ = Alfalfa['PGC'] 
  #Alfalfa_sgl = Alfalfa['SGL']
  #Alfalfa_sgb = Alfalfa['SGB']
  #Alfalfa_gl  = Alfalfa['Glon']
  #Alfalfa_gb  = Alfalfa['Glat']
  Alfalfa_vh_  = Alfalfa['Vhel']
  alfa = {}
  for i in range(len(Alfalfa_pgc_)): 
      alfa[Alfalfa_pgc_[i]] = Alfalfa_vh_[i]  
  
  
  inFile  = 'EDD_distance_cf4_v22.csv'
  table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)

  Alfalfa_pgc = table['pgc']
  Alfalfa_sgl = table['sgl']
  Alfalfa_sgb = table['sgb']
  Alfalfa_gl  = table['gl']
  Alfalfa_gb  = table['gb']
  Alfalfa_vh = Alfalfa_gb*0.
  N_esn = len(Alfalfa_pgc)
  inc = table['inc']
  
  
  inFile = 'All_LEDA_EDD.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
  pgc_leda    = table['pgc']
  vh_leda     = table['v']
  leda = {}
  for i in range(len(pgc_leda)): 
      leda[pgc_leda[i]] = vh_leda[i]
  
  for i in range(N_esn):
      try: 
          Alfalfa_vh[i] = leda[Alfalfa_pgc[i]]
      except: 
          Alfalfa_vh[i] = alfa[Alfalfa_pgc_[i]]
          
      
      #print Alfalfa_vh[i], inc[i]
  
  #############################
  
  
  
  #############################
  #############################

  pgcMax = max(max(TMRS_pgc), max(CF2D_pgc), max(HI_pgc), max(Alfalfa_pgc))
  print "MAx PGC:   ",  pgcMax
  
  i1 = 0
  n1 = len(TMRS_pgc)
  
  i2 = 0
  n2 = len(CF2D_pgc)
  
  i3 = 0
  n3 = len(HI_pgc)
  
  i4 = 0 
  n4 = len(Alfalfa_pgc)
  
  SGX = []
  SGY = []
  SGZ = []
  Vls0 = []
  
  SGX1 = []
  SGY1 = []
  SGZ1 = []
  Vls1 = []
  
  SGX2 = []
  SGY2 = []
  SGZ2 = []
  Vls2 = []
  
  SGX3 = []
  SGY3 = []
  SGZ3 = []
  Vls3 = []  
  
  for pg in range(1,pgcMax+10):
    
     color = 0
     
     # Background
     if i1<n1 and TMRS_pgc[i1] == pg:
       Vls = Vh2Vls(TMRS_gl[i1], TMRS_gb[i1], TMRS_vh[i1])
       if Vls>0: 
           sgx, sgy, sgz = SGxy(TMRS_sgl[i1], TMRS_sgb[i1], Vls)
           color = 1  # gray
       i1+=1


     if i3<n3 and HI_pgc[i3] == pg:
       Vls = Vh2Vls(HI_gl[i3], HI_gb[i3], HI_vh[i3])
       if Vls>0: 
           sgx, sgy, sgz = SGxy(HI_sgl[i3], HI_sgb[i3], Vls)
           color = 3  # blue
       i3+=1     
     
     # Foreground
     if i2<n2 and CF2D_pgc[i2] == pg:
       Vls = CF2D_vls[i2]
       if Vls>0: 
           sgx, sgy, sgz = SGxy(CF2D_sgl[i2], CF2D_sgb[i2], Vls)
           color = 2  # green
       i2+=1  
    
    
     if i4<n4 and Alfalfa_pgc[i4] == pg:
       Vls = Vh2Vls(Alfalfa_gl[i4], Alfalfa_gb[i4], Alfalfa_vh[i4])
       if Vls>0: 
           sgx, sgy, sgz = SGxy(Alfalfa_sgl[i4], Alfalfa_sgb[i4], Vls)
           color = 4  # red
       i4+=1       









    
     if color == 1: # and abs(sgz)<4000:
        SGX.append(sgx)
        SGY.append(sgy)
        SGZ.append(sgz)
        Vls0.append(Vls)
     elif color == 2: # and abs(sgz)<4000:
        SGX1.append(sgx)
        SGY1.append(sgy)
        SGZ1.append(sgz)
        Vls1.append(Vls)
     elif color == 3: # and abs(sgz)<4000:
        SGX2.append(sgx)
        SGY2.append(sgy)
        SGZ2.append(sgz)
        Vls2.append(Vls)
     elif color == 4: # and abs(sgz)<4000:
        SGX3.append(sgx)
        SGY3.append(sgy)
        SGZ3.append(sgz)
        Vls3.append(Vls)        
     
  print "HI needed to be measured:", len(SGX2)  
  print "CF3D:", len(SGX1)  


  #############################
  #############################
  #############################

  #for i in range(len(TMRS_pgc)):
     #Vls = Vh2Vls(TMRS_gl[i], TMRS_gb[i], TMRS_vh[i])
     #if Vls>0: 
        #sgx, sgy, sgz = SGxy(TMRS_sgl[i], TMRS_sgb[i], Vls)
        #SGX.append(sgx)
        #SGY.append(sgy)
        #SGZ.append(sgz)
  


  #############################

  #for i in range(len(CF2D_pgc)):
     #Vls = CF2D_vls[i]
     #if Vls>0: 
        #sgx, sgy, sgz = SGxy(CF2D_sgl[i], CF2D_sgb[i], Vls)
        #SGX1.append(sgx)
        #SGY1.append(sgy)
        #SGZ1.append(sgz)
        
  #############################

  #for i in range(len(HI_pgc)):
     #Vls = Vh2Vls(HI_gl[i], HI_gb[i], HI_vh[i])
     #if Vls>0: 
        #sgx, sgy, sgz = SGxy(HI_sgl[i], HI_sgb[i], Vls)
        #SGX2.append(sgx)
        #SGY2.append(sgy)
        #SGZ2.append(sgz)
               
    
  #############################
 
    


        #BOL = True
        #for j in range(len(CF2D_pgc)):
	  #if CF2D_pgc[j] == HI_pgc[i]:
	    #BOL = False         
	    #break
        #if BOL:
            #myTable.add_row([sgx, sgy, sgz])
  

  
    
  fig = plt.figure(figsize=(7, 7), dpi=100)

  ax = fig.add_axes([0.19, 0.19, 0.75,  0.75]) 
  ax.xaxis.set_major_locator(MultipleLocator(5000))
  ax.yaxis.set_major_locator(MultipleLocator(5000))
  #ax.xaxis.set_minor_locator(MultipleLocator(1))
  #ax.yaxis.set_minor_locator(MultipleLocator(1))  
  
  
  plt.minorticks_on()
  plt.tick_params(which='major', length=7, width=1.5)
  plt.tick_params(which='minor', length=4, color='#000033', width=1.0)     
  
  
  ## 2MRS
  plt.plot(SGX, SGY,'.', markersize = 1, color='#696969', alpha=0.3) 
  

  ##HI - BLUE
  #plt.plot(SGX2, SGY2,'.', markersize = 1, color='blue')    
  
  ##CF3D - Green
  plt.plot(SGX1, SGY1, '.', markersize = 1.1, color='green', alpha=0.3) 
  

  ##ALFALFA - red
  plt.plot(SGX3, SGY3, '.', markersize = 1.1, color='red', alpha=0.3) 
  
  limit = 15000
  plt.ylim(-1.*limit,limit)
  plt.xlim(-1.*limit,limit)
  plt.xlabel("SGX (km s"+r"$^{-1}$"+")", fontsize=20)
  plt.ylabel("SGY (km s"+r"$^{-1}$"+")", fontsize=20)
  plt.yticks(fontsize=14)
  plt.xticks(fontsize=14)
  
  
  #myTable1 = Table()
  #myTable1.add_column(Column(data=Vls1,name='Vls'))
  #myTable1.add_column(Column(data=SGX1,name='SGX'))
  #myTable1.add_column(Column(data=SGY1,name='SGY'))
  #myTable1.write('Vls.only.Cf2d.csv', format='ascii.fixed_width',delimiter=',', bookend=False) # CF2D
  
  
  #Vls2 = np.concatenate((Vls1, Vls2))
  #SGX2 = np.concatenate((SGX1, SGX2))
  #SGY2 = np.concatenate((SGY1, SGY2))
  #myTable2 = Table()
  #myTable2.add_column(Column(data=Vls2,name='Vls'))
  #myTable2.add_column(Column(data=SGX2,name='SGX'))
  #myTable2.add_column(Column(data=SGY2,name='SGY'))
  #myTable2.write('Vls.HI.and.Cf2d.csv', format='ascii.fixed_width',delimiter=',', bookend=False) # HI  
  
  
  
  plt.show()
  
  
   
  
  
  
  
  
  
  
  
  
  
  


