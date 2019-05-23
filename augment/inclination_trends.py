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
from scipy.optimize import curve_fit
from astropy.stats import sigma_clip
import random
######################################
def rnd_inc(inc):
    
            if inc==None: return None
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
    
    n = 0
    if email=='rbtully1@gmail.com': n = 4
    elif email=='ekourkchi@gmail.com': n = 4
    elif email=='s.eftekharzadeh@gmail.com':
        if inc>50: n=1
        else: n=0
    elif email=='mokelkea@hawaii.edu': n = 3
    elif email=='chasemu@hawaii.edu': n = 3
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
    elif email=='arnaud.ohet@gmail.com': n = 2
    elif email=='hawaii@udrea.fr': n = 2
    elif email=='helenecourtois33@gmail.com': n = 2
    elif email=='claude.rene21@gmail.com': n = 1
    elif email=='fredwallet@gmail.com': n = 1
    elif email=='henri140860@wanadoo.fr': n = 2
    elif email=='joannin.lycee@free.fr': n = 2
    elif email=='bevig434@gmail.com': n = 1
    elif email=='echarraix69@gmail.com':
        if inc<85 and inc>50: n=1
        else: n=0
    elif email=='pierrefcevey@gmail.com': n = 1
    elif email=='pierre@macweber.ch': n = 1
    elif email=='arnaudoech@gmail.com': n = 1
    elif email=='lionmarm@gmail.com': n = 1
    elif email=='neilljd@gmail.com': n = 3
    elif email=='mseibert@carnegiescience.edu': n = 3
        
    for i in range(n): incs.append(inc)
    return incs 
######################################
def correction(i, email):
    
    a=1
    b=0

    if email=='mka7@hawaii.edu':
        a = 0.9962765770447537
        b = 1.632224534453941
    if email=='chuangj@hawaii.edu':
        a = 0.9717341859632354
        b = 3.654944012785386
    if email=='mi24@hawaii.edu':
        a = 1.0033220814125834
        b = 0.9880920297011041
    if email=='s.eftekharzadeh@gmail.com':
        a = 0.8743681979165089
        b = 7.831987496520716
    if email=='arnaud.ohet@gmail.com':
        a = 0.9049085332042158
        b = 7.679626830024785
    if email=='cgrubner0@gmail.com':
        a = 0.8983834757119172
        b = 8.315207008784302
    if email=='echarraix69@gmail.com':
        a = 0.9069401106228983
        b = 8.603480747378375
    if email=='pascal.jouve@free.fr':
        a = 1.0410645393211804
        b = -1.9661414004232223
    if email=='a.danesh61@gmail.com':
        a = 1.054190817672426 
        b = -4.115230286293349
    if email=='helenecourtois33@gmail.com':
        a = 1.0041229424908624
        b = 2.2948858998199455



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
        emails = ['rtully@hawaii.edu', 'rbtully1@gmail.com','ekourkchi@gmail.com','mokelkea@hawaii.edu', 'jrl2014@hawaii.edu', 'dschoen@hawaii.edu', 'adholtha@hawaii.edu'] 
    else: 
        emails = include_Email
    
    
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
    
    
    PGC = []
    for i in range(len(pgc_incout)):
        if not pgc_incout[i] in PGC:
            PGC.append(pgc_incout[i])
    for i in range(len(pgc_incout_)):
        if not pgc_incout_[i] in PGC:
            PGC.append(pgc_incout_[i])        
            
            
    incDict = {}
    for i in range(len(PGC)):   
        
        data = []
        
        indx = np.where(PGC[i] == pgc_incout)
        for j in indx[0]:
            if email[j] in emails and not email[j] in exclude_Email:
                inc_incout[j] = correction(inc_incout[j], email[j])
                data.append([email[j], inc_incout[j],flag_incout[j],note[j], [NS[j], BI[j], TF[j], AM[j], DI[j], HI[j], FO[j], NP[j], MU[j]]])

        indx = np.where(PGC[i] == pgc_incout_)
        for j in indx[0]:
            if email_[j] in emails and not email_[j] in exclude_Email:
                inc_incout_[j] = correction(inc_incout_[j], email[j])
                data.append([email[j], inc_incout_[j],flag_incout_[j],note_[j], [NS_[j], BI_[j], TF_[j], AM_[j], DI_[j], HI_[j], FO_[j], NP_[j], MU_[j]]])

        incDict[PGC[i]] = data
        
        
    return incDict   
###########################################################          
######################################
def incMedian(incDic):
    
    boss = 'ekourkchi@gmail.com'
    
    Keypeople = []
    for item in incDic:
        Keypeople.append(item[0])
        if item[0] == 'rbtully1@gmail.com':
            boss = 'rbtully1@gmail.com'
        if item[0] == 'rtully@hawaii.edu':
            boss = 'rtully@hawaii.edu'            
            

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
            stdev = np.std(incs)

            incs2 = np.asarray(incs2)
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
        stdev = np.std(incs)

        incs2 = np.asarray(incs2)
        filtered_data = sigma_clip(incs2, sigma=2, iters=5, copy=False)
        incs2 = filtered_data.data[np.logical_not(filtered_data.mask)]
        inc = np.median(incs2)
            
    note = addConcern(note, concerns)
    #inc = rnd_inc(inc)
    
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
inFile = 'Wise_calib_visier.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_wise_vizier    = table['PGC']
inc_wise_vizier    = table['i']
b_a_wise_vizier    = table['b_a']
######################################

inFile = 'EDD.inclination.All.Manoa.22May2019172954.txt'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_incout    = table['pgcID']
inc_incout    = table['inc']
flag_incout   = table['flag']
email         = [' '.join(dummy.split()) for dummy in table['email']]


inFile = 'EDD.inclination.All.Guest.22May2019173010.txt'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_incout_    = table['pgcID']
inc_incout_    = table['inc']
flag_incout_   = table['flag']
email_         = [' '.join(dummy.split()) for dummy in table['email']]
inputTable_    = [' '.join(dummy.split()) for dummy in table['inputTable']]

name    = 'Brent'
myEmail = 'rbtully1@gmail.com'

#name    = 'Ehsan'
#myEmail = 'ekourkchi@gmail.com'

#name    = 'Sarah'
#myEmail = 's.eftekharzadeh@gmail.com'

#name    = 'Amber'
#myEmail = 'mokelkea@hawaii.edu'

#name    = 'Chase'
#myEmail = 'chasemu@hawaii.edu'

#name    = 'Devin'
#myEmail = 'dschoen@hawaii.edu'

#name    = 'Alexandria'
#myEmail = 'adholtha@hawaii.edu'

#name    = 'Jordan'
#myEmail = 'jrl2014@hawaii.edu'

#name    = 'Juana'
#myEmail = 'chuangj@hawaii.edu'

#name    = 'Michael I.'
#myEmail = 'mi24@hawaii.edu'

#name    = 'Michael A.'
#myEmail = 'mka7@hawaii.edu'

#name    = 'Arash'
#myEmail = 'a.danesh61@gmail.com'

#name    = 'Charles G.'
#myEmail = 'cgrubner0@gmail.com'

#name    = 'Pascal J.'
#myEmail = 'pascal.jouve@free.fr'

#myEmail = 'dlsaintsorny@gmail.com'
#name    = 'Daniel S.'

#myEmail = 'arnaud.ohet@gmail.com'
#name    = 'Arnaud'

#name    = 'Denis'
#myEmail = 'hawaii@udrea.fr'

#name     = 'Henri'
#myEmail = 'henri140860@wanadoo.fr'

#myEmail     = 'fredwallet@gmail.com'
#name = 'Fred'

#myEmail     = 'claude.rene21@gmail.com'
#name = 'Claude-Rene'

#myEmail     = 'helenecourtois33@gmail.com'
#name = 'Helene'

#myEmail     = 'joannin.lycee@free.fr'
#name = 'Regis'

#myEmail    = 'bevig434@gmail.com'
#name = 'Benjamin'

#myEmail     = 'echarraix69@gmail.com'
#name = 'Emmanuel'

A_emails = ['rtully@hawaii.edu', 'rbtully1@gmail.com', 'mokelkea@hawaii.edu', 'jrl2014@hawaii.edu', 'dschoen@hawaii.edu', 'mi24@hawaii.edu', 'chuangj@hawaii.edu']

B_emails = ['ekourkchi@gmail.com', 's.eftekharzadeh@gmail.com', 'chasemu@hawaii.edu', 'adholtha@hawaii.edu', 'mka7@hawaii.edu', 'a.danesh61@gmail.com', 'helenecourtois33@gmail.com']

C_emails = ['cgrubner0@gmail.com', 'pascal.jouve@free.fr', 'dlsaintsorny@gmail.com', 'arnaud.ohet@gmail.com', 'hawaii@udrea.fr', 'henri140860@wanadoo.fr']

D_emails = ['henri140860@wanadoo.fr', 'claude.rene21@gmail.com', 'fredwallet@gmail.com', 'joannin.lycee@free.fr', 'bevig434@gmail.com', 'echarraix69@gmail.com']

E_emails = ['pierrefcevey@gmail.com','pierre@macweber.ch', 'arnaudoech@gmail.com', 'lionmarm@gmail.com', 'neilljd@gmail.com', 'mseibert@carnegiescience.edu']

##############################################################################

#incDic = getINC(include_Email=A_emails+B_emails+E_emails, exclude_Email=myEmail)
incDic = getINC(include_Email=A_emails+B_emails+C_emails+D_emails+E_emails, exclude_Email=myEmail)

pgc_common   = []
old_inc       = []
online_inc   = []
No = 0 

for i in range(len(pgc_incout)):
    if email[i]==myEmail and flag_incout[i]==0 and inc_incout[i]>50 and inc_incout[i]<90:
        No+=1
        if pgc_incout[i] in incDic:
            inc, stdev, flag, note, n = incMedian(incDic[pgc_incout[i]])
            if n>=2:
                corrected_inc = correction(inc_incout[i], myEmail)
                if (np.abs(corrected_inc-inc)<10):
                    old_inc.append(corrected_inc)
                    pgc_common.append(pgc_incout[i])
                    online_inc.append(inc)

i_lst = []
for i in range(len(pgc_incout_)):
    if email_[i]==myEmail:
        i_lst.append(i)


if myEmail in C_emails: 
    ignore=100
elif myEmail in D_emails: 
    ignore=20
else: 
    ignore=0
         
for i in i_lst[:len(i_lst)-ignore]:
  if inputTable_[i]!='example_bad_galaxie' and inputTable_[i]!='example_good_galaxie':
    if flag_incout_[i]==0:
        No+=1
        if pgc_incout_[i] in incDic:
            inc, stdev, flag, note, n = incMedian(incDic[pgc_incout_[i]])
            if n>=2:
                old_inc.append(correction(inc_incout_[i], myEmail))
                pgc_common.append(pgc_incout_[i])
                online_inc.append(inc)   
##############################################################################
################################################
         
#### 2 plots - horizontal
fig = py.figure(figsize=(12, 5), dpi=100)    
fig.subplots_adjust(wspace=0.15, top=0.95, bottom=0.1, left=0.05, right=0.98)



ax = fig.add_subplot(121)
ax_ = fig.add_subplot(122)

ax.plot(online_inc, old_inc, 'g.', picker=5, alpha=0.5)   #### 
p1, = ax.plot([0,100], [0,100], color='black', linestyle='-', label="equality")
p2, = ax.plot([0,100], [5,105], color='b', linestyle=':', label=r'$\pm5^o$')
ax.plot([0,100], [-5,95], color='b', linestyle=':')
p3, = ax.plot([0,100], [10,110], color='r', linestyle='--', label=r'$\pm10^o$')
ax.plot([0,100], [-10,90], color='r', linestyle='--')


pgc_common = np.asarray(pgc_common)
online_inc = np.asarray(online_inc)
old_inc = np.asarray(old_inc)

N = len(online_inc)
a1 = np.zeros(N)
a2 = np.zeros(N)




ax.set_xlim([35,100])
ax.set_ylim([35,100])
ax.set_ylabel(r'$i$'+' ('+name+') [deg]', fontsize=14)
ax.set_xlabel(r'$i_{av}$'+' [deg]', fontsize=14)



ax.tick_params(which='major', length=5, width=2.0, direction='in')
ax.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')
ax.minorticks_on()

# Legend
lns = [p1, p2, p3]
ax.legend(handles=lns, loc=2)


y = []
x = []
for i in range(len(online_inc)):
    if old_inc[i]<=80 and abs(online_inc[i]-old_inc[i])<10.:
        x.append(online_inc[i])
        y.append(old_inc[i])

x=np.asarray(x)
y=np.asarray(y)

fit  = np.polyfit(y,x, 1, cov=True)
a=1.* fit[0][0]
b=1.* fit[0][1]
cov = fit[1]
print '(a, b, cov) = ', a,b,cov



ax.plot([0,100], [-b/a,100./a-b/a], color='brown', linestyle='--')


#fit  = np.polyfit(x,y, 1, cov=True)
#a=1.* fit[0][0]
#b=1.* fit[0][1]
#cov = fit[1]
#print '(a, b, cov) = ', a,b,cov


#ax.plot([0,100], [b,100.*a+b], color='black', linestyle='--')
#ax_.plot(online_inc, old_inc/a-b/a, 'b.', picker=5, alpha=0.5)
ax_.plot(online_inc, old_inc*a+b, 'b.', picker=5, alpha=0.5)



a1[np.where(online_inc<80)] = 1
a2[np.where(online_inc>50)] = 1
a0 = a1 + a2

index = np.where(a0==2)
xx = online_inc[index]
yy = old_inc[index]

delta = xx-yy
delta = delta[np.where(delta<8)]
std = np.std(delta)
rms = np.sqrt(np.mean(delta**2))

ax.text(38,84, r'$\sigma: $'+"%.1f" % (std)+r'$^o$')
ax.text(38,80, r'$RMS: $'+"%.1f" % (rms)+r'$^o$')
#ax.text(85,60, r'$a: $'+"%.4f" % (a), color='brown')
#ax.text(85,56, r'$b: $'+"%.4f" % (b), color='brown')
#ax.text(85,52, r'$\sigma_{a}: $'+"%.4f" % np.sqrt(cov[0][0]), color='brown')
#ax.text(85,48, r'$\sigma_{b}: $'+"%.4f" % np.sqrt(cov[1][1]), color='brown')
#ax.text(85,44, r'$C_{ab}: $'+"%.4f" % (cov[0][1]), color='brown')
#######################################################
#old_inc = a*old_inc+b   #### correction
old_inc = old_inc/a-b/a   #### correction

yy = old_inc[index]

delta = xx-yy
delta = delta[np.where(delta<8)]
std = np.std(delta)
rms = np.sqrt(np.mean(delta**2))

ax_.text(38,84, r'$\sigma: $'+"%.1f" % (std)+r'$^o$')
ax_.text(38,80, r'$RMS: $'+"%.1f" % (rms)+r'$^o$')

p1, = ax_.plot([0,100], [0,100], color='black', linestyle='-', label="equality")
p2, = ax_.plot([0,100], [5,105], color='g', linestyle=':', label=r'$\pm5^o$')
ax_.plot([0,100], [-5,95], color='g', linestyle=':')
p3, = ax_.plot([0,100], [10,110], color='r', linestyle='--', label=r'$\pm10^o$')
ax_.plot([0,100], [-10,90], color='r', linestyle='--')
# Legend
lns = [p1, p2, p3]
ax_.legend(handles=lns, loc=2)
ax_.set_xlim([35,100])
ax_.set_ylim([35,100])
ax_.set_ylabel(r"$i'$"+' ('+name+') [deg] - Corrected', fontsize=14)
ax_.set_xlabel(r'$i_{av}$'+' [deg]', fontsize=14)
ax_.tick_params(which='major', length=5, width=2.0, direction='in')
ax_.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')
ax_.minorticks_on()

#ax_.text(70,40, r"$i'=a * i + b $", fontsize=14)

#######################################################




#fitParams, fitCovariances = curve_fit(fitFunc, x, y)
#print fitParams
#print fitCovariances
#t = np.linspace(40,100,500)
#plt.plot(t, fitFunc(t, fitParams[0], fitParams[1]), color='red', linestyle='--')




def onpick(event):
    ind = event.ind
    print 'pgc', pgc_common[ind]

fig.canvas.mpl_connect('pick_event', onpick)



plt.show()

    

    
    

   
   
   
   










