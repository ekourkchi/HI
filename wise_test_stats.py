
#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 

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
##########################################


inFile  = 'augment/EDD_distance_cf4_v15.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  
QA_sdss = table['QA_sdss']  
QA_wise = table['QA_wise']  


t = 0
s = 0
w = 0
a = 0 
p = 0 
for i in range(len(pgc)):       
    
    
    if QA_sdss[i]==1 and QA_wise[i]==1:
        a+=1    
    
    if QA_sdss[i]==0 and QA_wise[i]==0:
        p+=1
        print "Warning: pgc", pgc[i]
      
    
    if QA_sdss[i]==1 or QA_wise[i]==1:
        t+=1
     
    if QA_sdss[i]==1:
        s+=1
        
    if QA_wise[i]==1:
        w+=1        
   
print 'Total qa: ', t
print 'SDSS  qa: ', s 
print 'WISE  qa: ', w
print 'Both  qa: ', a
print 'No    qa: ', p
   
########################################################################

