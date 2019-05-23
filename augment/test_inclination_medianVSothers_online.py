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
#import pyfits



######################################
def addNote(note, text):
    
    if text=='': return note
    
    if note=='':
        note = '['+text+']'
    else:
        note = note+' '+'['+text+']'
    
    return note
    

def addConcern(note, cncrn):
    
    if cncrn[0]>0: note = addNote(note, 'not_sure')
    if cncrn[1]>0: note = addNote(note, 'better_image')
    if cncrn[2]>0: note = addNote(note, 'bad_TF')
    if cncrn[3]>0: note = addNote(note, 'ambiguous')
    if cncrn[4]>0: note = addNote(note, 'disturbed')
    if cncrn[5]>0: note = addNote(note, 'HI')
    if cncrn[6]>0: note = addNote(note, 'face_on')
    if cncrn[7]>0: note = addNote(note, 'not_spiral')
    if cncrn[8]>0: note = addNote(note, 'multiple')
    return note
######################################
#######################################
def getINC(exclude_Email=[]):
    
    #### Manoa
    inFile = 'EDD.inclination.All.Manoa.22May2019172954.txt'
    table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
    pgc_incout    = table['pgcID']
    inc_incout    = table['inc']
    flag_incout   = table['flag']
    note          = [' '.join(dummy.split()) for dummy in table['note']]
    email         = [' '.join(dummy.split()) for dummy in table['email']]
    NS = table['not_sure']
    BI = table['better_image']
    TF = table['bad_TF']
    AM = table['ambiguous']
    DI = table['disturbed']
    HI = table['HI']
    FO = table['face_on']
    NP = table['not_spiral']
    MU = table['multiple']
    
    #### Guest
    inFile = 'EDD.inclination.All.Guest.22May2019173010.txt'
    table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
    pgc_incout_    = table['pgcID']
    inc_incout_    = table['inc']
    flag_incout_   = table['flag']
    note_          = [' '.join(dummy.split()) for dummy in table['note']]
    email_         = [' '.join(dummy.split()) for dummy in table['email']]
    NS_ = table['not_sure']
    BI_ = table['better_image']
    TF_ = table['bad_TF']
    AM_ = table['ambiguous']
    DI_ = table['disturbed']
    HI_ = table['HI']
    FO_ = table['face_on']
    NP_ = table['not_spiral']
    MU_ = table['multiple']
    
    
    #eMails = ['rbtully1@gmail.com','ekourkchi@gmail.com','s.eftekharzadeh@gmail.com']

    PGC = []
    for i in range(len(pgc_incout)):
        if not pgc_incout[i] in PGC:
            PGC.append(pgc_incout[i])
    for i in range(len(pgc_incout_)):
        if not pgc_incout_[i] in PGC:
            PGC.append(pgc_incout_[i])        
            
            
    incDict = {}
    for i in range(len(PGC)):   
        
        data = {}
        
        indx = np.where(PGC[i] == pgc_incout)
        for j in indx[0]:
            if not email[j] in data.keys() and not email[j] in exclude_Email:
                data[email[j]] = [inc_incout[j],flag_incout[j],note[j], [NS[j], BI[j], TF[j], AM[j], DI[j], HI[j], FO[j], NP[j], MU[j]]]

        indx = np.where(PGC[i] == pgc_incout_)
        for j in indx[0]:
            if not email_[j] in data.keys() and not email_[j] in exclude_Email:
                data[email_[j]] = [inc_incout_[j],flag_incout_[j],note_[j], [NS_[j], BI_[j], TF_[j], AM_[j], DI_[j], HI_[j], FO_[j], NP_[j], MU_[j]]]

        incDict[PGC[i]] = data
        
        
    return incDict   
###########################################################          
######################################
def incMedian(incDic):
    
    boss = 'rbtully1@gmail.com'
    #boss = 'ekourkchi@gmail.com'
    
    flag = 0
    inc  = 0
    note = ''
    stdev = 0
    n = 0   # number of good measurments
    concerns = np.zeros(9)
    
    if boss in incDic.keys():
        
        if incDic[boss][1] != 0:  # boss has flagged it
            
            flag = 1
            for email in incDic:
                if incDic[email][1]==1:
                   note =  addNote(note, incDic[email][2])
                   concerns+=np.asarray(incDic[email][3])
                   n+=1
        
        else:  # boss has NOT flagged it
            
            flag = 0
            incs = []
            for email in incDic:
                if incDic[email][1]==0:
                    incs.append(incDic[email][0])
                    note = addNote(note, incDic[email][2])
                    n+=1

            inc = np.median(incs)
            stdev = np.std(incs)
        
    else:
        flag = []
        for email in incDic:
            flag.append(incDic[email][1])
        flag = np.median(flag)
        if flag > 0: flag =1
        
        incs = []
        for email in incDic:
            if incDic[email][1]==flag:
               incs.append(incDic[email][0])
               note = addNote(note, incDic[email][2])
               concerns+=np.asarray(incDic[email][3])
               n+=1
        inc = np.median(incs)
        stdev = np.std(incs)
    
    note = addConcern(note, concerns)
    
    return inc, stdev, flag, note, n

#######################################


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



#myEmail = 's.eftekharzadeh@gmail.com' ; name='Sarah'
myEmail = 'ekourkchi@gmail.com' ; name='Ehsan'
#myEmail = 'mokelkea@hawaii.edu' ; name='Amber'
#myEmail =  'dschoen@hawaii.edu' ; name='Devin'
#myEmail =  'chasemu@hawaii.edu' ; name='Chase'
#myEmail =  'jrl2014@hawaii.edu' ; name='Jordan'
#myEmail =  'adholtha@hawaii.edu' ; name='Lexie'
#myEmail =  'chuangj@hawaii.edu' ; name='Juana'
#myEmail =  'mka7@hawaii.edu' ; name='Mike'
#myEmail =  'rbtully1@gmail.com' ; name='Brent'
#myEmail =  'a.danesh61@gmail.com' ; name='Arash'


#myEmail =  'arnaud.ohet@gmail.com' ; name='Arnaud'
#myEmail =  'pascal.jouve@free.fr' ; name='Pascal'
#myEmail =  'cgrubner0@gmail.com' ; name='Charles'
#myEmail =  'fredwallet@gmail.com' ; name='Fred'
#myEmail =  'dlsaintsorny@gmail.com' ; name='Daniel'
#myEmail =  'echarraix69@gmail.com' ; name='Emmanuel'
#myEmail =  'helenecourtois33@gmail.com' ; name='Helene'
#myEmail =  'hawaii@udrea.fr' ; name='Denis'
#myEmail =  'bergeravier@gmail.com' ; name='Ravier'
#myEmail =  'henri140860@wanadoo.fr' ; name='Henri'
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''
#myEmail =  '' ; name=''





inFile = 'EDD.inclination.All.Manoa.22May2019172954.txt'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_incout_    = table['pgcID']
inc_incout_    = table['inc']
flag_incout_   = table['flag']
email_   = table['email']


pgc_incout = []
inc_incout = []
flag_incout = []

pgc_incout_eval = []
inc_incout_eval = []
flag_incout_eval = []

for i in range(len(pgc_incout_)):
    email_[i] = ' '.join(email_[i].split())
    if email_[i]== myEmail:
        
        pgc_incout.append(pgc_incout_[i])
        inc_incout.append(inc_incout_[i])
        flag_incout.append(flag_incout_[i])
        
        
inFile = 'EDD.inclination.All.Guest.22May2019173010.txt'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_incout_    = table['pgcID']
inc_incout_    = table['inc']
flag_incout_   = table['flag']
email_   = table['email']
inputTable   = table['inputTable']

pq = 0
for i in range(len(pgc_incout_)):
    email_[i] = ' '.join(email_[i].split())
    if email_[i]== myEmail:
        
        pgc_incout.append(pgc_incout_[i])
        inc_incout.append(inc_incout_[i])
        flag_incout.append(flag_incout_[i])  
        
        if  ' '.join(inputTable[i].split()) == 'Input_Guest_test_calib':
            pgc_incout_eval.append(pgc_incout_[i])
            inc_incout_eval.append(inc_incout_[i])
            flag_incout_eval.append(flag_incout_[i])             
             
        if  ' '.join(inputTable[i].split()) == 'Input_Guest':
            pq+=1
        
        


pgc_incout = np.asarray(pgc_incout)
inc_incout = np.asarray(inc_incout)
flag_incout = np.asarray(flag_incout)

pgc_incout_eval = np.asarray(pgc_incout_eval)
inc_incout_eval = np.asarray(inc_incout_eval)
flag_incout_eval = np.asarray(flag_incout_eval)


print len(pgc_incout)


incDic = getINC(exclude_Email=myEmail)
#incDic = getINC()


pgc_common = []
my_inc     = []
th_inc     = []  # median

pgc_common_eval = []
my_inc_eval     = []
th_inc_eval    = []  # median


for i in range(len(pgc_incout)):
    
    inc, stdev, flag, note, n = incMedian(incDic[pgc_incout[i]])        
    if flag_incout[i]==0 and flag==0 and n>=1:

           my_inc.append(inc_incout[i])
           pgc_common.append(pgc_incout[i])
           th_inc.append(inc)
           
           if pgc_incout[i] in pgc_incout_eval:
               my_inc_eval.append(inc_incout[i])
               pgc_common_eval.append(pgc_incout[i])
               th_inc_eval.append(inc)               
           
           
print len(pgc_common)
print "Input_Guest: ", pq
        
        
        
fig = py.figure(figsize=(7, 5), dpi=100)
fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
ax = fig.add_subplot(111)    

#ax.plot(th_inc, my_inc, 'o', mfc='white', picker=5, alpha=1.0, color='green')
#ax.plot(th_inc_eval, my_inc_eval, 'g.', picker=5, alpha=1.0,  markersize=10)

ax.plot(th_inc, my_inc, 'g.', picker=5, alpha=0.3)

p1, = ax.plot([0,100], [0,100], color='black', linestyle='-', label="equality")
p2, = ax.plot([0,100], [5,105], color='b', linestyle=':', label=r'$\pm5^o$')
ax.plot([0,100], [-5,95], color='b', linestyle=':')
p3, = ax.plot([0,100], [10,110], color='r', linestyle='--', label=r'$\pm10^o$')
ax.plot([0,100], [-10,90], color='r', linestyle='--')



pgc_common = np.asarray(pgc_common)
th_inc = np.asarray(th_inc)
my_inc = np.asarray(my_inc)

N = len(th_inc)
a1 = np.zeros(N)
a2 = np.zeros(N)


a1[np.where(th_inc<80)] = 1
a2[np.where(th_inc>60)] = 1
a = a1 + a2

index = np.where(a==2)
th_inc = th_inc[index]
my_inc = my_inc[index]

delta = th_inc-my_inc
std = np.std(delta)
rms = np.sqrt(np.mean(delta**2))

ax.set_xlim([20,100])
ax.set_ylim([20,100])
ax.text(23,80, r'$RMS: $'+"%.1f" % (rms)+r'$^o$')
#ax.text(30,90, r'$\sigma: $'+"%.1f" % (std)+r'$^o$')
#ax.set_xlabel('Inc. (Meidan) [deg]', fontsize=14)
#ax.set_ylabel('Inc. ('+name+') [deg]', fontsize=14)
ax.set_xlabel('Inclination [deg]', fontsize=14)
ax.set_ylabel('Inclination [deg]', fontsize=14)
ax.text(85,30, name, size=16, color='green')

ax.tick_params(which='major', length=5, width=2.0, direction='in')
ax.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')
ax.minorticks_on()

# Legend
lns = [p1, p2, p3]
ax.legend(handles=lns, loc='best')



def onpick(event):
    ind = event.ind
    print 'pgc', pgc_common[ind]

fig.canvas.mpl_connect('pick_event', onpick)



plt.show()

    

    
    

   
   
   
   










