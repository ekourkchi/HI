#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 

import sqlcl
#################
###############################
def isInSDSS_DR12(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcl.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
  
###############################


inFile = 'All_LEDA_EDD.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_leda    = table['pgc']
ra_leda     = table['al2000']
ra_leda *= 15.
dec_leda    = table['de2000']
l_leda      = table['l2']
b_leda      = table['b2']
sgl_leda    = table['sgl']
sgb_leda    = table['sgb']
logd25_leda = table['logd25']
logr25_leda = table['logr25']
pa_leda     = table['pa']
ty_leda     = table['t']
type_leda   = table['type']

##################################################

inFile  = 'EDD_distance_cf4_v04.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  
sdss    = table['sdss']  
d25     = table['d25']
b_a     = table['b_a']
PA      = table['pa']
Ty      = table['ty']  
QA_wise = table['QA_wise']  
##################################################

inFile = 'TFcalibrators.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_TFcalibrators    = table['PGC']

p = 0 
for i in range(len(pgc_TFcalibrators)):
    
    new_pgc = pgc_TFcalibrators[i]
    if not new_pgc in pgc:
        for j in range(len(pgc_leda)):
            if pgc_leda[j] == new_pgc:
              #if isInSDSS_DR12(ra_leda[j], dec_leda[j]) == 1:
              
                 name = 'pgc'+str(new_pgc)
                 d25 = 0.1*(10**logd25_leda[j])
                 b_a = 1./(10**logr25_leda[j])
                 print name, ra_leda[j], dec_leda[j], d25, d25*b_a, pa_leda[j], ty_leda[j]
                 p+=1


#for i in range(len(pgc)):
    
    #if pgc[i] in pgc_TFcalibrators and QA_wise[i]==0:
        #name = 'pgc'+str(pgc[i])
        #try:
           #print name, ra[i], dec[i], d25[i], d25[i]*b_a[i], PA[i], Ty[i]
        #except:
           #print '[Warning]', name
            
        #p+=1
    
print "New TF gals: #", p

            

    


