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
def myPlot(ax, xFile, yFile, pcolor):

    table = np.genfromtxt(yFile , delimiter=',', filling_values=None, names=True, dtype=None)
    pgc_incout    = table['pgc']
    inc_incout    = table['inc']
    flag_incout   = table['flag']

    table = np.genfromtxt(xFile , delimiter=',', filling_values=None, names=True, dtype=None)
    pgc_brent    = table['pgc']
    inc_brent    = table['inc']
    flag_brent   = table['flag']

    pgc_common = []
    my_inc     = []
    th_inc     = []  # brent

    for i in range(len(pgc_brent)):
        
        if flag_brent[i]<=0 and pgc_brent[i] in pgc_incout:
            
            i_lst = np.where(pgc_incout == pgc_brent[i])
            if flag_incout[i_lst][0]<=0:

               my_inc.append(inc_incout[i_lst][0])
               pgc_common.append(pgc_brent[i])
               th_inc.append(inc_brent[i])


    th_inc = np.asarray(th_inc)
    my_inc = np.asarray(my_inc)
    ax.plot(th_inc, th_inc-my_inc, pcolor, ms=2, color='black')
######################################


        
        
        
fig = py.figure(figsize=(7, 5), dpi=100)
fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
ax = fig.add_subplot(111)    


#p1, = ax.plot([0,100], [0,100], color='black', linestyle='-', label="equality")
#p2, = ax.plot([0,100], [5,105], color='b', linestyle=':', label=r'$\pm5^o$')
#ax.plot([0,100], [-5,95], color='b', linestyle=':')
#p3, = ax.plot([0,100], [10,110], color='g', linestyle='--', label=r'$\pm10^o$')
#ax.plot([0,100], [-10,90], color='g', linestyle='--')


xFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_brent_calib.lst.output'
table = np.genfromtxt(xFile, delimiter=',', filling_values=None, names=True, dtype=None)
pgc_brent    = table['pgc']
inc_brent    = table['inc']
flag_brent   = table['flag']

lst = []
for i in range(len(pgc_brent)):
    if flag_brent[i]==0 and inc_brent[i]>0:
        lst.append([pgc_brent[i], [inc_brent[i]]])
        

###########################################################################
xFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_ehsan_calib.lst.output'
table = np.genfromtxt(xFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc    = table['pgc']
inc    = table['inc']
flag   = table['flag']
for i in range(len(pgc_brent)):
    if pgc_brent[i] in pgc:
        i_lst = np.where(pgc == pgc_brent[i])
        if flag[i_lst][0]==0:
            for j in range(len(lst)):
                if lst[j][0]==pgc_brent[i]:
                    if inc[i_lst][0]>0:
                        lst[j][1].append(inc[i_lst][0])
                    break
###########################################################################
xFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_amber_calib.lst.output'
table = np.genfromtxt(xFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc    = table['pgc']
inc    = table['inc']
flag   = table['flag']
for i in range(len(pgc_brent)):
    if pgc_brent[i] in pgc:
        i_lst = np.where(pgc == pgc_brent[i])
        if flag[i_lst][0]==0:
            for j in range(len(lst)):
                if lst[j][0]==pgc_brent[i]:
                    if inc[i_lst][0]>0:
                        lst[j][1].append(inc[i_lst][0])
                    break
###########################################################################
xFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_arash_calib.lst.output'
table = np.genfromtxt(xFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc    = table['pgc']
inc    = table['inc']
flag   = table['flag']
for i in range(len(pgc_brent)):
    if pgc_brent[i] in pgc:
        i_lst = np.where(pgc == pgc_brent[i])
        if flag[i_lst][0]==0:
            for j in range(len(lst)):
                if lst[j][0]==pgc_brent[i]:
                    if inc[i_lst][0]>0:
                        lst[j][1].append(inc[i_lst][0])
                    break
###########################################################################
###########################################################################
xFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_lexie_calib.lst.output'
table = np.genfromtxt(xFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc    = table['pgc']
inc    = table['inc']
flag   = table['flag']
for i in range(len(pgc_brent)):
    if pgc_brent[i] in pgc:
        i_lst = np.where(pgc == pgc_brent[i])
        if flag[i_lst][0]==0:
            for j in range(len(lst)):
                if lst[j][0]==pgc_brent[i]:
                    if inc[i_lst][0]>0:
                        lst[j][1].append(inc[i_lst][0])
                    break
###########################################################################
###########################################################################
xFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_chase_calib.lst.output'
table = np.genfromtxt(xFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc    = table['pgc']
inc    = table['inc']
flag   = table['flag']
for i in range(len(pgc_brent)):
    if pgc_brent[i] in pgc:
        i_lst = np.where(pgc == pgc_brent[i])
        if flag[i_lst][0]==0:
            for j in range(len(lst)):
                if lst[j][0]==pgc_brent[i]:
                    if inc[i_lst][0]>0:
                        lst[j][1].append(inc[i_lst][0])
                    break
###########################################################################


for i in range(len(lst)):
   lst[i].append(np.median(lst[i][1]))
   #lst[i].append(lst[i][1][0])  # brent
   
   
for i in range(len(lst)):
   if len(lst[i][1])>3:
       for inc in lst[i][1]:
           med = lst[i][2]
           #ax.plot([med], [inc-med], '.', ms=1, color='black')
       #ax.plot([med], [lst[i][1][0]-med], 'r.')



Linc=[]
Linc_err=[]
LincY=[]
for incl in np.arange(40,90,2):
    Linc.append(incl+1)
    
    el=[]
    for l in lst:
        if len(l[1])>3 and l[2]>incl and l[2]<=incl+2.:
            el+=l[1]
    Linc_err.append(np.std(el))
    LincY.append(np.median(el))
    
    
Linc=np.asarray(Linc) 
Linc_err=np.asarray(Linc_err) 
LincY=np.asarray(LincY)  
#ax.errorbar(Linc, 0.*Linc, yerr=Linc_err, fmt='o')    
##ax.errorbar(Linc, LincY-Linc, yerr=Linc_err, fmt='o')  



for i in range(len(lst)):
   print lst[i]



###########################################################################
xFile = '/home/ehsan/PanStarrs/INClinationCode/pgc_chase_calib.lst.output'
table = np.genfromtxt(xFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc    = table['pgc']
inc    = table['inc']
flag   = table['flag']

incX= []
incY= []

for i in range(len(lst)):
    if len(lst[i][1])>3 and lst[i][0] in pgc:
        i_lst = np.where(pgc == lst[i][0])
        if flag[i_lst][0]==0 and inc[i_lst][0]>0:
            incX.append(lst[i][2])
            incY.append(inc[i_lst][0])
incX=np.asarray(incX)
incY=np.asarray(incY)
ax.plot(incX,incY-incX, '.', ms=2, color='black')  


Linc=[]
Linc_err=[]
LincY=[]
for incl in np.arange(40,90,2):
    Linc.append(incl+1)
    
    el=[]
    for i in range(len(incX)):
        if incX[i]>incl and incX[i]<=incl+2.:
            el.append(incY[i]-incX[i])
    el=np.asarray(el)
    Linc_err.append(np.std(el))
    LincY.append(np.median(el))
    
    
    
Linc=np.asarray(Linc) 
Linc_err=np.asarray(Linc_err) 
LincY=np.asarray(LincY)  
ax.errorbar(Linc, LincY, yerr=Linc_err, fmt='o', color='green') 


delta=incY-incX
ave = np.median(delta)
std = np.std(delta)
ax.plot([0,100], [ave,ave], color='b', linestyle='--')   
ax.plot([0,100], [ave+std,ave+std], color='g', linestyle=':')  
ax.plot([0,100], [ave-std,ave-std], color='g', linestyle=':')  


ax.text(35,-24, r'$\sigma: \pm$'+"%.1f" % (std)+r'$^o$')
ax.text(35,-19, r'$offset: $'+"%.1f" % (ave)+r'$^o$')

ax.set_xlim([30,100])
ax.set_ylim([-30,30])


ax.set_xlabel('Inc. (Median) [deg]', fontsize=14)
ax.set_ylabel('Inc. (Chase-Median) [deg]', fontsize=14)
###########################################################################


##################################################
inFile = 'Wise_calib_visier.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_wise_vizier    = table['PGC']
inc_wise_vizier    = table['i']
##################################################
incX= []
incY= []
pgc_common=[]
for i in range(len(lst)):
    if len(lst[i][1])>3 and lst[i][0] in pgc_wise_vizier:
        i_lst = np.where(pgc_wise_vizier == lst[i][0])
        incX.append(lst[i][2])  # median
        incY.append(inc_wise_vizier[i_lst][0])
        pgc_common.append(lst[i][0])
incX=np.asarray(incX)
incY=np.asarray(incY)
#ax.plot(incX,incY-incX, 'g.', picker=5)   

ave = np.median(incY-incX)
std = np.std(incY-incX)
#ax.plot([0,100], [ave,ave], color='b', linestyle='--')   
#ax.plot([0,100], [ave+std,ave+std], color='g', linestyle=':')  
#ax.plot([0,100], [ave-std,ave-std], color='g', linestyle=':')  


#ax.text(35,-20, r'$\sigma: \pm$'+"%.1f" % (std)+r'$^o$')
#ax.text(35,-16, r'$offset: $'+"%.1f" % (ave)+r'$^o$')

#ax.set_xlabel('Inc. (Median) [deg]', fontsize=14)
#ax.set_ylabel('Inc. (Neil+14-Median) [deg]', fontsize=14)
###########################################################################
incX= []
incY= []
pgc_common=[]
for i in range(len(pgc_brent)):
    if flag_brent[i]==0 and inc_brent[i]>0 and pgc_brent[i] in pgc_wise_vizier:
        i_lst = np.where(pgc_wise_vizier == pgc_brent[i])
        incX.append(inc_brent[i])
        incY.append(inc_wise_vizier[i_lst][0])
        pgc_common.append(pgc_brent[i])
incX=np.asarray(incX)
incY=np.asarray(incY)
#ax.plot(incX,incX-incY, 'b.', picker=5)   


#ave = np.median(incY-incX)
#std = np.std(incY-incX)
#ax.plot([0,100], [ave,ave], color='b', linestyle='--')   
#ax.plot([0,100], [ave+std,ave+std], color='g', linestyle=':')  
#ax.plot([0,100], [ave-std,ave-std], color='g', linestyle=':')  


#ax.text(35,11, r'$\sigma: \pm$'+"%.1f" % (std)+r'$^o$')
#ax.text(35,15, r'$offset: $'+"%.1f" % (ave)+r'$^o$')
    
#ax.set_xlabel('Inc. (Brent) [deg]', fontsize=14)
#ax.set_ylabel('Inc. (Neil+14-Brent) [deg]', fontsize=14)    
###########################################################################


pgc_common = np.asarray(pgc_common)
def onpick(event):
    ind = event.ind

    print 'pgc', pgc_common[ind]

fig.canvas.mpl_connect('pick_event', onpick)

###########################################################################

ax.set_xlim([30,100])
#ax.set_ylim([20,100])


###########################################################################

plt.show()

    

    
    

   
   
   
   










