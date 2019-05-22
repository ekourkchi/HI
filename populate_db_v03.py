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

#datasets.append('pilot_01.glga')   # Arash (Vrified)+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_pilot_01/')

#datasets.append('pilot_02.glga')   # Jordan (Vrified)+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_pilot_02/')

#datasets.append('pilot_03.glga')   # Sarah (Vrified)+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_pilot_03/')

#datasets.append('pilot_05.glga')   # Randy-Ehsan - V+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_pilot_05/')

#datasets.append('data_set_11.glga')   # Arash+V(April/06/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_11/')

#datasets.append('data_set_12.glga')   # Arash-Ehsan - V+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_12/')

#datasets.append('data_set_21.glga')   # Jordan+V(April/07/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_21/')

#datasets.append('data_set_22.glga')   # Ehsan - V+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_22/')

#datasets.append('data_set_31.glga')   # Sarah (Vrified)+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_31/')

#datasets.append('data_set_41.glga')   # Ehsan - V+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_41/')

#datasets.append('data_set_51.glga')   # Chase-Ehsan - V+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_set_51/')


#datasets.append('data_summer_1.glga')   # Randy+(April/07/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_1/')

#datasets.append('data_summer_2.glga')   # Randy+V(April/09/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_2/')

#datasets.append('data_summer_3.glga')   # Randy+V(April/19/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_3/')

#datasets.append('data_summer_4.glga')   # Randy+V(April/28/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_4/')

#datasets.append('data_summer_5.glga')   # Randy+V(May/03/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_5/')

#datasets.append('data_summer_6.glga')   # Randy-Ehsan (verified)+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_6/')

#datasets.append('data_summer_7.glga')   # Ehsan-Arash (verified)+
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_7/')


#datasets.append('data_summer_8.glga')   # Jordan+V(April/08/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_8/')

#datasets.append('data_summer_9.glga')   # Jordan+V(April/08/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_9/')

#datasets.append('data_summer_10.glga')   # Jordan+V(April/09/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_10/')

#datasets.append('data_summer_11.glga')   # Jordan+V(April/19/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_11/')

#datasets.append('data_summer_12.glga')   # Jordan+V(April/28/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_12/')

#datasets.append('data_summer_13.glga')   # Jordan+V(May/06/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_13/')

#datasets.append('data_summer_14.glga')   # Jordan+V(May/06/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_14/')

#datasets.append('data_summer_15.glga')   # Jordan+V(May/06/2018)
#locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_15/')

datasets.append('data_summer_16.glga')   # Sarah+V(April/07/2018)
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_16/')

datasets.append('data_summer_17.glga')   # Arash+V(April/08/2018)
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_17/')

datasets.append('data_summer_18.glga')   # Arash+V(April/08/2018)
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_18/')

datasets.append('data_summer_19.glga')   # Sarah+V(April/08/2018)
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_19/')

datasets.append('data_summer_20.glga')   # Chase-Ehsan+
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_20/')

datasets.append('data_gold1.glga')   # Ehsan - V+
locations.append('/home/ehsan/db_esn/DONE_DATA/data_gold1/')

datasets.append('data_gold2.glga')   # Ehsan - V+
locations.append('/home/ehsan/db_esn/DONE_DATA/data_gold2/')


########################################################################
########################################################################
########################################################################
for index in range(len(datasets)):

        dataset = datasets[index]
        location = locations[index]
        pgcname, radb = read_glga('New_era/'+dataset)
         

        for i in range(len(pgcname)):
            
            directory = destination+pgcname[i]
            isDirAvailable =  os.path.isdir(directory)
            
            if not isDirAvailable:
                xcmd('mkdir '+directory, True)
            
            
            with cd(directory):
                
                
                
                photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_i_asymptotic.dat'
                if os.path.exists(photometry):
                    
                    gal_pgc = int(pgcname[i][3:])
                    
                    
                    ii = get_mag(photometry)
                    
                    
                    photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_g_asymptotic.dat'
                    gg = get_mag(photometry)
                    


                    photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_r_asymptotic.dat'
                    rr = get_mag(photometry)
                    
                    
                    qa_txt = location + radb[i] + '/sdss/fits/' + pgcname[i]+'_qa.txt'
                    qual = get_quality(qa_txt)
                    
                    ellipsefile = location + radb[i] +'/photometry/'+pgcname[i]+'_i_ellipsepar.dat'
                    ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse(ellipsefile)
                
                    
                    string = '<table border="1" width="50%">'
                    
                    string = string + '<tr>'
                    string = string + "<th>"+'pgc'+"</th>"
                    string = string + "<th>"+'ra (deg)'+"</th>"
                    string = string + "<th>"+'dec (deg)'+"</th>"
                    string = string + "<th>"+"semimajor (')"+"</th>"
                    string = string + "<th>"+"semiminor (')"+"</th>"
                    string = string + "<th>"+'PA (deg)'+"</th>"
                    string = string + "<th>"+'g (mag)'+"</th>"
                    string = string + "<th>"+'r (mag)'+"</th>"
                    string = string + "<th>"+'i (mag)'+"</th>"
                    string = string + '</tr>'
                    
                    string = string + '<tr>'
                    string = string + "<td>"+str(gal_pgc)+"</td>"
                    string = string + "<td>"+'{:.4f}'.format(ra_cen)+"</td>"
                    string = string + "<td>"+'{:.4f}'.format(dec_cen)+"</td>"
                    string = string + "<td>"+'{:.2f}'.format(semimajor/60.)+"</td>"
                    string = string + "<td>"+'{:.2f}'.format(semiminor/60.)+"</td>"
                    string = string + "<td>"+str(PA)+"</td>"
                    string = string + "<td>"+'{:.2f}'.format(gg)+"</td>"
                    string = string + "<td>"+'{:.2f}'.format(rr)+"</td>"
                    string = string + "<td>"+'{:.2f}'.format(ii)+"</td>"
                    string = string + '</tr>'                   
                    
                    
                    
                    string = string + '</table>'
                    string = string + '<br> <br>'
                    
                    #print
                    #print string
                    with open(pgcname[i]+'_t1.htm', 'w+') as f:
                        f.write(string)
                        
                    
                    string = '<table border="1" >'
                    
                    string = string + '<tr>'
                    string = string + "<th>"+'quality*'+"</th>"
                    string = string + "<th>"+'uncertain'+"</th>"
                    string = string + "<th>"+'multiple'+"</th>"
                    string = string + "<th>"+'bright star'+"</th>"
                    string = string + "<th>"+'FOV'+"</th>"
                    string = string + "<th>"+'disturbed'+"</th>"
                    string = string + "<th>"+'trail'+"</th>"
                    string = string + "<th>"+'not spiral'+"</th>"
                    string = string + "<th>"+'face-on'+"</th>"
                    string = string + "<th>"+'faint'+"</th>"
                    string = string + "<th>"+'crowded'+"</th>"
                    string = string + "<th>"+'over-masked'+"</th>"
                    string = string + "<th>"+'Note'+"</th>"
                    string = string + '</tr>'
                    
                    
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
                    
                    
                    string = string + '<tr>'
                    
                    if quality>-1:
                       string = string + "<td>"+str(quality)+"</td>"
                    else: string = string + "<td> </td>"
                    
                    if uncertain>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"
                    
                    if multiple>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"                    
                    
                    if bright_star>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"
                    
                    if fov>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"                    
                    
                    if disturbed>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"                    
                                        
                    if trail>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"                    
                                        
                    if not_spiral>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"                    
                                        
                    if face_on>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"  
                                        
                    if faint>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"                      
                    
                    if crowded>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"                      
                    
                    if over_masked>0:
                       string = string + "<td>"+'<img src="web_images/checkmark.png" alt="1" style="width:20px;height:20px;">'+"</td>"
                    else: string = string + "<td> </td>"                                                              
                                        
                    string = string + "<td><div style='width: 200px;'>"+note+"</div></td>"
                    string = string + '</tr>'
                    
                    string = string + '</table>'
                    #string = string + '<br> <br>'
                    #print 
                    #print string 
                    
                    #print 
                    #print note_file
                    
                    with open(pgcname[i]+'_t2.htm', 'w+') as f:
                        f.write(string)
                    #sys.exit()
                    
                
                
                cmd = 'cp '+ location + radb[i] + '/sdss/fits/' + pgcname[i] + '_qa.txt .'
                xcmd(cmd, True)
                
                cmd = 'cp '+ location + radb[i] + '/plots/' + pgcname[i] + '_sdss_images.jpg .'
                xcmd(cmd, True)
            
                cmd = 'cp '+ location + radb[i] + '/plots/' + pgcname[i] + '_sdss_profile.jpg .'
                xcmd(cmd, True)
                
                
                cmd = 'cp '+ location + radb[i] + '/plots/' + pgcname[i] + '_sdss_images.pdf .'
                xcmd(cmd, True)

                cmd = 'cp '+ location + radb[i] + '/plots/' + pgcname[i] + '_sdss_profile.pdf .'
                xcmd(cmd, True)
                
                
                cmd = 'cp '+ location + radb[i] + '/photometry/' + pgcname[i] + '_*_annprofile.dat .'
                xcmd(cmd, True)

                
                
                


