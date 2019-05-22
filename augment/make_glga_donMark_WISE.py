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
#################################
def ra_db(ra):   # returns a string
  
     ra_id = str(int(np.floor(ra)))
     if ra < 10:
       ra_id = '00'+ra_id+'D'
     elif ra < 100:
       ra_id = '0'+ra_id+'D'
     else:
       ra_id = ra_id+'D'
  
     return ra_id
#################################
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

inFile   = 'EDD_distance_cf4_v15.csv'
table    = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc      = table['pgc']
ra       = table['ra']
dec      = table['dec']  
sdss     = table['sdss']  
d25      = table['d25']
b_a      = table['b_a']
PA       = table['pa']
Ty       = table['ty']  
QA_wise  = table['QA_wise']  
Wquality = table['Wqlt'] 
##################################################





inFile = 'wise_all.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
ID_all  = table['ID']
PGC_all = table['PGC']

location_wise  = '/home/ehsan/db_esn/cf4_wise/data/'


p = 0

for i in range(len(pgc)):
    
    if QA_wise[i] ==1 and Wquality[i]==-1:
        galname = 'pgc'+str(pgc[i])
        radb = ra_db(ra[i])
        
        ### for WISE
        if pgc[i] in PGC_all:
          i_lst = np.where(pgc[i] == PGC_all)
          galname = ID_all[i_lst][0]
          
        
          qa_txt_wise = location_wise + radb + '/wise/fits/' + galname+'_qa.txt'
          if not os.path.exists(qa_txt_wise):
             galname = 'pgc'+str(pgc[i])
        else:
             galname = 'pgc'+str(pgc[i])
          
        
        
        print galname, ra[i], dec[i], d25[i], b_a[i]*d25[i], PA[i], Ty[i]
        p+=1
        
    
#print "All: ", p    




            

    


