
#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 

##########################################

def read_glga_wise(filename):
  
  name_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    name_ID = columns[0]
    name_lst.append(name_ID)
  
  return name_lst 

#################################


inFile  = 'augment/EDD_distance_cf4_v04.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  
QA_sdss = table['QA_sdss']  
QA_wise = table['QA_wise']  
########################################################################
inFile = 'augment/wise_all.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
wise_name = table['ID']
wise_pgc  = table['PGC']


WISE_QA_done = []
datasets = ['wise_qa_4.glga'] 
for dataset in datasets:
     WISE_QA_done += read_glga_wise('New_era/'+dataset)
     
     
########################################################################

#for i in range(len(WISE_QA_done)):
    #name= WISE_QA_done[i]
    #if name in wise_name:
        #i_lst = np.where(wise_name == name)
        #WISE_QA_done[i] = int(wise_pgc[i_lst][0])
        
#p = 0   
#for i in range(len(WISE_QA_done)):  
    #if WISE_QA_done[i] in pgc:
        #print WISE_QA_done[i]
        #p+=1

#print 'P: ', p
########################################################################
t = 0
s = 0
w = 0
a = 0 
for i in range(len(pgc)):       
    
    
    if QA_sdss[i]==1 and QA_wise[i]==1:
        a+=1    
    
    if QA_sdss[i]==1 or QA_wise[i]==1:
        t+=1
     
    if QA_sdss[i]==1:
        s+=1
        
    if QA_wise[i]==1:
        w+=1        
   
print 'T,S,W: ', t,s,w, a
   
########################################################################
