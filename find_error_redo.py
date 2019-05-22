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
    while columns[j]==' ': j+=1
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

### For a given photometry file, this returns the magnitude value
def get_mag(photometry):
    if os.path.exists(photometry):
      with open(photometry) as f:
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
###############################
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
  note = ''
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



#datasets = ['data_set_21.glga', 'data_set_41.glga', 'PStesters_sdss.glga', 'pilot_01.glga', 'pilot_02.glga', 'pilot_03.glga', 'data_set_31.glga', 'data_set_22.glga', 'data_summer_1.glga', 'data_summer_8.glga'] 


#destination = '/home/ehsan/PanStarrs/EDD_server/public_html/cf4_photometry/sdss_photometry/'

destination = '/var/run/media/ehsan/HOURI/sdss_photometry/'

datasets  = []
locations = []

datasets.append('pilot_01.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_pilot_01/')

datasets.append('pilot_02.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_pilot_02/')

datasets.append('pilot_03.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_pilot_03/')

datasets.append('pilot_05.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_pilot_05/')

datasets.append('data_set_11.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_11/')

datasets.append('data_set_21.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_21/')

datasets.append('data_set_22.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_22/')

datasets.append('data_set_31.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_31/')

datasets.append('data_set_41.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_41/')

datasets.append('data_summer_1.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_1/')

datasets.append('data_summer_2.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_2/')

datasets.append('data_summer_8.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_8/')

datasets.append('data_summer_9.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_9/')



datasets.append('data_summer_16.glga')
locations.append('/home/ehsan/db_esn/data_summer_16/')

datasets.append('data_set_51.glga')
locations.append('/home/ehsan/db_esn/data_set_51/')


########################################################################
inFile  = 'New_era/IMPORTANT_ehsan_NOTES'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
PGC     = table['PGC']
  

########################################################################
########################################################################
for index in range(len(datasets)):

        dataset = datasets[index]
        location = locations[index]
        pgcname, radb = read_glga('New_era/'+dataset)
         

        for i in range(len(pgcname)):
                     
            
            if True:
                
                
                
                photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_i_asymptotic.dat'
                if os.path.exists(photometry):
                    
                    gal_pgc = int(pgcname[i][3:])
                    
                    
                    ii = get_mag(photometry)
                    
                    
                    photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_g_asymptotic.dat'
                    gg = get_mag(photometry)
                    


                    photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_r_asymptotic.dat'
                    rr = get_mag(photometry)
                    
                    

                    
                    ellipsefile = location + radb[i] +'/photometry/'+pgcname[i]+'_i_ellipsepar.dat'
                    ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse(ellipsefile)
                
                  
                    
                    
                    note_file = location + radb[i] + '/sdss/fits/' + pgcname[i] + '_qa.txt'
                    quality     = get_quality(note_file)
                    disturbed   = get_quality(note_file, nline=41)
                    trail       = get_quality(note_file, nline=42)
                    not_spiral  = get_quality(note_file, nline=43)
                    face_on     = get_quality(note_file, nline=44)
                    faint       = get_quality(note_file, nline=45)
                    crowded     = get_quality(note_file, nline=46)
                    over_masked = get_quality(note_file, nline=47)
                    fov         = get_quality(note_file, nline=20)
                    multiple    = get_quality(note_file, nline=19)
                    bright_star = get_quality(note_file, nline=18)   
                    uncertain   = get_quality(note_file, nline=17)
                    note        = read_note(note_file)
                    
                    
                    if quality<3 and not pgcname[i] in PGC:
                      print pgcname[i]
                  
                
                


