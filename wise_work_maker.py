#!/usr/bin/python
import sys
import os.path
import subprocess
import glob
import numpy as np
from astropy.table import Table, Column 
import pyfits
from subprocess import Popen, PIPE



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

db_dir = "/home/ehsan/db_esn/data/"
inFile = 'wise_photometry.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc  = table['PGC']
RA0   = table['RAJ']   # deg
DEC0  = table['DEJ']   # deg
d1   = table['MAJ']   # arcmin
d2   = table['MIN']   # arcmin
PA   = table['PA']
Ty   = table['Type']


for i in range(len(pgc)):
  
  pgc_dir = "pgc"+str(pgc[i])
  

  ra_id = str(int(np.floor(RA0[i])))
  if RA0[i] < 10:
     ra_id = '00'+ra_id+'D'
  elif RA0[i] < 100:
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
  

  if not is_done and os.path.exists(root_file+'_r_sex.txt'):
       sex_file = root_file+'_r_sex.txt'
       Status, RA, DEC, ra, rb, pa = split_func(sex_file)
       if Status:
         comment = "r_sextract"
         is_done = True


  if not is_done and os.path.exists(root_file+'_i_sex.txt'):
       sex_file = root_file+'_i_sex.txt'
       Status, RA, DEC, ra, rb, pa = split_func(sex_file)
       if Status:
         comment = "i_sextract"
         is_done = True



  if not is_done and os.path.exists(root_file+'_z_sex.txt'):
       sex_file = root_file+'_z_sex.txt'
       Status, RA, DEC, ra, rb, pa = split_func(sex_file)
       if Status:
         comment = "z_sextract"
         is_done = True


  if not is_done and os.path.exists(root_file+'_u_sex.txt'):
       sex_file = root_file+'_u_sex.txt'
       Status, RA, DEC, ra, rb, pa = split_func(sex_file)
       if Status:
         comment = "u_sextract"
         is_done = True

  if not is_done:
       RA  = RA0[i]
       DEC = DEC0[i]
       ra  = d1[i]
       rb  = d2[i]
       pa  = PA[i]
       comment = "WISE"
       is_done = True



  g_file = root_file+'_g.fits'
  r_file = root_file+'_r.fits'
  i_file = root_file+'_i.fits'

  if (os.path.exists(g_file) or os.path.exists(r_file) or os.path.exists(i_file)):
      # print comment, pgc_dir, RA, DEC, ra, rb, pa, Ty[i]
      print pgc_dir, RA, DEC, ra, rb, pa, Ty[i]
      #### python wise_work_maker.py > wise_work_qa_v02.txt

      
      
#temp = np.chararray(len(pgc))
#temp[:] = ';'

#myTable = Table()
#myTable.add_column(Column(data=temp, name=';'))
#myTable.add_column(Column(data=pgc, name='pgc'))
#myTable.add_column(Column(data=ra, name='ra'))
#myTable.add_column(Column(data=dec, name='dec'))
#myTable.add_column(Column(data=d1, name='a'))
#myTable.add_column(Column(data=d2, name='b'))
#myTable.add_column(Column(data=pa, name='pa'))
#myTable.add_column(Column(data=ty, name='type'))

#myTable.write('wise_work_qa.txt', format='ascii.fixed_width',delimiter=' ', bookend=False)













