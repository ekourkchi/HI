#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 

#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.
##########################################



def read_glga(filename):
  
  pgc_lst = []
  ra_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    
    pgc = columns[0]
    pgc_lst.append(pgc)
    
    j = 1 
    while columns[j]=='' or columns[j]==' ': j+=1
    ra_lst.append(ra_db(float(columns[j])))
  
  return pgc_lst, ra_lst

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
#################################

def xcmd(cmd,verbose):

  if verbose: print '\n'+cmd

  tmp=os.popen(cmd)
  output=''
  for x in tmp: output+=x
  if 'abort' in output:
    failure=True
  else:
    failure=tmp.close()
  if False:
    print 'execution of %s failed' % cmd
    print 'error is as follows',output
    sys.exit()
  else:
    return output

#################################
###########################

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
###############################

if __name__=='__main__':
    
    
    databse = '~/db_esn/'+'/cf4_sdss/data/'
    
    destin = '~/db_esn/'+'/cf4_wise/data/'
    
    
    inFile  = 'wise_cf4_need_qa.csv'
    table   = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
    pgc      = table['pgc']
    name     = table['name']
    ra       = table['ra']
    dec      = table['dec']

    
    
    
    
    for i in range(len(pgc)):
        
        radb = ra_db(ra[i])
        pgcname = 'pgc'+str(pgc[i])
        
        
        fromm = databse+radb+'/aux/'+pgcname+'_ellipse.dat'
        too   = destin +radb+'/aux/'+name[i]+'_ellipse.dat'
        
        #print fromm
        #print too
        #print
                      
                
        
        
        cmd = "cp "+ fromm+' '+ too
        xcmd(cmd,True)           
    




