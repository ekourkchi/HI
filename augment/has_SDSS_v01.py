#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import urllib2

import sqlcl
import sqlcldr7

#################
###############################

def cordiante_parser(ra_dec):
  
  ra_dec = ra_dec[1:]
  # J2000
  # example: 004244.4+411608.0
  while ra_dec[0] == ' ' or ra_dec[0] == 'J': 
      ra_dec = ra_dec[1:]
  
  ra_h = ra_dec[0:2]
  ra_m = ra_dec[2:4]
  ra_s = ra_dec[4:8]
  ra_hex = ra_h+":"+ra_m+":"+ra_s
  
  ra_deg = 15.*(float(ra_h)+float(ra_m)/60.+float(ra_s)/3600.)


  dec_d = ra_dec[8:11]
  dec_m = ra_dec[11:13]
  dec_s = ra_dec[13:17]
  dec_hex = dec_d+":"+dec_m+":"+dec_s
  s = np.sign(float(dec_d))

  if s == 0 and ra_dec[8] == '-':
    s = -1.
  elif s == 0 and ra_dec[8] == '+':
    s = 1.


  dec_deg = s*(np.abs(float(dec_d))+float(dec_m)/60.+float(dec_s)/3600.)

  return ra_hex, dec_hex, ra_deg, dec_deg


def hms_dms(ra_hex, dec_hex):
  
  ra_h = np.int(ra_hex[0:2])
  ra_m = np.int(ra_hex[3:5])
  ra_s = np.float(ra_hex[6:10])
  
  dec_d = np.int(dec_hex[0:3])
  dec_m = np.int(dec_hex[4:6])
  dec_s = np.float(dec_hex[7:11])
  
  return [ra_h, ra_m, ra_s, dec_d, dec_m, dec_s]
  
  

###############################
#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.


def exclude(pgc, pgc_ex):
  
  pgc = np.asarray(pgc)
  pgc_ex = np.asarray(pgc_ex)
  pgc_ex = np.sort(pgc_ex)
  
  n0 = len(pgc)
  n_ex = len(pgc_ex)
  
  indices = np.arange(n0)
  ind_srot = np.argsort(pgc)
  indices = indices[ind_srot]
  pgc = pgc[ind_srot]
  
  j = 0 
  for i in range(n_ex):
    while(pgc[j] < pgc_ex[i] and pgc[j]  < n0):
      j+=1
    if pgc[j] == pgc_ex[i]:
      indices[j] = -1   # will be excluded
      j+=1
  
  return (indices[np.where(indices > -1)],)
  

#################
#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.


def intersect(pgc, pgc_ex):
  
  pgc = np.asarray(pgc)
  pgc_ex = np.asarray(pgc_ex)
  pgc_ex = np.sort(pgc_ex)
  
  n0 = len(pgc)
  n_ex = len(pgc_ex)
  
  indices = np.arange(n0)
  ind_srot = np.argsort(pgc)
  indices = indices[ind_srot]
  pgc = pgc[ind_srot]
  
  j = 0 
  common_indices = []
  for i in range(n_ex):
    while(pgc[j] < pgc_ex[i] and pgc[j]  < n0):
      j+=1
    if pgc[j] == pgc_ex[i]:
      common_indices.append(indices[j])   # will be kept (that's in the intersect region)
      j+=1
  
  indices = np.asarray(common_indices)
  return (indices,)
  

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

def isInSDSS_DR7(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcldr7.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0

###############################

def really_isInSDSS_DR12(ra, dec):
  querry = "SELECT TOP 10 p.fieldID FROM Field AS p WHERE "+str(dec)+" BETWEEN p.decMin AND p.decMAx AND "+str(ra)+"  BETWEEN p.raMin AND p.raMax"
  lines = sqlcl.query(querry).readlines()
  if len(lines) == 2: 
    return 0
  else: 
    return 1

###############################
def query_leda_lyon(pgc):

  leda = []
  query=""
  if True:
     query=query+"%20or%20pgc%3D"+str(pgc)
     if True:
         query=query[5:]
         url='http://leda.univ-lyon1.fr/leda/fullsqlmean.cgi?Query=select%20*%20where'+query
         result=urllib2.urlopen(url)
         for myline in result:
             if "<" in myline:
                 continue
             if myline=="":
                 continue

             elements=myline.replace(" ","").split("|")
             elements=[x if x!="-" else None for x in elements]

             if ("pgc" in elements[0]):
                 continue
             if (len(elements)<2):
                 continue
             elements.pop()
             if (elements):
               #print elements[:3]
               leda.append((elements))
         query=""
  
  pgc_leda    = None
  ra_leda     = None
  dec_leda    = None
  l_leda      = None
  b_leda      = None
  sgl_leda    = None
  sgb_leda    = None
  logd25_leda = None
  logr25_leda = None
  pa_leda     = None
  ty_leda     = None
  type_leda   = None 
  Vhel_leda   = None 
  
  if (leda):
    
    leda = leda[0]
    pgc_leda    = int(leda[0])
    ra_leda     = float(leda[5])*15.
    dec_leda    = float(leda[6])
    l_leda      = float(leda[7])
    b_leda      = float(leda[8])
    sgl_leda    = float(leda[9])
    sgb_leda    = float(leda[10])
    logd25_leda = float(leda[20])
    logr25_leda = float(leda[22])
    pa_leda     = float(leda[24])
    ty_leda     = float(leda[17])
    type_leda   = (leda[12])   
    Vhel_leda   = float(leda[52])    
  
  return([pgc_leda, ra_leda, dec_leda, l_leda, b_leda, sgl_leda, sgb_leda, logd25_leda, logr25_leda, pa_leda, ty_leda, type_leda, Vhel_leda])
  
  #return leda

###############################
############################################################
inFile = 'All_LEDA_EDD.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=-1000000, names=True, dtype=None)
pgc_leda    = table['pgc']
ra_leda     = table['al2000']
ra_leda *= 15.
dec_leda    = table['de2000']
l_leda      = table['l2']
b_leda      = table['b2']
sgl_leda    = table['sgl']
sgb_leda    = table['sgb']
logd25_leda = table['logd25']
d25_leda = 0.1*(10**logd25_leda)
logr25_leda = table['logr25']
b_a_leda = 1./(10**logr25_leda)
pa_leda     = table['pa']
ty_leda     = table['t']
type_leda   = table['type']
LEDA_vhelio = table['v']
############################################################


# Main Program ....
###############################


#inFile = 'new_gals.txt'
#table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
#pgc_add    = table['PGC']

pgc_add = [30708]

N_galaxies = len(pgc_add)

pgc_ = []
ra_  = []
dec_ =[]


for i in range(N_galaxies):
    print i,' / ',N_galaxies
    try:
        
        if not pgc_add[i] in pgc_leda:
            leda_lexi =  query_leda_lyon(pgc_add[i])
            ra_.append(leda_lexi[1])
            dec_.append(leda_lexi[2])
            
        else:
            indx, = np.where(pgc_leda==pgc_add[i])
            ra_.append(ra_leda[indx][0])
            dec_.append(dec_leda[indx][0])
            #print pgc_add[i], ra_leda[indx][0], dec_leda[indx][0]
        
        pgc_.append(pgc_add[i])
    except:
        pass

#sys.exit()
##########################




for i in range(len(pgc_)):
  
  ra = ra_[i]
  dec = dec_[i]
  
  sdss_selected=0
  if isInSDSS_DR12(ra, dec) == 1:
    sdss_selected = 1
  elif really_isInSDSS_DR12(ra, dec) == 1:
    sdss_selected = 1

  print i+1, pgc_[i], ra, dec, sdss_selected





