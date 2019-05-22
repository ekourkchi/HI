#!/usr/bin/python
import sys
import os
import subprocess
import math
import numpy as np
from astropy.table import Table, Column 
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
def read_note(filename):

  qa_note =  filename
  note = ' '
  if os.path.exists(qa_note):
     with open(qa_note) as f:
	counter = 1
	for line in f:
	  if counter == 11:
	    line_split = line.split("=")
	    note =  line_split[1]
	    note = note[0:len(note)-1]
	  counter+=1       
       
  return note

#################################
#########################################
def read_glga_wise(filename):
  
  name_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    name_ID = columns[0]
    name_lst.append(name_ID)
  
  return name_lst 
##############################################

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
######################################

location_sdss  = '/home/ehsan/db_esn/cf4_sdss/data/'
location_wise  = '/home/ehsan/db_esn/cf4_wise/data/'


inFile = 'augment/wise_all.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
wise_name = table['ID']
wise_pgc  = table['PGC']




############################################################



inFile  = 'augment/EDD_distance_cf4_v12.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  
sdss    = table['sdss']  
d25     = table['d25']
b_a     = table['b_a']
PA      = table['pa']
Ty      = table['ty']  
type      = table['type']
alfa100_  = table['alfa100']
QA_sdss   = table['QA_sdss']  
QA_wise   = table['QA_wise'] 

N = len(pgc)

quality     = np.zeros(N)
disturbed   = np.zeros(N)
trail       = np.zeros(N)
not_spiral  = np.zeros(N)
face_on     = np.zeros(N)
faint       = np.zeros(N)
crowded     = np.zeros(N)
over_masked = np.zeros(N)
fov         = np.zeros(N)
multiple    = np.zeros(N)
bright_star = np.zeros(N)
uncertain   = np.zeros(N)
note        = np.zeros((N,), dtype='a150')
source      = np.zeros((N,), dtype='a4')

Good = 0 
for i in range(len(pgc)):
    
    Getit = True
    
    radb    = ra_db(ra[i])
    pgcname = 'pgc'+str(pgc[i])
    qa_txt_sdss = location_sdss + radb + '/sdss/fits/' + pgcname+'_qa.txt'
    
    found = False
    if os.path.exists(qa_txt_sdss):
        qa_txt  = qa_txt_sdss
        found = True
        source[i] = 'SDSS'
    else:
        if QA_wise[i]==1:
            if pgc[i] in wise_pgc:
                i_lst = np.where(wise_pgc == pgc[i])
                galname = wise_name[i_lst][0]
                qa_txt_wise = location_wise + radb + '/wise/fits/' + galname+'_qa.txt'
                if not os.path.exists(qa_txt_wise):
                    galname = 'pgc'+str(pgc[i])
            else:
                galname = 'pgc'+str(pgc[i])
                
            qa_txt_wise = location_wise + radb + '/wise/fits/' + galname+'_qa.txt'
            if os.path.exists(qa_txt_wise):
                qa_txt  = qa_txt_wise
                found = True
                source[i] = 'WISE'
            else: 
                #print galname
                print galname, ra[i], dec[i], d25[i], d25[i]*b_a[i], PA[i], Ty[i]
                
                source[i] = 'NONE'
            
            
    if found:

        quality[i]     = get_quality(qa_txt)
        disturbed[i]   = get_quality(qa_txt, nline=41)
        trail[i]       = get_quality(qa_txt, nline=42)
        not_spiral[i]  = get_quality(qa_txt, nline=43)
        face_on[i]     = get_quality(qa_txt, nline=44)
        faint[i]       = get_quality(qa_txt, nline=45)
        crowded[i]     = get_quality(qa_txt, nline=46)
        over_masked[i] = get_quality(qa_txt, nline=47)
        fov[i]         = get_quality(qa_txt, nline=20)
        multiple[i]    = get_quality(qa_txt, nline=19)
        bright_star[i] = get_quality(qa_txt, nline=18)   
        uncertain[i]   = get_quality(qa_txt, nline=17)
        note[i]        = read_note(qa_txt)     
        
        if quality[i]>=0 and quality[i]<3: Getit=False
        if uncertain[i]==1: Getit=False
        if multiple[i]==1: Getit=False
        if disturbed[i]==1: Getit=False
        if trail[i]==1: Getit=False
        if not_spiral[i]==1: Getit=False
        if face_on[i]==1: Getit=False
        
        if Getit: Good+=1
        
           
print Good
#myTable = Table()
#myTable.add_column(Column(data=pgc, name='pgc'))
#myTable.add_column(Column(data=ra,  name='ra', format='%0.4f')) 
#myTable.add_column(Column(data=dec,  name='dec', format='%0.4f')) 
#myTable.add_column(Column(data=source,  name='source', dtype='S4'))
#myTable.add_column(Column(data=quality,  name='qlt', dtype=np.dtype(int)))
#myTable.add_column(Column(data=disturbed,  name='dst', dtype=np.dtype(int)))
#myTable.add_column(Column(data=trail,  name='trl', dtype=np.dtype(int)))
#myTable.add_column(Column(data=not_spiral,  name='nsp', dtype=np.dtype(int)))
#myTable.add_column(Column(data=face_on,  name='fon', dtype=np.dtype(int)))
#myTable.add_column(Column(data=faint,  name='fnt', dtype=np.dtype(int)))
#myTable.add_column(Column(data=crowded,  name='cwd', dtype=np.dtype(int)))
#myTable.add_column(Column(data=over_masked,  name='ovm', dtype=np.dtype(int)))
#myTable.add_column(Column(data=fov,  name='fov', dtype=np.dtype(int)))
#myTable.add_column(Column(data=multiple,  name='mlp', dtype=np.dtype(int)))
#myTable.add_column(Column(data=bright_star,  name='bts', dtype=np.dtype(int)))
#myTable.add_column(Column(data=uncertain,  name='unc', dtype=np.dtype(int)))
#myTable.add_column(Column(data=note,  name='note', dtype='S150'))

#myTable.write('test.csv', format='ascii.fixed_width',delimiter=',', bookend=False)        
        
        
                    
        
        
        
        
        
        
        
        
    
    
    

