#!/usr/bin/python
import sys
import os.path
import glob
import numpy as np
from astropy.table import Table, Column 
import pyfits
from subprocess import Popen, PIPE

     #### python glga_work_make.py > glga_work_hall2012

def split_func(sex_file):
  
  output = Popen(["awk", "(NR>2){print($10\" \"$12\" \"$16\" \"$18\" \"$22)}", sex_file], stdout=PIPE)
  s = output.stdout.read()
  spl = s.split()
  RA = np.float(spl[0])
  DEC = np.float(spl[1])  
  ra = np.float(spl[2])
  rb = np.float(spl[3])
  pa = np.float(spl[4])
  
  Status = True
  if ra*rb*pa == 0: Status = False
  
  return Status, RA, DEC, ra, rb, pa
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
def intersect(pgc, pgc_ex):
  
  pgc = np.asarray(pgc)
  pgc_ex = np.asarray(pgc_ex)
  pgc_ex = np.sort(pgc_ex)
  
  n0 = len(pgc)
  n_ex = len(pgc_ex)
  
  indices = np.arange(n0)
  ind_srot = np.argsort(pgc)
  indices = indices[ind_srot]
  pgc = pgc[ind_srot]
  
  j = 0 
  common_indices = []
  for i in range(n_ex):
    while(pgc[j] < pgc_ex[i] and pgc[j]  < n0):
      j+=1
    if pgc[j] == pgc_ex[i]:
      common_indices.append(indices[j])   # will be kept (that's in the intersect region)
      j+=1
  
  indices = np.asarray(common_indices)
  return (indices,)
  

#################

inFile = 'brent_list/edd_HI_ba_T_9060.short.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc         = table['PGC']
d25         = table['d25']   # arcmin
Ty          = table['Ty']
PA          = table['PA']
b_a         = table['b_a']

#inFile = 'Hall_sdss/Hall.SDSS.EDDtable04Feb2016.txt'
#table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#pgc_ex      = table['PGC']


inFile = 'has_Hall.SDSS.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
ra_cor    = table['ra']
dec_cor   = table['dec']
sdss      = table['SDSS']
pgc_ex      = table['pgc']

all_indices = np.where(sdss == 1)
all_indices = all_indices[0]
pgc_ex = pgc_ex[all_indices]

ex_ind =  intersect(pgc, pgc_ex)

selected_pgc = pgc[ex_ind]
n_selected = len(selected_pgc)

db_dir = "/home/ehsan/db_esn/data/"

max = -10
count = 0
for i in ex_ind[0]:
  
  pgc_dir = "pgc"+str(pgc[i])
  

  ra_id = str(int(np.floor(ra_cor[i])))
  if ra_cor[i] < 10:
     ra_id = '00'+ra_id+'D'
  elif ra_cor[i] < 100:
     ra_id = '0'+ra_id+'D'
  else:
     ra_id = ra_id+'D'
     
  
  desitination = db_dir + ra_id + '/sdss/fits/'
  root_file = desitination+pgc_dir
  
  comment = ""
  is_done = False
  
  
  if not is_done and os.path.exists(root_file+'_g_sex.txt'):
       sex_file = root_file+'_g_sex.txt'
       Status, RA, DEC, ra, rb, pa = split_func(sex_file)
       if Status:
         comment = "g_sextract"
         is_done = True
         #print comment, RA, DEC, ra, rb, pa
  

  if not is_done and os.path.exists(root_file+'_r_sex.txt'):
       sex_file = root_file+'_r_sex.txt'
       Status, RA, DEC, ra, rb, pa = split_func(sex_file)
       if Status:
         comment = "r_sextract"
         is_done = True
         #print comment, RA, DEC, ra, rb, pa


  if not is_done and os.path.exists(root_file+'_i_sex.txt'):
       sex_file = root_file+'_i_sex.txt'
       Status, RA, DEC, ra, rb, pa = split_func(sex_file)
       if Status:
         comment = "i_sextract"
         is_done = True
         #print comment, RA, DEC, ra, rb, pa
   
  if not is_done:
       RA  = ra_cor[i]
       DEC = dec_cor[i]
       ra  = d25[i]
       rb  = ra*b_a[i]
       pa  = PA[i]
       comment = "RC3"
       is_done = True
  
  
  g_file = root_file+'_g.fits'
  r_file = root_file+'_r.fits'
  i_file = root_file+'_i.fits'
  
  if not (os.path.exists(g_file) or os.path.exists(r_file) or os.path.exists(i_file)):
    #print comment, pgc_dir, RA, DEC, ra, rb, pa, Ty[i]
    #if ra>max and ra<60 : max = ra
    #count+=1
    R = 20*ra/60
    if R < 1.0: R = 1.0
    if ra < 60:
      print "sdssall", pgc_dir, RA, DEC, R, "0.396"
      print "rm -rf", pgc_dir
      print "mkdir ", pgc_dir
      print "mv ", pgc_dir+'_*.fits.gz', pgc_dir+"/."
    
#print max, count
     #### python glga_work_make.py > glga_work_hall2012

  
   
  
























