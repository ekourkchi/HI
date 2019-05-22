#!/usr/bin/python
import sys
import os
import subprocess
import math
import numpy as np
import sqlcl
#########################################
def read_glga_wise(filename):
  
  name_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    name_ID = columns[0]
    name_lst.append(name_ID)
  
  return name_lst 
##########################################

def read_glga(filename):
  
  pgc_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    pgc = columns[0]
    pgc_ID = pgc[3:len(pgc)]
    pgc_lst.append(int(pgc_ID))
  
  return pgc_lst 

##########################################
###############################
def isInSDSS_DR12(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcl.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
  
###############################
##########################################

inFile  = 'EDD_distance_cf4_v07.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  
sdss    = table['sdss']  
d25     = table['d25']
b_a     = table['b_a']
PA      = table['pa']
Ty      = table['ty']  
sdss    = table['sdss']
QA_sdss = table['QA_sdss']  
QA_wise = table['QA_wise']  







inFile  = 'wise_cf4_need_qa.csv'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_     = table['pgc']
name_    = table['name']

#for i in range(len(pgc_)):
    
    #gal = pgc_[i]
    #j = np.where(pgc == gal)
    #j = j[0][0]
    #print name_[i], ra[j], dec[j], d25[j], d25[j]*b_a[j], PA[j], Ty[j]



    
gal = 58411
j = np.where(pgc == gal)
j = j[0][0]
print 'pgc58411', ra[j], dec[j], d25[j], d25[j]*b_a[j], PA[j], Ty[j]






#inFile = 'TFcalibrators.csv'
#table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#pgc_TFcalibrators    = table['PGC']









#print " SSS DDD SSS SSS ..... "
#print 
##for i in range(len(pgc_TFcalibrators)):
    
    ##gal = pgc_TFcalibrators[i]
    ##j = np.where(pgc == gal)
    
#for j in range(len(pgc)):    
    #gal = pgc[j]
    #if QA_sdss[j] == 0 and sdss[j] == 1:
        #name = 'pgc'+str(gal)
        #print name, ra[j], dec[j], d25[j], d25[j]*b_a[j], PA[j], Ty[j]
    
    #if not gal in pgc:
        #print "NA pgc:", gal


#print " WWWW IIII SSSS EEEE ..... "
#print 
#for i in range(len(pgc_TFcalibrators)):
    
    #gal = pgc_TFcalibrators[i]
    #j = np.where(pgc == gal)
    #if QA_wise[j] == 0:
        #name = 'pgc'+str(gal)
        #print name, ra[i], dec[i], d25[i], d25[i]*b_a[i], PA[i], Ty[i]    
    
    
    






