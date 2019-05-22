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

inFile  = '../augment/EDD_distance_cf4_v11.csv'
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


inFile  = 'all.9060.csv'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc1     = table['PGC']

inFile  = 'all.EDDv10.PS.3237.csv'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc2     = table['PGC']


##################################################

p = 0 
for i in range(len(pgc)):
    
    #if pgc[i] in pgc_TFcalibrators or pgc[i] in pgc_TF_arecibo:
    if not pgc[i] in pgc1 and not pgc[i] in pgc2:
        
        if dec[i] > -30: # and sdss[i]==0:
            
            d25gal = d25[i]
            if d25gal<0.1 or np.isnan(d25gal):
                d25gal = 0.5
            if np.isnan(PA[i]):
                PA[i] = 0
            
            
            #print pgc[i], ra[i], dec[i], d25gal, PA[i]
            p+=1
            
    
print "New TF gals: #", p

            

    


