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
from scipy.optimize import curve_fit
from astropy.stats import sigma_clip
import random

def add_dict(myDict, key, flag=False):
    
    if key in myDict: 
        if not flag:
           myDict[key] += 1
        else: myDict[key]=1000
    else:
        if not flag:
           myDict[key] = 1
        else: myDict[key]=1000        
    
    
######################################
def rnd_inc(inc):
    
            if inc==None: return None
            if inc>90: return 90.
            if inc<45: return 0.
            d_inc = inc - int(inc)
            if d_inc>0.5: inc=int(inc)+1
            elif d_inc<0.5: inc=int(inc)
            else:
                rand = random.randint(0,1)
                if rand==0: inc=int(inc)
                else: inc=int(inc)+1
            return inc
######################################
def inc_append(incs, email, inc):
    
    n = 1
    if email=='rbtully1@gmail.com': n = 4
    elif email=='ekourkchi@gmail.com': n = 4
    elif email=='s.eftekharzadeh@gmail.com': 
        if inc>55: n=1
        else: n=0
    elif email=='mokelkea@hawaii.edu': n = 3
    elif email=='chasemu@hawaii.edu': n = 2
    elif email=='jrl2014@hawaii.edu': n = 2
    elif email=='dschoen@hawaii.edu': n = 3
    elif email=='adholtha@hawaii.edu': n = 4
    elif email=='chuangj@hawaii.edu': n = 2
    elif email=='mi24@hawaii.edu': n = 3
    elif email=='mka7@hawaii.edu': n = 2
    elif email=='a.danesh61@gmail.com': n = 2
    
    elif email=='cgrubner0@gmail.com': n = 1
    elif email=='pascal.jouve@free.fr': n = 2
    elif email=='dlsaintsorny@gmail.com': n = 2
    elif email=='arnaud.ohet@gmail.com': n = 1
    elif email=='hawaii@udrea.fr': n = 2
    elif email=='helenecourtois33@gmail.com': n = 3
    elif email=='claude.rene21@gmail.com': n = 1
    elif email=='fredwallet@gmail.com': n = 2
    elif email=='henri140860@wanadoo.fr': n = 2
    elif email=='joannin.lycee@free.fr': n = 2
    elif email=='bevig434@gmail.com': n = 1
    elif email=='echarraix69@gmail.com': 
        if inc<85 and inc>60: n=1
        else: n=0
    
    for i in range(n): incs.append(inc)
    return incs
######################################
def correction(i, email):
    
    a=1
    b=0

    if email=='mka7@hawaii.edu':
        a = 0.9796100828231535
        b = 2.6459216900236147
    if email=='chasemu@hawaii.edu':
        a = 0.9407173034726307
        b = 4.25752408050204
    if email=='chuangj@hawaii.edu':
        a = 0.9698391552105461
        b = 3.582543838111245
    if email=='mi24@hawaii.edu':
        a = 0.9819724300214063
        b = 2.485648837307963
    if email=='arnaud.ohet@gmail.com':
        a = 0.8925968302721691
        b = 8.021973390519326
    if email=='cgrubner0@gmail.com':
        a = 0.8957026107782403
        b = 9.076420810780814
    if email=='echarraix69@gmail.com':
        a = 0.9404807823601113
        b = 6.1016971604571895      
    if email=='pascal.jouve@free.fr':
        a = 1.0385774511616022 
        b = -1.566426430732299
    if email=='helenecourtois33@gmail.com':
        a = 0.9961038898095195
        b = 2.7659703481957454


    return a*i+b
######################################

def fitFunc(x, a, b):
    return a*x+b
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
def getINC(include_Email=None, exclude_Email=[]):
    
    if include_Email==None:
        emails = ['rbtully1@gmail.com','ekourkchi@gmail.com','mokelkea@hawaii.edu', 'jrl2014@hawaii.edu', 'dschoen@hawaii.edu', 'adholtha@hawaii.edu'] 
    else: 
        emails = include_Email
    
    
    #### Manoa
    inFile = 'EDD.inclination.All.Guest.12Feb2019143526.txt'
    table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None, encoding=None)
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
    #print len(pgc_incout)
    
    #### Guest
    inFile = 'EDD.inclination.All.Manoa.12Feb2019141428.txt'
    table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None, encoding=None)
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
    #print len(pgc_incout_)
    
    PGC = []
    for i in range(len(pgc_incout)):
        if not pgc_incout[i] in PGC:
            PGC.append(pgc_incout[i])
    for i in range(len(pgc_incout_)):
        if not pgc_incout_[i] in PGC:
            PGC.append(pgc_incout_[i])        
    
    #print len(PGC)
            
    incDict = {}
    for i in range(len(PGC)):   
        
        data = []
        
        if PGC[i] in pgc_incout:
            indx = np.where(PGC[i] == pgc_incout)
            for j in indx[0]:
                if email[j] in emails and not email[j] in exclude_Email:
                    inc_incout[j] = correction(inc_incout[j], email[j])
                    data.append([email[j], inc_incout[j],flag_incout[j],note[j], [NS[j], BI[j], TF[j], AM[j], DI[j], HI[j], FO[j], NP[j], MU[j]]])
        
        if PGC[i] in pgc_incout_:
            indx = np.where(PGC[i] == pgc_incout_)
            for j in indx[0]:
                if email_[j] in emails and not email_[j] in exclude_Email:
                    inc_incout_[j] = correction(inc_incout_[j], email_[j])
                    data.append([email_[j], inc_incout_[j],flag_incout_[j],note_[j], [NS_[j], BI_[j], TF_[j], AM_[j], DI_[j], HI_[j], FO_[j], NP_[j], MU_[j]]])

        incDict[PGC[i]] = data
        
        
    return incDict   
###########################################################      
def incEmails(incDic):

    email_lst = []
    for item in incDic:
         email_lst.append(item[0])
    
    return email_lst
######################################
def incMedian(incDic):
    
    boss = 'ekourkchi@gmail.com'
    
    Keypeople = []
    for item in incDic:
        Keypeople.append(item[0])
        if item[0] == 'rbtully1@gmail.com':
            boss = 'rbtully1@gmail.com'
            

    flag = 0
    inc  = 0
    note = ''
    stdev = 0
    n = 0   # number of good measurments
    concerns = np.zeros(9)
    
    if boss in Keypeople:
        
        poss_i = 0
        for ppl in Keypeople:
            if ppl==boss: break
            poss_i+=1
        
        if incDic[poss_i][2] != 0:  # boss has flagged it
            
            flag = 1
            for item in incDic:
                if item[2]==1:
                   note =  addNote(note, item[3])
                   concerns+=np.asarray(item[4])
                   n+=1
        
        else:  # boss has NOT flagged it
            
            flag = 0
            incs = []
            incs2 = []
            for item in incDic:
                if item[2]==0:
                    incs.append(item[1])
                    incs2 = inc_append(incs2, item[0], item[1])
                    note = addNote(note, item[3])
                    n+=1
            
            
            incs = np.asarray(incs)
            filtered_data = sigma_clip(incs, sigma=2, iters=5, copy=False)
            incs = filtered_data.data[np.logical_not(filtered_data.mask)]
            #stdev = np.std(incs)

            incs2 = np.asarray(incs2)
            stdev = np.std(incs2) ####
            filtered_data = sigma_clip(incs2, sigma=2, iters=5, copy=False)
            incs2 = filtered_data.data[np.logical_not(filtered_data.mask)]
            inc = np.median(incs2)
            
        
    else:
        flag = []
        for item in incDic:
            flag.append(item[2])
        flag = np.median(flag)
        if flag > 0: flag =1
        
        incs = []
        incs2 = []
        for item in incDic:
            if item[2]==flag:
               incs.append(item[1])
               incs2 = inc_append(incs2, item[0], item[1])
               note = addNote(note, item[3])
               concerns+=np.asarray(item[4])
               n+=1
        
        incs = np.asarray(incs)
        filtered_data = sigma_clip(incs, sigma=2, iters=5, copy=False)
        incs = filtered_data.data[np.logical_not(filtered_data.mask)]
        #stdev = np.std(incs)

        incs2 = np.asarray(incs2)
        stdev = np.std(incs2) ####
        filtered_data = sigma_clip(incs2, sigma=2, iters=5, copy=False)
        incs2 = filtered_data.data[np.logical_not(filtered_data.mask)]
        inc = np.median(incs2)
            
    note = addConcern(note, concerns)
    inc = rnd_inc(inc)
    
    if inc>=89:
        err = 1.
    elif inc>=85:
        err = 2.       
    elif inc>=69:
        err = 3.
    elif inc>=50:
        err = 4.  
    elif inc>=45:    
        err = 6. 
    else:
        err = 0 
        flag = 1
        inc = 0 
        stdev = 0 
        
    stdev = np.max([stdev, err])
    stdev = np.round(stdev)
        
    return inc, stdev, flag, note, n

#######################################    

inFile  = 'EDD_distance_cf4_v24.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None, encoding=None)
pgc     = table['pgc']
#inc     = table['inc']
#inc_e   = table['inc_e']
#inc_flg = table['inc_flg']
#inc_n   = table['inc_n']
##################### PART A ###################################################################


#if True:
    ##### Manoa
    #inFile = 'EDD.inclination.All.Manoa.04Dec2018134905.txt'
    #table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None, encoding=None)
    #pgc_incout    = table['pgcID']
    #inc_incout    = table['inc']
    #flag_incout   = table['flag']
    #note          = [' '.join(dummy.split()) for dummy in table['note']]
    #email         = [' '.join(dummy.split()) for dummy in table['email']]
    #NS = table['not_sure']
    #BI = table['better_image']
    #TF = table['bad_TF']
    #AM = table['ambiguous']
    #DI = table['disturbed']
    #HI = table['HI']
    #FO = table['face_on']
    #NP = table['not_spiral']
    #MU = table['multiple']
    
#if True:
    
    ##### Guest
    #inFile = 'EDD.inclination.All.Guest.04Dec2018134846.txt'
    #table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None, encoding=None)
    #pgc_incout_    = table['pgcID']
    #inc_incout_    = table['inc']
    #flag_incout_   = table['flag']
    #note_          = [' '.join(dummy.split()) for dummy in table['note']]
    #email_         = [' '.join(dummy.split()) for dummy in table['email']]
    #NS_ = table['not_sure']
    #BI_ = table['better_image']
    #TF_ = table['bad_TF']
    #AM_ = table['ambiguous']
    #DI_ = table['disturbed']
    #HI_ = table['HI']
    #FO_ = table['face_on']
    #NP_ = table['not_spiral']
    #MU_ = table['multiple']


#myDict = {}
#for i in range(len(pgc_incout)):
    #reject = False
    #if flag_incout[i] == 1 and email[i]=='ekourkchi@gmail.com':
        #reject = True
    #if flag_incout[i] == 1 and email[i]=='rbtully1@gmail.com':
        #reject = True    
    #add_dict(myDict, pgc_incout[i], flag=reject)
#for i in range(len(pgc_incout_)):
    #reject = False
    #if flag_incout_[i] == 1 and email_[i]=='ekourkchi@gmail.com':
        #reject = True
    #if flag_incout_[i] == 1 and email_[i]=='rbtully1@gmail.com':
        #reject = True        
    #add_dict(myDict, pgc_incout_[i], flag=reject)    

#sum = 0 
#for p in range(30):    
    #N=0
    #for key in pgc:
        #if myDict[key]>=p and myDict[key]<999:
           #N+=1
    #sum+=N
    #print p, N

#print sum
#N=0
#for key in pgc:
    #if myDict[key]<3:
       #N+=1
       #print key
#print N
######################### PART B ################################################################
############################################################ Begin


#############################################################
A_emails = ['rbtully1@gmail.com', 'mokelkea@hawaii.edu', 'jrl2014@hawaii.edu', 'dschoen@hawaii.edu', 'mi24@hawaii.edu', 'chuangj@hawaii.edu']

B_emails = ['ekourkchi@gmail.com', 's.eftekharzadeh@gmail.com', 'chasemu@hawaii.edu', 'adholtha@hawaii.edu', 'mka7@hawaii.edu', 'a.danesh61@gmail.com', 'helenecourtois33@gmail.com']

C_emails = ['cgrubner0@gmail.com', 'pascal.jouve@free.fr', 'dlsaintsorny@gmail.com', 'arnaud.ohet@gmail.com', 'hawaii@udrea.fr', 'henri140860@wanadoo.fr']

D_emails = ['henri140860@wanadoo.fr', 'claude.rene21@gmail.com', 'fredwallet@gmail.com', 'joannin.lycee@free.fr', 'bevig434@gmail.com', 'echarraix69@gmail.com']
#D_emails = ['henri140860@wanadoo.fr', 'claude.rene21@gmail.com', 'fredwallet@gmail.com', 'joannin.lycee@free.fr', 'bevig434@gmail.com']

incDic = getINC(include_Email=A_emails+B_emails+C_emails+D_emails)

rd = 0 

for i in range(len(pgc)):
        
        
        inc, stdev, flag, note, n = incMedian(incDic[pgc[i]])
        
        email_lst = incEmails(incDic[pgc[i]])
        em = 'echarraix69@gmail.com'
        
        Redo = False
        #if n<3 and flag==0 and inc>=60: Redo=True

        if n<4 and flag==0 and not em in email_lst and inc<80 and inc>60: 
            Redo=True
            
            #if inc>=89 and stdev>2: Redo = True
            #elif inc>=85 and stdev>3: Redo = True
            #elif inc>=60 and stdev>4: Redo = True
            #elif inc>=50 and stdev>5: Redo = True    
            #elif inc>=45 and stdev>7: Redo = True
          
          
        if Redo:
                rd+=1
                print pgc[i]

#print rd, len(pgc)
        






