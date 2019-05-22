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
def addNote(note, text):
    
    if text=='': return note
    
    if note=='':
        note = '<'+text+'>'
    else:
        note = note+' '+'<'+text+'>'
    
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
def myMedian(incDic):
    
    boss = 'rbtully1@gmail.com'
    
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
    
    return [inc, stdev, flag, note, n]

#######################################

inFile = '/home/ehsan/PanStarrs/INClinationCode/EDD.inclination.All.Manoa.03Apr2018160432.txt'
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

inFile = '/home/ehsan/PanStarrs/INClinationCode/EDD.inclination.All.Guest.03Apr2018161254.txt'
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

eMails = ['rbtully1@gmail.com','ekourkchi@gmail.com','s.eftekharzadeh@gmail.com']

PGC = []
for i in range(len(pgc_incout)):
    if not pgc_incout[i] in PGC:
        PGC.append(pgc_incout[i])
for i in range(len(pgc_incout_)):
    if not pgc_incout_[i] in PGC:
        PGC.append(pgc_incout_[i])        
        
        
myDict = {}
for i in range(len(PGC)):   
    
    data = {}
    
    indx = np.where(PGC[i] == pgc_incout)
    for j in indx[0]:
        if not email[j] in data.keys() and email[j] in eMails:
            data[email[j]] = [inc_incout[j],flag_incout[j],note[j], [NS[j], BI[j], TF[j], AM[j], DI[j], HI[j], FO[j], NP[j], MU[j]]]

    indx = np.where(PGC[i] == pgc_incout_)
    for j in indx[0]:
        if not email_[j] in data.keys() and email_[j] in eMails:
            data[email_[j]] = [inc_incout_[j],flag_incout_[j],note_[j], [NS_[j], BI_[j], TF_[j], AM_[j], DI_[j], HI_[j], FO_[j], NP_[j], MU_[j]]]

    myDict[PGC[i]] = data
    
p = 0
for pgc in  myDict:
    
    print pgc, myMedian(myDict[pgc])

        
    p+=1
    if p>100: break


if 705 in myDict:
    
    print myMedian(myDict[705])








