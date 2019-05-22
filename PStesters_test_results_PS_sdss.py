#!/usr/bin/python
import sys
import os.path
import subprocess
import glob
import numpy as np
from astropy.table import Table, Column 
import pyfits
import pylab as py
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter



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
##########################################
    
def read_file(fname, n_skip = 1, seprator = ','):
  
                # how columns are seprated
  
  list_name = []
  list_ra   = []
  list_dec  = []
  list_a    = []
  list_b    = []
  list_pa   = []
  list_ty   = []
  
  line_no = 0
  for line in open(fname, 'r+'):
    
    columns = line.split(seprator)
    
    line_no+=1
    if len(columns) >= 2:
        
        if line_no>n_skip: 
	  
	  n = 0
	  i = 0
	  while n < len(columns):
	    
	    if columns[n] != '' and i==0:
	       list_name.append(columns[n])
	       i+=1
	       n+=1
	       continue
	    
	    if columns[n] != '' and i==1:
	       list_ra.append(float(columns[n]))
	       i+=1
	       n+=1
	       continue       
	    if columns[n] != '' and i==2:
	       list_dec.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue
	    if columns[n] != '' and i==3:
	       list_a.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==4:
	       list_b.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==5:
	       list_pa.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==6:
	       type = columns[n]
	       type = type[0:len(type)-1]
	       list_ty.append(type)
	       i+=1
	       n+=1
	       continue	     	     
	    n+=1

  
  list_name = np.asarray(list_name)
  list_ra   = np.asarray(list_ra)
  list_dec  = np.asarray(list_dec)
  list_a    = np.asarray(list_a)
  list_b    = np.asarray(list_b)
  list_pa   = np.asarray(list_pa)
  list_ty   = np.asarray(list_ty)
  
  return list_name, list_ra, list_dec, list_a, list_b, list_pa, list_ty
#################################################################
def pgc_n(pgc_id):
  
  n = len(pgc_id)
  return int(pgc_id[3:n])
#################################################################
#################################################################
def read_mag(pgc, ra, filters=['g','r','i'], sdss=None, ps=None):
  
  db_root = '/home/ehsan/db_esn/data/'
  db_id = ra_db(ra)
  
  if sdss==1: 
    pgc_id = 'pgc'+str(pgc)
  elif ps==1:
    pgc_id = 'PS_pgc'+str(pgc)
 
  m = len(filters)
  mags = np.zeros(m)
  
  for p in range(m):
    
   filter = filters[p]
   photometry =  db_root+db_id+'/photometry/'+pgc_id+'_'+filter+'_asymptotic.dat'
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
	    mags[p] = np.float(thing)
	  counter+=1
  
  return mags
#################################################################
def read_note(pgc, ra, sdss=None, ps=None):
  
  db_root = '/home/ehsan/db_esn/data/'
  db_id = ra_db(ra)
  
  if sdss==1: 
    pgc_id = 'pgc'+str(pgc)
    srvy = 'sdss'
  elif ps==1:
    pgc_id = 'PS_pgc'+str(pgc)
    srvy = 'panstarrs'    
 
  qa_note =  db_root+db_id+'/'+srvy+'/fits/'+pgc_id+'_qa.txt'
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
  
#################################################################

fname = 'New_era/PStesters_sdss.glga'
list_name, list_ra, list_dec, list_a, list_b, list_pa, list_ty = read_file(fname, n_skip = 0, seprator = ' ')

inFile  = 'New_era/edd_HI_ba_T_9060.short.csv'
table   = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
d25     = table['d25']
PGC     = table['PGC']



ignore = [40761,23519,64552,62651,60049,24469,90968,61254,4010299,38457,142843,91191,39833,48409,1672298,1305231,61220,60436,53891]


new_ID  = []
new_D25 = []
new_g_ps = []
new_r_ps = []
new_g_sdss = []
new_r_sdss = []
my_count = 0
for i in range(len(list_name)):
  

  ID = pgc_n(list_name[i])    # integer
  
  ind = np.where(PGC==ID)
  RA  = list_ra[i]
  DEC = list_dec[i]
  D25 = d25[ind][0]
  
  mags_ps = read_mag(ID, RA, filters=['g','r', 'i', 'z'], ps=1)
  g_ps    = mags_ps[0]
  r_ps    = mags_ps[1]
  i_ps    = mags_ps[2]
  z_ps    = mags_ps[3]
  note_ps = read_note(ID, RA, ps=1)
  
  
  mags_sdss = read_mag(ID, RA, filters=['g','r', 'i', 'z'], sdss=1)
  g_sdss    = mags_sdss[0]
  r_sdss    = mags_sdss[1]
  i_sdss    = mags_sdss[2]
  z_sdss    = mags_sdss[3]
  note_sdss = read_note(ID, RA, sdss=1)  
  
  db_root = '/home/ehsan/db_esn/data/'
  db_id = ra_db(RA)
  
  
  if g_ps!=0 and not ID in ignore:
    s= ''
    s += str(my_count+1) + ", " 
    s += str(ID) + ", " 
    s += str(D25) + ", " 
    s += '{:.5f}'.format(RA) + ", " 
    s += '{:.5f}'.format(DEC) + ", " 
    s += '{:.2f}'.format(g_sdss) + ", " 
    s += '{:.2f}'.format(r_sdss) + ", " 
    s += '{:.2f}'.format(i_sdss) + ", " 
    s += '{:.2f}'.format(z_sdss) + ", " 
    s += '{:.2f}'.format(g_ps) + ", " 
    s += '{:.2f}'.format(r_ps) + ", " 
    s += '{:.2f}'.format(i_ps) + ", " 
    s += '{:.2f}'.format(z_ps)   
    my_count += 1
    print s

  

  #s = ''
  #s += "|| " + str(i+1) + " " 
  #s += " || " + str(ID)
  #s += " || " + str(D25)
  ##s += " || " + '{:.5f}'.format(RA)
  ##s += " || " + '{:.5f}'.format(DEC)
  
  #if g_sdss != 0 :
    #s += " || " + '{:.2f}'.format(g_sdss)
  #else: s += " || "
  #if r_sdss != 0 : s += " || " + '{:.2f}'.format(r_sdss) 
  #else: s += " || "
  #s += " || [http://www.ifa.hawaii.edu/~ehsan/test/" + 'pgc'+str(ID)
  #s += "_sdss_profile.jpg profile]  ||  [http://www.ifa.hawaii.edu/~ehsan/test/" + 'pgc'+str(ID)
  #s += "_sdss_images.jpg images]  || " 
  #s += " || " + note_sdss  
  #s += " || " + ' * '
  #if g_ps!=0: s += " || " + '{:.2f}'.format(g_ps)
  #else: s += " || "
  #if r_ps!=0 : s += " || " + '{:.2f}'.format(r_ps)
  #else: s += " || "
  #s += " || [http://www.ifa.hawaii.edu/~ehsan/test/" + 'PS_pgc'+str(ID)
  #s += "_panstarrs_profile.jpg profile]  ||  [http://www.ifa.hawaii.edu/~ehsan/test/" + 'PS_pgc'+str(ID)
  #s += "_panstarrs_images.jpg images]  || " 
  #s += " || " + note_ps
  #s += " || " + ' * '  
  #print s
  
 


  #pgc_id = 'PS_pgc'+str(ID)
  #fname1 = db_root+db_id+'/plots/'+pgc_id+'_panstarrs_images.jpg'
  #command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/test/']
  #subprocess.call(command)
  #fname1 = db_root+db_id+'/plots/'+pgc_id+'_panstarrs_profile.jpg'
  #command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/test/']
  #subprocess.call(command)
  
  #pgc_id = 'pgc'+str(ID)
  #fname1 = db_root+db_id+'/plots/'+pgc_id+'_sdss_images.jpg'
  #command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/test/']
  #subprocess.call(command)
  #fname1 = db_root+db_id+'/plots/'+pgc_id+'_sdss_profile.jpg'
  #command = ["cp", fname1, '/home/ehsan/PanStarrs/Jan/HI/test/']
  #subprocess.call(command)  
  
###################################################



  if not ID in ignore:
    new_ID.append(ID)
    new_D25.append(D25)
    new_g_ps.append(g_ps)
    new_r_ps.append(r_ps)
    new_g_sdss.append(g_sdss)
    new_r_sdss.append(r_sdss)
    
    

print len(new_ID)
new_ID = np.asarray(new_ID)
new_D25 = np.asarray(new_D25)
new_g_ps = np.asarray(new_g_ps)
new_r_ps = np.asarray(new_r_ps)
new_g_sdss = np.asarray(new_g_sdss)
new_r_sdss = np.asarray(new_r_sdss) 
###################################################

fig = py.figure(figsize=(7, 5), dpi=100)
fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
ax = fig.add_subplot(111)
plt.tick_params(which='major', length=7, width=1.5)
plt.tick_params(which='minor', length=4, color='#000033', width=1.0) 


ax.plot([0,20], [-0.05,-0.05], ':', color='blue')
ax.plot([0,20], [+0.05,+0.05], ':', color='blue')
ax.plot([0,20], [-0.1,-0.1], ':', color='red')
ax.plot([0,20], [+0.1,+0.1], ':', color='red')
ax.plot([0,20], [0,0], '--', color='black')

ax.set_ylim([-0.4,0.4])
ax.set_xlim([9,18])

#ax.set_xlabel('g-mag (SDSS)', fontsize=14)
#ax.set_ylabel(r'$\Delta$'+'g (SDSS - PS)', fontsize=14)
#col = 'green'
#x_ax =  new_g_sdss
#y_ax = new_g_sdss-new_g_ps


#ax.set_xlabel('r-mag (SDSS)', fontsize=14)
#ax.set_ylabel(r'$\Delta$'+'r (SDSS - PS)', fontsize=14)
#col = 'red'
#x_ax =  new_r_sdss
#y_ax = new_r_sdss-new_r_ps


#ax.set_xlabel('d25 (arcmin)', fontsize=14)
#ax.set_ylabel(r'$\Delta$'+'g (SDSS - PS)', fontsize=14)
#col = 'green'
#x_ax =  new_D25
#y_ax = new_g_sdss-new_g_ps
#ax.set_xlim([0,2])

#ax.set_xlabel('d25 (arcmin)', fontsize=14)
#ax.set_ylabel(r'$\Delta$'+'r (SDSS - PS)', fontsize=14)
#col = 'red'
#x_ax =  new_D25
#y_ax = new_r_sdss-new_r_ps
#ax.set_xlim([0,2])


ax.set_xlabel('d25 (arcmin)', fontsize=14)
ax.set_ylabel(r'$\Delta$'+'(g-r) (SDSS - PS)', fontsize=14)
col = 'blue'
x_ax = new_D25
y_ax = (new_g_sdss-new_r_sdss) - (new_g_ps-new_r_ps)
ax.set_xlim([0,2])
ax.set_ylim([-0.4,0.4])


ax.plot(x_ax, y_ax, 'o', color=col, markersize=4, picker=5)



def onpick(event):
    ind = event.ind
    print 'pgc', new_ID[ind]

fig.canvas.mpl_connect('pick_event', onpick)


#plt.show()
###################################################

  
  
  
  
  
  
  
  



