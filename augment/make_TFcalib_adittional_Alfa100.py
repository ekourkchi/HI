#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
from kapteyn import wcs

import sqlcl
#################

###############################

def cordiante_parser(ra_dec):
  
  # J2000
  # example: 004244.4+411608.0
  while ra_dec[0] == ' ': ra_dec = ra_dec[1:]

  ra_h = ra_dec[0:2]
  ra_m = ra_dec[2:4]
  ra_s = ra_dec[4:8]

  ra_deg = 15.*(float(ra_h)+float(ra_m)/60.+float(ra_s)/3600.)


  dec_d = ra_dec[8:11]
  dec_m = ra_dec[11:13]
  dec_s = ra_dec[13:17]

  s = np.sign(float(dec_d))

  if s == 0 and ra_dec[8] == '-':
    s = -1.
  elif s == 0 and ra_dec[8] == '+':
    s = 1.


  dec_deg = s*(np.abs(float(dec_d))+float(dec_m)/60.+float(dec_s)/3600.)

  return ra_deg, dec_deg


###############################
def isInSDSS_DR12(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcl.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
  
###############################


#inFile = 'All_LEDA_EDD.csv'
#table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#pgc_leda    = table['pgc']
#ra_leda     = table['al2000']
#ra_leda *= 15.
#dec_leda    = table['de2000']
#l_leda      = table['l2']
#b_leda      = table['b2']
#sgl_leda    = table['sgl']
#sgb_leda    = table['sgb']
#logd25_leda = table['logd25']
#d25_leda = 0.1*(10**logd25_leda)
#logr25_leda = table['logr25']
#b_a_leda = 1./(10**logr25_leda)
#pa_leda     = table['pa']
#ty_leda     = table['t']
#type_leda   = table['type']

##################################################

#inFile  = 'EDD_distance_cf4_v10.csv'
#table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
#pgc     = table['pgc']
#ra      = table['ra']
#dec     = table['dec']  
#sdss    = table['sdss']  
#d25     = table['d25']
#b_a     = table['b_a']
#PA      = table['pa']
#Ty      = table['ty']  
#QA_wise = table['QA_wise']  
##################################################
#inFile  = 'alfa100.csv'
#table   = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#pgc_a100     = table['PGC']
#w100_a100    = table['W100']
#logr25_a100  = table['lgR25']
#logd25_a100 = table['lgD25']
#d25_a100 = 0.1*(10**logd25_a100)
#snr_a100     = table['SNR']  
#T_a100       = table['T']
#Inc_a100     = table['Inc']
#l_a100       = table['l']
#b_a100       = table['b']
#b_a_a100 = 1./(10**logr25_a100)
##################################################




inFile = 'wise_all.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
ID_all  = table['ID']
PGC_all = table['PGC']


#p = 0 
#for i in range(len(pgc_a100)):
    
    #new_pgc = pgc_a100[i]
    
    #if not new_pgc in pgc:
        
        #Select = True
        #if not np.isnan(b_a_a100[i]) and (b_a_a100[i]>0.5 or logr25_a100[i]==0): Select=False
        #if not np.isnan(Inc_a100[i]) and (Inc_a100[i]>60 or Inc_a100[i]==0): Select=True
        #if np.isnan(Inc_a100[i]): Select=True
        
        
        #if not np.isnan(snr_a100[i]) and snr_a100[i]<5: Select=False
        #if not np.isnan(T_a100[i])   and T_a100[i]!=0 and T_a100[i]<1: Select=False
        
        
        #if Select:    
            
          #tran = wcs.Transformation("galactic j2000 j2000", "equatorial")
          #RA, DEC = tran((l_a100[i],b_a100[i]))
          #if isInSDSS_DR12(RA, DEC) == 1: 
              #sdss=1 
          #else: 
              #sdss=0
          
          #pag  = 45.
          #i_lst = np.where(new_pgc == pgc_leda)[0]
          #if not np.isnan(pa_leda[i_lst]):
            #pag = pa_leda[i_lst][0] 
           
          
             
          #print new_pgc, RA, DEC, l_a100[i], b_a100[i], d25_a100[i], d25_a100[i]*b_a_a100[i], pag, T_a100[i], sdss
          #p+=1




inFile = 'alfa100.csv.selected'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_sel   = table['pgc']
ra_sel    = table['ra']
dec_sel   = table['dec'] 
gl_sel    = table['gl']
gb_sel    = table['gb']
d25_sel   = table['d25']
b_sel     = table['b']
pa_sel    = table['pa']
ty_sel    = table['T']  
sdss_sel  = table['sdss']


p=0
for i in range(len(pgc_sel)):
    
    if sdss_sel[i]==0:
        name = 'pgc'+str(pgc_sel[i])
        
        ### for WISE
        if sdss_sel[i] in PGC_all:
          i_lst = np.where(sdss_sel[i] == PGC_all)
          name = ID_all[i_lst][0]
        
        print name, ra_sel[i], dec_sel[i], d25_sel[i], b_sel[i], pa_sel[i], ty_sel[i]
        p+=1
        
    
    


    
print "New TF gals: #", p

            

    


