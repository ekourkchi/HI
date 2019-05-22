#!/usr/bin/python
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table, Column 
import pylab as py
import time
from scipy import stats
import datetime



#######################################
def nHour(inTime, DT, date_):
    
    seconds = 0

    for i in range(len(inTime)):
        inTime_ = inTime[i]
        myDate = inTime_.strftime('%Y-%m-%d').split(' ')
        myDate = myDate[0]
        if myDate==date_:
            if DT[i]<1000:
                seconds+=DT[i]
    
    return seconds/3600.
#######################################


inFile  = 'EDD.inclination.All.Manoa.11Jan2019135152.txt'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgcID1 = table['pgcID']
email1 = [' '.join(dummy.split()) for dummy in table['email']]
checkinTime1 = [' '.join(dummy.split()) for dummy in table['checkinTime']]
checkoutTime1 = [' '.join(dummy.split()) for dummy in table['checkoutTime']]


inFile  = 'EDD.inclination.All.Guest.11Jan2019135131.txt'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgcID2 = table['pgcID']
email2 = [' '.join(dummy.split()) for dummy in table['email']]
checkinTime2 = [' '.join(dummy.split()) for dummy in table['checkinTime']]
checkoutTime2 = [' '.join(dummy.split()) for dummy in table['checkoutTime']]

#myEmail= 'ekourkchi@gmail.com'
#myEmail= 'mokelkea@hawaii.edu'
myEmail= 'arnaud.ohet@gmail.com'
#myEmail= 's.eftekharzadeh@gmail.com'
#myEmail= 'a.danesh61@gmail.com'
#myEmail= 'henri140860@wanadoo.fr'
#myEmail= 'dschoen@hawaii.edu'
#myEmail = 'chasemu@hawaii.edu'
#myEmail = 'chuangj@hawaii.edu'
#myEmail = 'Total'

DT = []
dt_ = []
inTime = []
N = 0

for i in range(len(pgcID1)):
    time0 = datetime.datetime.strptime("2018-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    if myEmail=='Total' or email1[i]==myEmail:
        time2 = datetime.datetime.strptime(checkinTime1[i], "%Y-%m-%d %H:%M:%S")
        time1 = datetime.datetime.strptime(checkoutTime1[i], "%Y-%m-%d %H:%M:%S")
        elapsedTime = time2 - time1
        elapsedTime_ = time2 - time0
        inTime.append(time2)
        DT.append(elapsedTime.total_seconds())
        dt_.append(elapsedTime_.total_seconds())
        N+=1
for i in range(len(pgcID2)):
    time0 = datetime.datetime.strptime("2018-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    if myEmail=='Total' or email2[i]==myEmail:
        time2 = datetime.datetime.strptime(checkinTime2[i], "%Y-%m-%d %H:%M:%S")
        time1 = datetime.datetime.strptime(checkoutTime2[i], "%Y-%m-%d %H:%M:%S")
        inTime.append(time2)
        elapsedTime = time2 - time1
        elapsedTime_ = time2 - time0
        DT.append(elapsedTime.total_seconds())
        dt_.append(elapsedTime_.total_seconds())    
        N+=1
        


dt = np.asarray(DT)
dt_ = np.asarray(dt_)

indx = np.argsort(dt_)
dt = dt[indx]

dt = stats.sigmaclip(dt)
dt = dt[0]
med = np.median(dt)
std = np.std(dt)

#fig, ax = plt.subplots()

#ax.plot(dt, '.', alpha=0.2)
#ax.plot([0, len(dt)],[med,med], '-', color='black')
#ax.plot([0, len(dt)],[med+std,med+std], '--', color='green')
#ax.plot([0, len(dt)],[med-std,med-std], '--', color='green')

#ax.annotate(r"$T_{av} = $"+"%d" % (med)+r'$\pm$'+"%d" % (std)+' seconds/galaxy',(0, 400), fontsize=12)
#ax.annotate(myEmail,(0, 600), fontsize=12, color='maroon')


#ax.set_ylabel("Time (s)", fontsize=12)
#ax.set_xlabel("Galaxy Entry Number", fontsize=12)

#ax.set_ylim([2,1000])
#ax.set_yscale("log")


#date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")
#ax.set_title("Last update: "+date)


#plt.show()



tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
tomorrow = tomorrow.strftime('%Y-%m-%d')


start= '2018-01-01'
begin_day = datetime.datetime.strptime(start, "%Y-%m-%d")
current_day = begin_day.strftime('%Y-%m-%d')
hour = 0
while current_day!='2018-03-02':
    c0 = datetime.datetime.strptime(current_day, "%Y-%m-%d")
    myDate = current_day.split(' ')
    myDate = myDate[0]
    
    hour+= nHour(inTime, DT, myDate)    
    
    c =  c0 + datetime.timedelta(days=1)
    current_day = c.strftime('%Y-%m-%d')    

start= '2018-03-03'
begin_day = datetime.datetime.strptime(start, "%Y-%m-%d")
current_day = begin_day.strftime('%Y-%m-%d')

p = 7
hour = 0
myDates = []
hours = []

while current_day!=tomorrow:
    
    c0 = datetime.datetime.strptime(current_day, "%Y-%m-%d")
    myDate = current_day.split(' ')
    myDate = myDate[0]
    
    hour+= nHour(inTime, DT, myDate)
    
    if p%7==0: 
        myDates.append(c0)
        hours.append(hour)
        hour = 0
    
    c =  c0 + datetime.timedelta(days=1)
    p+=1
    current_day = c.strftime('%Y-%m-%d')
    
    

fig = plt.figure(figsize=(12.5, 4.0), dpi=100)
ax = fig.add_axes([0.05, 0.2, 0.92,  0.73])
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='--', linewidth=1)

xticklabels = []
for j in range(len(hours)):
    ax.bar([j], [hours[j]], 0.5, color='dodgerblue')
    myDate = myDates[j].strftime('%Y-%m-%d').split(' ')
    myDate = myDate[0]
    xticklabels.append(myDate)
    #xticklabels.append(str(j))

ax.tick_params(bottom='off')
ax.set_xticks(range(0,j+1))
ax.set_xticklabels(xticklabels, fontsize=8) 
ax.set_xlim([-0.5,j+0.5])

for tick in ax.get_xticklabels():
    tick.set_rotation(90)

total = 0
for h in hours: total+=h
ax.annotate("Total: "+"%d" % (math.ceil(total))+' hours',(0.2, 0.90), fontsize=14, xycoords='axes fraction', color='maroon')
ax.annotate("# of Galxies: "+"%d" % (N),(0.4, 0.90), fontsize=14, xycoords='axes fraction', color='green')




ax.set_ylabel("Hours", fontsize=12)
ax.set_xlabel("Date [yyyy-mm-dd]", fontsize=12)
ax.set_title("Weekly Work Hours ... Last update: "+myDate+'  <'+myEmail+'>', fontsize=12)

plt.show()










