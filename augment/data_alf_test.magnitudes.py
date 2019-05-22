#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import os.path
import subprocess
import glob
from astropy.table import Table, Column 
import pyfits
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

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
    pgc_ID = pgc[3:len(pgc)]
    pgc_lst.append(int(pgc_ID))
    ra_lst.append(float(columns[1]))
  
  return pgc_lst, ra_lst

##########################################
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
# extract amgnitude from a file
def get_mag(filename):
    
          with open(filename) as f:
            counter = 1
            for line in f:
              if counter == 14:
                line_split = line.split(" ")
                not_void = 0 
                for thing in line_split:
                  if thing != '': not_void+=1
                  if not_void==2: 
                    break
                return np.float(thing)    
              counter+=1
              
 # extract amgnitude from a file
def get_semimajor(filename):
    
          with open(filename) as f:
            counter = 1
            for line in f:
              if counter == 14:
                line_split = line.split(" ")
                not_void = 0 
                for thing in line_split:
                  if thing != '': not_void+=1
                  if not_void==1: 
                    break
                return np.float(thing)    
              counter+=1             


def get_ellipse(filename):
          
          ra_cen = -1
          dec_cen = -1
          semimajor = -1
          semiminor = -1
          PA = -1
          with open(filename) as f:
            counter = 1
            for line in f:
              if counter == 14:
                line_split = line.split(" ")
                not_void = 0 
                set_param = False
                for thing in line_split:
                  if thing != '': 
                      not_void+=1
                      set_param = True
                  if not_void==1 and set_param: 
                      set_param = False
                      ra_cen=np.float(thing) 
                  if not_void==2 and set_param: 
                      dec_cen=np.float(thing) 
                      set_param = False
                  if not_void==3 and set_param: 
                      semimajor=np.float(thing) 
                      set_param = False
                  if not_void==4 and set_param: 
                      semiminor=np.float(thing)
                      set_param = False
                  if not_void==5 and set_param: 
                      PA=np.float(thing) 
                      break
                return ra_cen, dec_cen, semimajor, semiminor, PA
              counter+=1   

         
#################################
def get_quality(filename):
    
  line_no = 0
  seprator = ' '
  for line in open(filename, 'r'):
    columns = line.split(seprator)
    line_no+=1
    if len(columns) >= 2 and line_no==40:
	  key  = columns[0]
	  j = 1
	  while columns[j] == '' or columns[j] == '=': j+=1
	  return int(columns[j])
  return -1

#################################

db_root = '/home/ehsan/db_esn/'
  
filters = ['g','r','i']


aux_dir = '../New_era/'
data_tst = aux_dir + 'data_alf_test.glga'

data_ps  = aux_dir + 'PStesters_sdss.glga'
data_21  = aux_dir + 'data_set_21.glga'
data_41  = aux_dir + 'data_set_41.glga'
data_pl1 = aux_dir + 'pilot_01.glga' 
data_pl2 = aux_dir + 'pilot_02.glga'
data_pl3 = aux_dir + 'pilot_03.glga'

data_tst_pgc,  data_ra  = read_glga(data_tst)

#data_ps_pgc,  tmp = read_glga(data_ps)
#data_21_lst,  tmp = read_glga(data_21)
#data_41_lst,  tmp = read_glga(data_41)
#data_pl1_lst, tmp = read_glga(data_pl1)
#data_pl2_lst, tmp = read_glga(data_pl2)
#data_pl3_lst, tmp = read_glga(data_pl3)


N = 10
N = len(data_tst_pgc)
mags = np.zeros([N, 3])     # g r i 
a_smi = np.zeros([N, 3])    # g r i (asymptotic semi-major axis)
qual = np.zeros([N])        # Quality of photometry
ra = np.zeros([N])          # R.A. of the object
ellipse = np.zeros([N,5])   # ra,dec, semimajor,semiminor, PA  (ellipse parameter, chosen by the user)
src = []                    # source of the photometry, i.e. which set this data is coming from

for i in range(N):
  
  pgc_number = data_tst_pgc[i]
  pgc_id = 'pgc'+str(pgc_number)
  db_id = ra_db(data_ra[i])
  ra[i] = data_ra[i]
  
  #if pgc_number in data_21_lst: 
      #db_root='/home/ehsan/db_esn/'+'/DONE_DATA/data_set_21/'
      #src.append('data_set_21')
  #elif pgc_number in data_41_lst: 
      #db_root='/home/ehsan/db_esn/'+'/DONE_DATA/data_set_41/'
      #src.append('data_set_41')
  #elif pgc_number in data_pl3_lst: 
      #db_root='/home/ehsan/db_esn/'+'/DONE_DATA/data_pilot_03/'
      #src.append('data_pilot_03')
  #elif pgc_number in data_pl1_lst: 
      #db_root='/home/ehsan/db_esn/'+'/DONE_DATA/data_pilot_01/'
      #src.append('data_pilot_01')
  #elif pgc_number in data_pl2_lst: 
      #db_root='/home/ehsan/db_esn/'+'/DONE_DATA/data_pilot_02/'
      #src.append('data_pilot_02')
  #elif pgc_number in data_ps_pgc: 
      #db_root='/home/ehsan/db_esn/'+'/data_main/'
      #src.append('data_main')
  #else: 
      #db_root = ''
      #src.append('NULL')
  
  db_root = '/home/ehsan/db_esn/data_alf_test/'
  if db_root!='':
      for p in range(3):
        
        filter = filters[p]
        photometry =  db_root+db_id+'/photometry/'+pgc_id+'_'+filter+'_asymptotic.dat'
        ellipsefile = db_root+db_id+'/photometry/'+pgc_id+'_'+filter+'_ellipsepar.dat'
        if os.path.exists(photometry):
            mags[i][p] = get_mag(photometry)
            qa_txt = db_root+db_id+'/sdss/fits/'+pgc_id+'_qa.txt'
            qual[i] = get_quality(qa_txt)
            
            a_smi[i][p] = get_semimajor(photometry)
            
            ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse(ellipsefile)
            ellipse[i][0] = ra_cen
            ellipse[i][1] = dec_cen
            ellipse[i][2] = semimajor
            ellipse[i][3] = semiminor
            ellipse[i][4] = PA
            
            
      #print ['cp', '-f', db_root+db_id+'/aux/'+pgc_id+'*', '/home/ehsan/db_esn/data/'+db_id+'/aux/.']
      #subprocess.call(['cp', '-f', db_root+db_id+'/aux/'+pgc_id+'_sdss_pointsrc.dat', '/home/ehsan/db_esn/data/'+db_id+'/aux/.'])
      #subprocess.call(['cp', '-f', db_root+db_id+'/aux/'+pgc_id+'_sdss_roi.dat', '/home/ehsan/db_esn/data/'+db_id+'/aux/.'])
      #subprocess.call(['cp', '-f', db_root+db_id+'/aux/'+pgc_id+'_ellipse.dat', '/home/ehsan/db_esn/data/'+db_id+'/aux/.'])
            
            
#print 'pgc ra dec a b pa g r i a_g a_r a_i qual ra_db src'
print 'pgc g r i qual'
for i in range(N):
    #print data_tst_pgc[i], ellipse[i][0], ellipse[i][1], ellipse[i][2], ellipse[i][3], ellipse[i][4], mags[i][0], mags[i][1], mags[i][2], a_smi[i][0], a_smi[i][1], a_smi[i][2], qual[i], ra[i], src[i]
    print data_tst_pgc[i], mags[i][0], mags[i][1], mags[i][2], qual[i]




                       
                       














