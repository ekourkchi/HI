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

inFile = 'augment/wise_all.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
wise_name = table['ID']
wise_pgc  = table['PGC']



def get_no_frame(fname):
    
    if os.path.exists(fname):
        hdulist = pyfits.open(fname)
        prihdr = hdulist[0].header
        return int(prihdr['NUMFRMS'])
    else:
        return 0


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
def QA_SDSS_DONE(pgc, ra):
    
    
    databse = '/home/ehsan/db_esn/'+'/cf4_sdss/data/'
    
    name = 'pgc'+str(pgc)
    if os.path.exists(databse+ra_db(ra)+'/sdss/fits/'+name+'_qa.txt'):
        return True
        
    return False   
#################
def QA_WISE_DONE(pgc, ra):
    
    global wise_name, wise_pgc
    
    databse = '/home/ehsan/db_esn/'+'/cf4_wise/data/'
    
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


	  





destination = '/media/ehsan/HOURI/wise_photometry/'

datasets  = []
locations = []

location = '/home/ehsan/db_esn/cf4_wise/data/'


inFile  = 'augment/EDD_distance_cf4_v24.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  

########################################################################
w1N=[]
w2N=[]
w3N=[]

############################################################


if True:


         

        for i in range(len(pgc)):
            
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
                    

            
            if not found:
                continue
            

            
            if os.path.exists(qa_txt):
            
                      
                        
                        photometry =  location + radb +'/photometry/'+galname+'_w1_asymptotic.dat'
                        if os.path.exists(photometry):
                            
                            gal_pgc = pgc[i]
                            
 
                            
                            fits_file = location + radb +'/wise/fits/'+galname+'_w1.fits.gz'
                            w1_frame = get_no_frame(fits_file)
                            fits_file = location + radb +'/wise/fits/'+galname+'_w2.fits.gz'
                            w2_frame = get_no_frame(fits_file)
                            fits_file = location + radb +'/wise/fits/'+galname+'_w3.fits.gz'
                            w3_frame = get_no_frame(fits_file)
                            
                            print gal_pgc,w1_frame,  w2_frame, w3_frame
                            w1N.append(w1_frame)
                            w2N.append(w2_frame)
                            w3N.append(w3_frame)
                            
print np.median(w1N),np.mean(w1N),np.std(w1N)
print np.median(w2N),np.mean(w2N),np.std(w2N)
print np.median(w3N),np.mean(w3N),np.std(w3N)
                            
                            
                            
                            
                            
                            
                            
 
