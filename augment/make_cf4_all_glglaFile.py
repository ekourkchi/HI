#!/usr/bin/python
import sys
import os
import subprocess
import math
import numpy as np
###############################

inFile = 'wise_all.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
wise_name = table['ID']
wise_pgc  = table['PGC']
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

def QA_WISE_DONE(pgc, ra):
    
    global wise_name, wise_pgc
    
    databse = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/'+'/cf4_wise/data/'
    
    if pgc in wise_pgc:
        i_lst = np.where(pgc == wise_pgc)
        name = wise_name[i_lst][0] 
        if os.path.exists(databse+ra_db(ra)+'/wise/fits/'+name+'_qa.txt'):
            return name
    
    name = 'pgc'+str(pgc)
    if os.path.exists(databse+ra_db(ra)+'/wise/fits/'+name+'_qa.txt'):
        return name
        
    return name    

###############################

inFile  = 'EDD_distance_cf4_v24.csv'
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



p = 0 
warnings = 0 
for i in range(len(pgc)):
    
    if QA_sdss[i]==1:
        name = 'pgc'+str(pgc[i])            ## activate when SDSS
        ##name = QA_WISE_DONE(pgc[i], ra[i])   ## activate when WISE
        try:
           print name, ra[i], dec[i], d25[i], d25[i]*b_a[i], PA[i], Ty[i]
        except:
           warnings+=1
            
        p+=1
    
print "gals: #", p, warnings

         #python make_cf4_all_glglaFile.py > cf4_wise_all.glga   
         #python make_cf4_all_glglaFile.py > cf4_sdss_all.glga

    


