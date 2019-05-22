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
def extract_pgc(ID):
    
    return int(ID[3:10])
    
##########################################

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

##########################################
#################
def parseout_pgc(string):
    
    string = string[66:len(string)]
    
    i = 0
    
    try: 
      while string[i]!='<': 
         i+=1
    except:
      return None
    
    return string[0:i]
    
    

##########################################

inFile = 'EDD_distance_cf4_v02.csv'
table = np.genfromtxt( inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc2 = table['pgc']


inFile = 'EDD_distance_cf4_v03.csv'
table = np.genfromtxt( inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc3 = table['pgc']
sdss3 = table['sdss']

p = 0 
for i in range(len(pgc3)):
    
    if not pgc3[i] in pgc2:# and sdss3[i] == 1:
        p+=1
    
print p


#inFile = 'helene_nancy.csv'
#table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#ID = table['ID']


#inFile = 'nancy_pgc_dbl.csv'
#table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#pgc_helene = table['pgc_helene']
#pgc_orig   = table['pgc_orig']

#xcmd('rm leda_nancy.csv',True)
#xcmd("awk '(NR==1){print($0)}' HyperLeda.txt > leda_nancy.csv",True)

#j = 0 
#for i in range(len(ID)):
    
    ##if not extract_pgc(ID[i]) in pgc:
    
        #pgc_new = extract_pgc(ID[i])
        #if pgc_new in pgc_helene:
            #for i in range(len(pgc_helene)):
                #if pgc_new == pgc_helene[i]: break
            
            #print "[Warning]  ", pgc_new, pgc_orig[i]
            #pgc_new = pgc_orig[i]
            
            
        #if pgc_new>0:
           #cmd = 'more HyperLeda.txt | grep ,'+str(pgc_new)+',G  >> leda_nancy.csv'
           #xcmd(cmd,True)
           #j+=1


#print 'count: ', j
                           
                           
                         
#inFile = 'leda_nancy.csv'
#table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#pgc_nancy    = table['pgc']
#ra_nancy     = table['al2000']
#ra_nancy *= 15.
#dec_nancy    = table['de2000']
#l_nancy      = table['l2']
#b_nancy      = table['b2']
#sgl_nancy    = table['sgl']
#sgb_nancy    = table['sgb']
#logd25_nancy = table['logd25']
#logr25_nancy = table['logr25']
#pa_nancy     = table['pa']
#ty_nancy     = table['t']
#type_nancy   = table['type']

#print len(pgc_nancy)

#xcmd("rm nancy_pgc_dbl2.txt",False)
#for i in range(len(ID)):
    
    #if not extract_pgc(ID[i]) in pgc_nancy  and not extract_pgc(ID[i]) in pgc_helene :
        ##print extract_pgc(ID[i]), ID[i]
        
        #xcmd("wget 'http://leda.univ-lyon1.fr/ledacat.cgi?PGC"+str(extract_pgc(ID[i]))+"&ob=ra'",False)
        #string =  xcmd("more ledacat.cgi\?PGC"+str(extract_pgc(ID[i]))+"\&ob=ra | grep 'pgc</a>'",False)
        #xcmd("rm ledacat.cgi\?PGC"+str(extract_pgc(ID[i]))+"\&ob=ra",False)
        
         
        #xcmd("echo "+str(ID[i])+" "+str(extract_pgc(ID[i]))+" " +str(parseout_pgc(string))+" >> nancy_pgc_dbl2.txt",False)
        
        
        
#print  len(ID) , len(pgc_nancy)
        
        




