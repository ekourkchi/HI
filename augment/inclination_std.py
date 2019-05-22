#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import sqlcl
#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.
##########################################
###############################
def isInSDSS_DR12(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcl.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
  
###############################
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
#################################################################
def SDSS_db_avilability(pgc, ra, dec, Filters=['u', 'g', 'r', 'i', 'z'], db_dir='', toDbase=False):
   
   pgc_dir = "pgc"+str(pgc)
   directory = "/home/ehsan/db_esn/Alfalfa70_SDSS_REPO/"+pgc_dir
   isDirAvailable =  os.path.isdir(directory)
   
   file_existence = 0
   
   if isDirAvailable:
     
     ra_id = str(int(np.floor(ra)))
     if ra < 10:
       ra_id = '00'+ra_id+'D'
     elif ra < 100:
       ra_id = '0'+ra_id+'D'
     else:
       ra_id = ra_id+'D'
     

     desitination = db_dir + ra_id + '/sdss/fits/'
     
     
     for filters in Filters:
        fname = directory+'/'+pgc_dir+'_'+filters+'.fits.gz'
        fname2 = '/home/ehsan/Dropbox/Home/PanStarrs/Jan/HI/SDSS+/'+pgc_dir+'_'+filters+'.fits.gz'
        if os.path.exists(fname):
	   
	   file_existence += 1
	   if toDbase:
	      command = ["cp", fname, desitination]
	      subprocess.call(command)
	      subprocess.call(['gunzip', '-f', desitination+pgc_dir+'_'+filters+'.fits.gz'])
           


   return file_existence


#################################################################
def exclude(pgc, pgc_ex):
  
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
  for i in range(n_ex):
    while(pgc[j] < pgc_ex[i] and pgc[j]  < n0):
      j+=1
    if pgc[j] == pgc_ex[i]:
      indices[j] = -1   # will be excluded
      j+=1
  
  return (indices[np.where(indices > -1)],)
  

#################


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
  

############################################################


inFile = 'All_LEDA_EDD.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_leda    = table['pgc']
ra_leda     = table['al2000']
dec_leda    = table['de2000']
gl_leda     = table['l2']
gb_leda     = table['b2']
sgl_leda    = table['sgl']
sgb_leda    = table['sgb']
logd25_leda = table['logd25']
logr25_leda = table['logr25']
ty_leda     = table['t']
pa_leda     = table['pa']
type_leda   = table['type']
name_leda   = table['objname']

ra_leda *= 15.
d25_leda = 0.1*(10**logd25_leda)
b_a_leda = 1./(10**logr25_leda)

inFile = 'inclination_prototypes_best73.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc_brent      = table['pgc']
inc_brent      = table['inc']

############################################################
ra_brent   = []
dec_brent  = []
gl_brent   = []
gb_brent   = []
sgl_brent  = []
sgb_brent  = []
sdss_brent = []
d25_brent  = []
pa_brent   = []
b_a_brent  = []
ty_brent   = []
type_brent = []
name_brent = []


for i in range(len(pgc_brent)):
    print i
    for j in range(len(pgc_leda)):
        if pgc_brent[i] == pgc_leda[j]:
            
            ra = ra_leda[j]
            dec = dec_leda[j]
            ra_brent.append(ra) 
            dec_brent.append(dec)   
            gl_brent.append(gl_leda[j])    
            gb_brent.append(gb_leda[j])    
            sgl_brent.append(sgl_leda[j])   
            sgb_brent.append(sgb_leda[j])   
            d25_brent.append(d25_leda[j])   
            pa_brent.append(pa_leda[j])    
            b_a_brent.append(b_a_leda[j])   
            ty_brent.append(ty_leda[j])    
            type_brent.append(type_leda[j]) 
            name_brent.append(name_leda[j]) 
            
            if isInSDSS_DR12(ra, dec) == 1:
                sdss_brent.append(1)  
            else:
                sdss_brent.append(0)  
                

            break             

############################################################

myTable = Table()
myTable.add_column(Column(data=pgc_brent, name='pgc'))
myTable.add_column(Column(data=ra_brent, name='ra', format='%0.4f'))
myTable.add_column(Column(data=dec_brent, name='dec', format='%0.4f'))
myTable.add_column(Column(data=gl_brent, name='gl', format='%0.4f'))
myTable.add_column(Column(data=gb_brent, name='gb', format='%0.4f'))
myTable.add_column(Column(data=sgl_brent, name='sgl', format='%0.4f'))
myTable.add_column(Column(data=sgb_brent, name='sgb', format='%0.4f'))
myTable.add_column(Column(data=d25_brent, name='d25', format='%0.2f'))
myTable.add_column(Column(data=b_a_brent, name='b_a', format='%0.2f'))
myTable.add_column(Column(data=pa_brent, name='pa', format='%0.2f'))
myTable.add_column(Column(data=ty_brent, name='ty', format='%0.2f'))
myTable.add_column(Column(data=type_brent, name='type'))
myTable.add_column(Column(data=name_brent, name='name'))
myTable.add_column(Column(data=inc_brent, name='inc'))
myTable.add_column(Column(data=sdss_brent, name='sdss'))
myTable.write('inclination_std.csv', format='ascii.fixed_width',delimiter=',', bookend=False) 
