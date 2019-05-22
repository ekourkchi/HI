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
#################

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
  
  return([pgc_leda, ra_leda, dec_leda, l_leda, b_leda, sgl_leda, sgb_leda, logd25_leda, logr25_leda, pa_leda, ty_leda, type_leda])
  
  #return leda

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
d25_leda = 0.1*(10**logd25_leda)
logr25_leda = table['logr25']
b_a_leda = 1./(10**logr25_leda)
pa_leda     = table['pa']
ty_leda     = table['t']
type_leda   = table['type']

##################################################
inFile  = 'EDD_distance_cf4_v21.csv'
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
QA_sdss = table['QA_sdss'] 
##################################################
inFile = 'output_1_Results_alexandra.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
id_lexi    = table['ID']

##################################################




#for i in range(len(id_lexi)):
    
    #pgc_lexi = int(id_lexi[i][3:10])
    #if not pgc_lexi in pgc:
        #name = 'pgc'+str(pgc_lexi)
        
        #print name

p = 0
q = 0

for i in range(len(id_lexi)):
    
    pgc_lexi = int(id_lexi[i][3:10])
    if not pgc_lexi in pgc:
        
        
        d25g = 0.2
        b_ag = 1.
        pag  = 45.
 
        
        if pgc_lexi in pgc_leda: 
            
            p+=1
            
            i_lst = np.where(pgc_lexi == pgc_leda)[0]
            
            rag = ra_leda[i_lst][0] 
            decg = dec_leda[i_lst][0] 

            
            if not  np.isnan(d25_leda[i_lst]):
                d25g = d25_leda[i_lst][0] 
            if not  np.isnan(pa_leda[i_lst]):
                pag = pa_leda[i_lst][0]              
            if not  np.isnan(ty_leda[i_lst]):
                tyg = ty_leda[i_lst][0] 
            if not  np.isnan(b_a_leda[i_lst]):
                b_ag = b_a_leda[i_lst][0] 
                

        else:
            q+=1
            leda_lexi =  query_leda_lyon(pgc_lexi)
            rag  = leda_lexi[1]
            decg = leda_lexi[2]
            d25g = 0.1*(10**leda_lexi[7])
            b_ag = 1./(10**leda_lexi[8])
            pag  = leda_lexi[9]
            tyg  = leda_lexi[11]

        if True: # isInSDSS_DR12(rag, decg) == 1:
            name = 'pgc'+str(pgc_lexi)
            #print name, rag, decg, d25g, d25g*b_ag, pag, tyg
            print str(pgc_lexi)+', '+str(rag)+', '+str(decg)+', '+str(d25g)+', '+str(pag)


#print p, q


#print query_leda_lyon(1751)


#for j in range(len(pgc_leda)):
     #if pgc_leda[j] == 1751:
                
                #print
                #print 'pgc_leda: ', pgc_leda[j]
                #print 'ra_leda: ', ra_leda[j]
                #print 'dec_leda: ', dec_leda[j]
                #print 'l_leda: ', l_leda[j]
                #print 'b_leda: ', b_leda[j]
                #print 'sgl_leda: ', sgl_leda[j]
                #print 'sgb_leda: ', sgb_leda[j]                
                #print 'logd25_leda: ', logd25_leda[j]                
                #print 'logr25_leda: ', logr25_leda[j]
                #print 'pa_leda: ', pa_leda[j]                
                #print 'ty_leda: ', ty_leda[j]
                #print 'type_leda: ', type_leda[j]
                #print
                
                #break







