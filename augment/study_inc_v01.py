#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 




##################################################
inFile = 'TFcalibrators.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_TFcalibrators    = table['PGC']
##################################################
inFile = 'TFcalibrators_Arecibo.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_TF_arecibo    = table['PGC']
RADE_TF_arecibo   = table['RADE']
TY_TF_arecibo     = table['T']
logr25_TF_arecibo = table['logr25']
Glon_TF_arecibo = table['Glon']
Glat_TF_arecibo = table['Glat']
SGL_TF_arecibo = table['SGL']
SGB_TF_arecibo = table['SGB']
b_a_TF_arecibo = 1./(10**logr25_TF_arecibo)



########################################################### Begin
inFile   = 'EDD_distance_cf4_v21.csv'
table    = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc      = table['pgc']
inc      = table['inc']
inc_e    = table['inc_e']
inc_flg  = table['inc_flg']
inc_n    = table['inc_n']
inc_note = table['inc_note']
face_on  = table['fon']

Sqlt = table['Sqlt']
Wqlt = table['Wqlt']
############################################################

n = 0
#for i in range(len(pgc)):
    
    #bol = False
    #if inc_flg[i]==0:
        
        #if inc_n[i]<2: bol=True
        #if inc[i]>=89 and inc_e[i]>1: bol=True
        #if inc[i]>=85 and inc_e[i]>2: bol=True
        #if inc[i]>=69 and inc_e[i]>3: bol=True
        #if inc[i]>=50 and inc_e[i]>4: bol=True
        #if inc[i]<50  and inc_e[i]>5: bol=True
        
        
        ##if pgc[i] in pgc_TFcalibrators:
            
        #if not bol: 
            

                
                #if Sqlt[i]>=3 or Wqlt[i]>=3: 
                   #if inc[i]>60: 
                       #n+=1
                       ##print  pgc[i]
                       #print str(pgc[i])+', '+str(inc[i])+', '+str(inc_e[i])+', '+str(inc_n[i])
        


for i in range(len(pgc)):
    
    fon = " ".join(face_on[i].split())
    if (fon == 'F' or (inc_flg[i]==1 and 'face_on' in inc_note[i])) and Sqlt[i]>4 and Wqlt[i]>4: 
        print pgc[i], Sqlt[i], Wqlt[i]
        n+=1





print n
