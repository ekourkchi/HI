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

#datasets = ['data_set_21.glga', 'data_set_41.glga', 'PStesters_sdss.glga', 'pilot_01.glga', 'pilot_02.glga', 'pilot_03.glga', 'data_set_31.glga', 'data_set_22.glga', 'data_summer_1.glga', 'data_summer_8.glga'] 


#destination = '/home/ehsan/PanStarrs/EDD_server/public_html/cf4_photometry/sdss_photometry/'

destination = '/var/run/media/ehsan/HOURI/tst/'

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

datasets.append('data_summer_8.glga')
locations.append('/home/ehsan/db_esn/DONE_DATA/data_summer_8/')




datasets.append('data_summer_16.glga')
locations.append('/home/ehsan/db_esn/data_summer_16/')

datasets.append('data_set_11.glga')
locations.append('/home/ehsan/db_esn/data_set_11/')

datasets.append('data_set_51.glga')
locations.append('/home/ehsan/db_esn/data_set_51/')


########################################################################
########################################################################
########################################################################

#gal_lst = []
#gal_g   = []
#gal_r   = []
#gal_i   = []
#guals   = []
#gal_i_hall = []
#semimajor_lst = []
#semiminor_lst = []

#inFile = 'Hall_sdss/Hall.SDSS.EDDtable04Feb2016.txt'
#table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
#pgc_hall      = table['PGC']
#m_ext_hall    = table['m_ext']


#for index in range(len(datasets)):

        #dataset = datasets[index]
        #location = locations[index]
        #pgcname, radb = read_glga('New_era/'+dataset)
         

        #for i in range(len(pgcname)):
            
            #directory = destination+pgcname[i]
            #isDirAvailable =  os.path.isdir(directory)
            
            #if not int(pgcname[i][3:])  in gal_lst:
                
                
                #photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_i_asymptotic.dat'
                #if os.path.exists(photometry):
                    
                    #gal_pgc = int(pgcname[i][3:])
                    
                    
                    #ii = get_mag(photometry)
                    
                    
                    #photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_g_asymptotic.dat'
                    #gg = get_mag(photometry)
                    


                    #photometry =  location + radb[i] +'/photometry/'+pgcname[i]+'_r_asymptotic.dat'
                    #rr = get_mag(photometry)
                    
                    
                    #qa_txt = location + radb[i] + '/sdss/fits/' + pgcname[i]+'_qa.txt'
                    #qual = get_quality(qa_txt)
                    
                    #ellipsefile = location + radb[i] +'/photometry/'+pgcname[i]+'_i_ellipsepar.dat'
                    #ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse(ellipsefile)
                    
                    
                    ##gal_i_hall.append(ii)
                    ##gal_lst.append(gal_pgc)
                    ##gal_g.append(gg)
                    ##gal_r.append(rr)
                    ##gal_i.append(ii)
                    ##guals.append(qual)
                    ##semimajor_lst.append(semimajor/60)    # arcmin
                    ##semiminor_lst.append(semiminor/60)    # arcmin                    

                    #for j in range(len(pgc_hall)):
                        #if pgc_hall[j] == gal_pgc:
                            #gal_i_hall.append(m_ext_hall[j])
                            #gal_lst.append(gal_pgc)
                            #gal_g.append(gg)
                            #gal_r.append(rr)
                            #gal_i.append(ii)
                            #guals.append(qual)
                            #semimajor_lst.append(semimajor/60)    # arcmin
                            #semiminor_lst.append(semiminor/60)    # arcmin

                            #break



            

#gal_lst = np.asarray(gal_lst)
#gal_g = np.asarray(gal_g)
#gal_r = np.asarray(gal_r)
#gal_i = np.asarray(gal_i)
#gal_i_hall = np.asarray(gal_i_hall)
#guals  = np.asarray(guals)
#semimajor_lst = np.asarray(semimajor_lst)
#semiminor_lst = np.asarray(semiminor_lst)


#index = np.where(guals>3)
#gal_lst = gal_lst[index]
#gal_g = gal_g[index]
#gal_r = gal_r[index]
#gal_i = gal_i[index]
#gal_i_hall = gal_i_hall[index]
#guals = guals[index]
#semimajor_lst = semimajor_lst[index]
#semiminor_lst = semiminor_lst[index]

#index = np.argsort(gal_lst)
#gal_lst = gal_lst[index]
#gal_g = gal_g[index]
#gal_r = gal_r[index]
#gal_i = gal_i[index]
#gal_i_hall = gal_i_hall[index]
#guals = guals[index]
#semimajor_lst = semimajor_lst[index]
#semiminor_lst = semiminor_lst[index]

##myTable = Table()
##myTable.add_column(Column(data=gal_lst, name='pgc'))
##myTable.add_column(Column(data=gal_g, name='g', format='%0.2f'))
##myTable.add_column(Column(data=gal_r, name='r', format='%0.2f'))
##myTable.add_column(Column(data=gal_i, name='i', format='%0.2f'))
##myTable.add_column(Column(data=semimajor_lst, name='a', format='%0.2f'))
##myTable.add_column(Column(data=semiminor_lst, name='b', format='%0.2f'))
##myTable.add_column(Column(data=gal_i_hall, name='m_ext', format='%0.2f'))
##myTable.write('sdss_cf4_hall.csv', format='ascii.fixed_width',delimiter='|', bookend=False) 
##myTable.write('sdss_cf4_sofar.csv', format='ascii.fixed_width',delimiter='|', bookend=False) 


#fig = py.figure(figsize=(7, 5), dpi=100)
#fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
#ax = fig.add_subplot(111)
#plt.tick_params(which='major', length=7, width=1.5)
#plt.tick_params(which='minor', length=4, color='#000033', width=1.0) 

#ax.plot([0,100], [-0.05,-0.05], ':', color='blue')
#ax.plot([0,100], [+0.05,+0.05], ':', color='blue')
#ax.plot([0,100], [-0.1,-0.1], ':', color='red')
#ax.plot([0,100], [+0.1,+0.1], ':', color='red')
#ax.plot([0,100], [0,0], '--', color='black')

#ax.plot(semimajor_lst, gal_i-gal_i_hall, 'o', color='orange', markersize=4, picker=5)

##ax.set_ylim([-0.7,0.7])

### when x-axis is size (arcmin)
#ax.set_xlim([0.2,10])
#ax.set_xscale("log")

##ax.set_xlabel('i-mag (cf4)', fontsize=14)

### size
#ax.set_xlabel('semimajor cf4 [arcmin]', fontsize=14)

#ax.set_ylabel(r'$\Delta$'+'i (cf4-hall)', fontsize=14)



#def onpick(event):
    #ind = event.ind
    #print 'pgc', gal_lst[ind], guals[ind]

#fig.canvas.mpl_connect('pick_event', onpick)



#plt.show()
########################################################################
########################################################################
########################################################################



            
            
            #if not isDirAvailable:
                #xcmd('mkdir '+directory, True)
            
            
            #with cd(directory):
                
                #cmd = 'cp '+ location + radb[i] + '/sdss/fits/' + pgcname[i] + '_qa.txt .'
                #xcmd(cmd, True)
                
                #cmd = 'cp '+ location + radb[i] + '/plots/' + pgcname[i] + '_sdss_images.jpg .'
                #xcmd(cmd, True)
            
                #cmd = 'cp '+ location + radb[i] + '/plots/' + pgcname[i] + '_sdss_profile.jpg .'
                #xcmd(cmd, True)





