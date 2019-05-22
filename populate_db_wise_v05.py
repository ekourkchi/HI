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



#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.
##########################################

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
#################
def QA_SDSS_DONE(pgc, ra):
    
    
    databse = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/'+'/cf4_sdss/data/'
    
    name = 'pgc'+str(pgc)
    if os.path.exists(databse+ra_db(ra)+'/sdss/fits/'+name+'_qa.txt'):
        return True
        
    return False   
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
def get_back(backfile):
    if os.path.exists(backfile):
      with open(backfile) as f:
	counter = 1
	for line in f:
	  if line.split(" ")[0]!= '#' and line.split(" ")[0]!='#\n':
	    line_split = line.split(" ")
	    not_void = 0 
	    set_param = False
	    for thing in line_split:
	      if thing != '': 
                  not_void+=1
                  set_param = True
	      if not_void==8 and set_param: 
                  back_modify_radius = np.float(thing)
                  set_param = False
	      if not_void==9 and set_param: 
                  back_modify_percent = np.float(thing)                  
                  set_param = False
	          return back_modify_radius/60., back_modify_percent
	  counter+=1
    return 0.,0.

def get_no_frame(fname):
    
    if os.path.exists(fname):
        hdulist = pyfits.open(fname)
        prihdr = hdulist[0].header
        return int(prihdr['NUMFRMS'])
    else:
        return 0
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
          


def get_ellipse(filename):
          
          ra_cen = -1
          dec_cen = -1
          semimajor = -1
          semiminor = -1
          PA = -1
          with open(filename) as f:
            counter = 1
            for line in f:
              if line.split(" ")[0]!= '#' and line.split(" ")[0]!='#\n': # counter == 17:
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



destination = '/var/run/media/ehsan/HOURI/wise_photometry/'

datasets  = []
locations = []

location = '/home/ehsan/db_esn/cf4_wise/data/'


inFile  = 'augment/EDD_distance_cf4_v07.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  

########################################################################


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
            
                    directory = destination+'pgc'+str(pgc[i])
                    isDirAvailable =  os.path.isdir(directory)
                    if not isDirAvailable:
                        xcmd('mkdir '+directory, True)
                    
                    
                    with cd(directory):
                        
                        
                        
                        photometry =  location + radb +'/photometry/'+galname+'_w1_asymptotic.dat'
                        if os.path.exists(photometry):
                            
                            gal_pgc = pgc[i]
                            
                            
                            
                            w1 = get_mag(photometry)

                            
                            photometry =  location + radb +'/photometry/'+galname+'_w2_asymptotic.dat'
                            w2 = get_mag(photometry)
                            #print photometry
                            


                            photometry =  location + radb +'/photometry/'+galname+'_w3_asymptotic.dat'
                            w3 = get_mag(photometry)
                            
                            
                            qual = get_quality(qa_txt)
                            
                            ellipsefile = location + radb +'/photometry/'+galname+'_w1_ellipsepar.dat'
                            
                            if not os.path.isfile(ellipsefile):
                                ellipsefile = location + radb +'/photometry/'+galname+'_w2_ellipsepar.dat'
                            if not os.path.isfile(ellipsefile):
                                ellipsefile = location + radb +'/photometry/'+galname+'_w3_ellipsepar.dat'                                
                            if not os.path.isfile(ellipsefile):
                                ellipsefile = location + radb +'/photometry/'+galname+'_w4_ellipsepar.dat'
                                                            
                            ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse(ellipsefile)
                        
                            
                            string = '<table border="1" width="50%">'
                            
                            string = string + '<tr>'
                            string = string + "<th>"+'pgc'+"</th>"
                            string = string + "<th>"+'ra (deg)'+"</th>"
                            string = string + "<th>"+'dec (deg)'+"</th>"
                            string = string + "<th>"+"semimajor (')"+"</th>"
                            string = string + "<th>"+"semiminor (')"+"</th>"
                            string = string + "<th>"+'PA (deg)'+"</th>"
                            string = string + "<th>"+'w1 (mag)'+"</th>"
                            string = string + "<th>"+'w2 (mag)'+"</th>"
                            string = string + "<th>"+'w3 (mag)'+"</th>"
                            string = string + '</tr>'
                            
                            string = string + '<tr>'
                            string = string + "<td>"+str(gal_pgc)+"</td>"
                            string = string + "<td>"+'{:.4f}'.format(ra_cen)+"</td>"
                            string = string + "<td>"+'{:.4f}'.format(dec_cen)+"</td>"
                            string = string + "<td>"+'{:.2f}'.format(semimajor/60.)+"</td>"
                            string = string + "<td>"+'{:.2f}'.format(semiminor/60.)+"</td>"
                            string = string + "<td>"+str(PA)+"</td>"
                            string = string + "<td>"+'{:.2f}'.format(w1)+"</td>"
                            string = string + "<td>"+'{:.2f}'.format(w2)+"</td>"
                            string = string + "<td>"+'{:.2f}'.format(w3)+"</td>"
                            string = string + '</tr>'                   
                            
                            
                            
                            string = string + '</table>'
                            string = string + '<br> <br>'
                            

                            with open(galname+'_t1.htm', 'w+') as f:
                                f.write(string)
                            
                            
                            
                            
                            string = '<table border="1" >'
                            string = string + '<tr>'
                            string = string + "<th>"+'# w1-Frames'+"</th>"
                            string = string + "<th>"+'# w2-Frames'+"</th>"
                            string = string + "<th>"+'# w3-Frames'+"</th>"
                            string = string + "<th>"+'back modify radius (arcmin)'+"</th>"
                            string = string + "<th>"+'back modify w1 (%)'+"</th>"
                            string = string + "<th>"+'back modify w2 (%)'+"</th>"
                            string = string + "<th>"+'back modify w3 (%)'+"</th>"
                            string = string + '</tr>'
                            
                            
                            backfile = location + radb +'/photometry/'+galname+'_w1_background.dat'
                            back_rad, w1_back_pcent = get_back(backfile)
                            backfile = location + radb +'/photometry/'+galname+'_w2_background.dat'
                            tmp_rad, w2_back_pcent = get_back(backfile)
                            backfile = location + radb +'/photometry/'+galname+'_w3_background.dat'
                            tmp_rad, w3_back_pcent = get_back(backfile)
                            
                            fits_file = location + radb +'/wise/fits/'+galname+'_w1.fits.gz'
                            w1_frame = get_no_frame(fits_file)
                            fits_file = location + radb +'/wise/fits/'+galname+'_w2.fits.gz'
                            w2_frame = get_no_frame(fits_file)
                            fits_file = location + radb +'/wise/fits/'+galname+'_w3.fits.gz'
                            w3_frame = get_no_frame(fits_file)
                            
                            string = string + '<tr>'
                            string = string + "<td>"+str(w1_frame)+"</td>"
                            string = string + "<td>"+str(w2_frame)+"</td>"
                            string = string + "<td>"+str(w3_frame)+"</td>"
                            
                            if back_rad>0:
                                string = string + "<td>"+'{:.2f}'.format(back_rad)+"</td>"
                                string = string + "<td>"+'{:.2f}'.format(w1_back_pcent)+"</td>"
                                string = string + "<td>"+'{:.2f}'.format(w2_back_pcent)+"</td>"
                                string = string + "<td>"+'{:.2f}'.format(w3_back_pcent)+"</td>"
                            else:
                                string = string + "<td></td>"
                                string = string + "<td></td>"
                                string = string + "<td></td>"
                                string = string + "<td></td>"

                            string = string + '</tr>'
                            string = string + '</table>'
                            string = string + '<br> <br>'
                            #print string
                            #sys.exit()
                            with open(galname+'_t1.5.htm', 'w+') as f:
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
                            
                            
                        quality     = get_quality(qa_txt)
                        disturbed   = get_quality(qa_txt, nline=41)
                        trail       = get_quality(qa_txt, nline=42)
                        not_spiral  = get_quality(qa_txt, nline=43)
                        face_on     = get_quality(qa_txt, nline=44)
                        faint       = get_quality(qa_txt, nline=45)
                        crowded     = get_quality(qa_txt, nline=46)
                        over_masked = get_quality(qa_txt, nline=47)
                        fov         = get_quality(qa_txt, nline=20)
                        multiple    = get_quality(qa_txt, nline=19)
                        bright_star = get_quality(qa_txt, nline=18)   
                        uncertain   = get_quality(qa_txt, nline=17)
                        note        = read_note(qa_txt)
                            
                            
                        string = string + '<tr>'
                             
                        if quality>-1 and quality<3:
                            echo_str = str(pgc[i]) + ', ' + str(galname) + ', ' + str(quality)
                            xcmd('echo '+echo_str +' >> /home/ehsan/PanStarrs/Jan/HI/wise_low_quality.csv',False)
                                
                            
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
 
                            
                        with open(galname+'_t2.htm', 'w+') as f:
                            f.write(string)
                            
                        
                        cmd = 'cp '+ location + radb + '/wise/fits/' + galname + '_qa.txt .'
                        xcmd(cmd, True)
                        
                        cmd = 'cp '+ location + radb + '/plots/' + galname + '_wise_images.jpg .'
                        xcmd(cmd, True)
                    
                        cmd = 'cp '+ location + radb + '/plots/' + galname + '_wise_profile.jpg .'
                        xcmd(cmd, True)
                        
                        
                        cmd = 'cp '+ location + radb + '/plots/' + galname + '_wise_images.pdf .'
                        xcmd(cmd, True)

                        cmd = 'cp '+ location + radb + '/plots/' + galname + '_wise_profile.pdf .'
                        xcmd(cmd, True)
                        
                        
                        cmd = 'cp '+ location + radb + '/photometry/' + galname + '_*_annprofile.dat .'
                        xcmd(cmd, True)

                        
                        
                        
                    #sys.exit()
            


