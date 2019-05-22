#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import pyfits

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

#################
def QA_WISE_DONE(pgc, ra):
    
    global wise_name, wise_pgc
    
    databse = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/'+'/cf4_wise/data/'
    
    if pgc in wise_pgc:
        i_lst = np.where(pgc == wise_pgc)
        name = wise_name[i_lst][0] 
        if os.path.exists(databse+ra_db(ra)+'/wise/fits/'+name+'_qa.txt'):
            return True
    
    name = 'pgc'+str(pgc)
    if os.path.exists(databse+ra_db(ra)+'/wise/fits/'+name+'_qa.txt'):
         return True
        
    return False    
     
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
###############################

### For a given photometry file, this returns the magnitude value
def get_mag_f(photometry):
    if os.path.exists(photometry):
      with open(photometry) as f:
	counter = 1
	for line in f:
	  if line.split(" ")[0]!= '#' and line.split(" ")[0]!='#\n':
	    line_split = line.split(" ")
	    not_void = 0 
	    for thing in line_split:
	      if thing != '': 
                  not_void+=1
                  set_param = True
	      if not_void==2: 
		break
	    return np.float(thing)
	  counter+=1
	  
	  
def get_mag(photometry):
    
    mag = get_mag_f(photometry)
    
    if mag!=None:
        return mag
    else:
        return -1000
###############################
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
location = '/home/ehsan/db_esn/cf4_wise/data/'

inFile  = 'EDD_Wise_Photometry.csv'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc     = table['PGC']
W1      = table['W1']
ra      = table['RAJ']

ii=0
j=0
k=0

if True:

        for i in range(len(pgc)):
            
          #if pgc[i]==30819:
            
            found = False
            if QA_WISE_DONE(pgc[i], ra[i]):
                    found = True
                    radb = ra_db(ra[i])
                    if pgc[i] in wise_pgc:
                        i_lst = np.where(wise_pgc == pgc[i])
                        galname = wise_name[i_lst][0]
                        qa_txt = location + radb + '/wise/fits/' + galname+'_qa.txt'
                    else:
                        galname = 'pgc'+str(pgc[i])
                        qa_txt = location + radb + '/wise/fits/' + galname+'_qa.txt'
                        
                    if not os.path.exists(qa_txt):    
                        galname = 'pgc'+str(pgc[i])
                        qa_txt = location + radb + '/wise/fits/' + galname+'_qa.txt'
                    
                    if not os.path.exists(qa_txt):
                        found = False
                    

            #print found
            #print galname
            if not found:
                continue
            
            photometry =  location + radb +'/photometry/'+galname+'_w1_asymptotic.dat'
            if os.path.exists(photometry):
                
                #print " There it is    " , photometry
                
                ii+=1
                
                w1       = get_mag(photometry)
                quality  = get_quality(qa_txt)
                
                #print w1, quality
                
                if quality>-1:
                    
                  j+=1  
                    
                  delta = (w1-W1[i])  
                  if delta > 0.05:
                     print pgc[i], w1, W1[i], delta, quality
                     #print photometry
                     k+=1



print ii,j,k



















