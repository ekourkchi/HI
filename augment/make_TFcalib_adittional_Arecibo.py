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
#################################
def get_quality(filename, nline=40):
    
  line_no = 0
  seprator = ' '
  for line in open(filename, 'r'):
    columns = line.split(seprator)
    line_no+=1
    if len(columns) >= 2 and line_no==nline:
	  key  = columns[0]
	  j = 1
	  while columns[j] == '' or columns[j] == '=': j+=1
	  return int(columns[j])
  return -1

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

inFile  = 'EDD_distance_cf4_v11.csv'   ## 'EDD_distance_cf4_v09.csv'
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

inFile = 'TFcalibrators_Arecibo.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_TFcalibrators    = table['PGC']
RADE_TFcalibrators    = table['RADE']
TY_TFcalibrators    = table['T']
logr25_TFcalibrators = table['logr25']
b_a_TFcalibrators = 1./(10**logr25_TFcalibrators)

inFile = 'wise_all.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
ID_all  = table['ID']
PGC_all = table['PGC']

location_sdss  = '/home/ehsan/db_esn/cf4_sdss/data/'
location_wise  = '/home/ehsan/db_esn/cf4_wise/data/'


#p = 0 
#for i in range(len(pgc_TFcalibrators)):
    
    #new_pgc = pgc_TFcalibrators[i]
    #if not new_pgc in pgc:
        
        #rag, decg  = cordiante_parser(RADE_TFcalibrators[i])
        #d25g = 0.2
        #b_ag = b_a_TFcalibrators[i]
        #pag  = 45.
        #tyg  = TY_TFcalibrators[i]  
        
        #i_lst = np.where(new_pgc == pgc_leda)[0]
        #if not  np.isnan(d25_leda[i_lst]):
            #d25g = d25_leda[i_lst][0] 
        #if not  np.isnan(pa_leda[i_lst]):
            #pag = pa_leda[i_lst][0]              
        
        #if isInSDSS_DR12(rag, decg) == 1:
                 #name = 'pgc'+str(new_pgc)
                 #print name, rag, decg, d25g, d25g*b_ag, pag, tyg

        #p+=1








p = 0 

for i in range(len(pgc_TFcalibrators)):
    
    Getit = False
    if pgc_TFcalibrators[i] in pgc:  # already in catalog
        
        i_lst = np.where(pgc_TFcalibrators[i] == pgc)[0] 
        if QA_wise[i_lst] == 0:  # need WISE photometry
                Getit = True
                rag  = ra[i_lst][0] 
                decg = dec[i_lst][0] 
                d25g = d25[i_lst][0] 
                b_ag = b_a[i_lst][0] 
                pag  = PA[i_lst][0] 
                tyg  = Ty[i_lst][0] 
    
    
                pgcname = 'pgc'+str(pgc[i_lst][0])          
                radb    = ra_db(rag)
                qa_txt_sdss = location_sdss + radb + '/sdss/fits/' + pgcname+'_qa.txt'
                #print qa_txt_sdss
                if os.path.exists(qa_txt_sdss):
                    qa_txt  = qa_txt_sdss
                    quality     = get_quality(qa_txt)
                    disturbed   = get_quality(qa_txt, nline=41)
                    trail       = get_quality(qa_txt, nline=42)
                    not_spiral  = get_quality(qa_txt, nline=43)
                    face_on     = get_quality(qa_txt, nline=44)
                    faint       = get_quality(qa_txt, nline=45)
                    multiple    = get_quality(qa_txt, nline=19)
                    uncertain   = get_quality(qa_txt, nline=17)
                    if quality>=0 and quality<3: Getit=False
                    if uncertain==1: Getit=False
                    if multiple==1: Getit=False
                    if disturbed==1: Getit=False
                    if trail==1: Getit=False
                    if not_spiral==1: Getit=False
                    if face_on==1: Getit=False
        
                
    if Getit:    
            name = 'pgc'+str(pgc_TFcalibrators[i])
            if pgc_TFcalibrators[i] in PGC_all:
               i_lst = np.where(pgc_TFcalibrators[i] == PGC_all)   
               name = ID_all[i_lst][0]
            try:
               print name, rag, decg, d25g, d25g*b_ag, pag, tyg
            except:
               print '[Warning]', name
                
            p+=1
 
 
    
#print "New TF gals: #", p

            

    


