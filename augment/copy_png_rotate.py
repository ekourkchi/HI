#!/usr/bin/python
import sys
import os
import os.path
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import pyfits
######################################
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
 
######################################

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
######################################
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

######################################

      
      
###########################################################################    
      
### Example: python make_png.py hall_list_ps.csv
##################################################

inFile  = 'EDD_distance_cf4_v17.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec']  
sdss    = table['sdss']  
d25     = table['d25']
b_a     = table['b_a']
PA      = table['pa']
Ty      = table['ty']  
QA_wise = table['QA_wise']  
QA_sdss = table['QA_sdss']
inc     = table['inc'] 
inc_flag = table['inc_flg'] 

##################################################
inFile = 'TFcalibrators.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_TFcalibrators    = table['PGC']
##################################################
inFile = 'TFcalibrators_Arecibo.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_TF_arecibo    = table['PGC']
RADE_TF_arecibo   = table['RADE']
TY_TF_arecibo     = table['T']
logr25_TF_arecibo = table['logr25']
Glon_TF_arecibo = table['Glon']
Glat_TF_arecibo = table['Glat']
SGL_TF_arecibo = table['SGL']
SGB_TF_arecibo = table['SGB']
b_a_TF_arecibo = 1./(10**logr25_TF_arecibo)


inFile = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/Home/PanStarrs/Jan/HI/augment/wise_all.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
ID_all  = table['ID']
PGC_all = table['PGC']


###################################### 1st stage + 2nd stage
inFile = 'SDSS_quality.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgcID    = table['pgcID']
selected = table['selected']

###################################### 2nd stage
inFile = 'PS_SDSS_quality.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgcID2    = table['pgcID']
selected2 = table['selected']
######################################


no  = 0 
All = 0
db_dir_sdss = '/home/ehsan/db_esn/cf4_sdss/'
db_dir_wise = '/home/ehsan/db_esn/cf4_wise/'
destination = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/Home/PanStarrs/INConline/demos/galpool/'
path1 = '/home/ehsan/db_esn/curtis/PNG_rotate/'
path2 = '/home/ehsan/PanStarrs/INClinationCode/PNG_rotate/'
path3 = '/home/ehsan/db_esn/my_PS_db/PNG_rotate/'
path4 = '/home/ehsan/db_esn/cf4_sdss/SDSS_PNG_rotate/'
path5 = '/home/ehsan/db_esn/curtis/DSS/DSS_PNG_rotate/'
path6 = '/home/ehsan/db_esn/DSS/DSS_PNG_rotate/'


paths = [path1, path2, path3, path4, path5, path6]


###################################### 2nd stage
inFile = '/home/ehsan/PanStarrs/INConline/INCLINATION_tools/Input_Grand_ALL_review_v01.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgcID_all    = table['pgcID']
selected_all = table['selected']
######################################


for i in range(0, len(pgcID_all)):
  
  
  if not pgcID_all[i] in pgc_TFcalibrators and not pgcID_all[i] in pgc_TF_arecibo:
   
    All+=1
    
    
    #if inc[i]==0 and inc_flag[i]==0:
    #if QA_sdss[i]==0 or QA_wise[i]==0:
        
    if selected_all[i]==0:
            
           no +=1
           print pgcID_all[i]
        
    ##if True:
    
       #All+=1
       #fileRoot = 'pgc'+str(pgc[i])+'_d25x2_rot'
       #has_g = False
       #has_r = False
       #has_i = False
       #has_gri = False
       #for filt in ['_g','_r','_i','_gri']:
           
           #for p in range(len(paths)):
               
               #### dealing with bad single colorful images returned by the SDSS system
               #### don't use these single images, because my code has failed and SDSS has returned something irrelevant
               #if p==3 and filt=='_gri':
                   #if os.path.isfile(paths[p]+fileRoot+'_gri.jpg') and not os.path.isfile(paths[p]+fileRoot+'_g.png'): continue
               
               
               #q = p
               
               #if filt=='_gri': sfx='.jpg' 
               #else: sfx='.png'
               #File1 = fileRoot + filt + sfx
               #File2 = fileRoot + filt + sfx

               #if os.path.isfile(paths[p]+File1):
                   
                   #if p==3:  # SDSS
                       #if pgc[i] in pgcID:
                           #index = np.where(pgcID==pgc[i])
                           #if selected[index][0]==1:
                               #if sfx=='.png':
                                   #File1 = fileRoot + filt + '.back' + sfx
                               #if not os.path.isfile(paths[p] +File1): 
                                   #File1=File2
                                   
##########################################################################################                           
                   #if p<3:  #PS
                       
                       ###### First stage - SDSS vs. PS (1st stage only)(comment this block for the stage 2) 
                       ##if os.path.isfile(paths[3]+File1):
                           ##File3 = fileRoot + filt + sfx
                           ##File4 = fileRoot + filt + '.back' + sfx
                           ##if pgc[i] in pgcID:
                               ##index = np.where(pgcID==pgc[i])
                               ##if selected[index][0]==1:
                                   ##File3 = fileRoot + filt + '.back' + sfx
                                   ##if not os.path.isfile(paths[3] +File3): 
                                       ##File3=fileRoot + filt + sfx                         
                           ##cmd = 'cp '+paths[3] +File3+' '+destination+'/'+File4
                           ##xcmd(cmd, True)
                           ##if filt=='_g':
                              ###print pgc[i]
                              ##no+=1
                       
                       ###### 2nd stage, choose the bests (comment this block for the stage 1)      
                       #if os.path.isfile(paths[3]+File1):
                         #if pgc[i] in pgcID2:
                            #index = np.where(pgcID2==pgc[i]) 
                            #if selected2[index][0]==1:
                                #q = 3
                                #File1 = fileRoot + filt + sfx
                                #File2 = fileRoot + filt + sfx
                                #if pgc[i] in pgcID:
                                    #index = np.where(pgcID==pgc[i])   # best from SDSS versions
                                    #if selected[index][0]==1:
                                        #if sfx=='.png': 
                                            #File1 = fileRoot + filt + '.back' + sfx
                                        #if not os.path.isfile(paths[3] +File1): 
                                            #File1=fileRoot + filt + sfx                         

#########################################################################################                           
                   #if filt=='_gri':
                     #has_gri=True
                   #if filt=='_r':
                     #has_r=True
                   #if filt=='_i':
                     #has_i=True                                                             
                   #if filt=='_g':
                     #has_g=True   
                     ##no+=1                
                     ###print pgc[i]
                   
                   ##if pgc[i]==69263 and filt=='_gri':
                       ##print paths[q] +File1
                       ##print destination+'/'+File2
                       ##sys.exit()
                     
                   #cmd = 'cp '+paths[q] +File1+' '+destination+'/'+File2
                   #xcmd(cmd, True)
                   #break
       
       #if has_g or has_r or has_i or has_gri:
           #no+=1       
                   
       #if not has_g and has_r:
           #cmd = 'cp '+destination+'/'+fileRoot+'_r.png '+destination+'/'+fileRoot+'_g.png '
           #xcmd(cmd, True)
       #elif not has_g and has_i:
           #cmd = 'cp '+destination+'/'+fileRoot+'_i.png '+destination+'/'+fileRoot+'_g.png '
           #xcmd(cmd, True)
       #elif not has_g and has_gri:
           #cmd = 'cp '+destination+'/'+fileRoot+'_gri.jpg '+destination+'/'+fileRoot+'_g.png '
           #xcmd(cmd, True)
           
#print no, All    

    

    
    

   
   
   
   










