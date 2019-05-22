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
import datetime
import mpld3


#######################################
def add_time(myDict, dtime):
    
    date = dtime.split(" ")[0]
    if date in myDict:
        myDict[date]+=1
    else:
        myDict[date] = 1
#######################################
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
#######################################
def time_serie(myDict, window=3, start=None):
    
    day_lst = []
    for key in myDict:
        a = ''
        for st in key.split('-'): a+=st
        day_lst.append(int(a))


    day_lst = np.sort(day_lst)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    
    if start is None:
        begin_day = datetime.datetime.strptime(str(day_lst[0]), "%Y%m%d")
    else: 
        begin_day = datetime.datetime.strptime(start, "%Y-%m-%d")

    current_day = begin_day.strftime('%Y-%m-%d')

    days = []
    numbers = []

    while current_day!=tomorrow:
        
        c0 = datetime.datetime.strptime(current_day, "%Y-%m-%d")
        
        if current_day in myDict:
            days.append(c0)
            numbers.append(myDict[current_day])
        else: 
            days.append(c0)
            numbers.append(0)
        
        c =  c0 + datetime.timedelta(days=1)
        current_day = c.strftime('%Y-%m-%d')

    numbers = smooth(numbers, window)
    
    return days, numbers
#######################################
    


inFile  = 'EDD.inclination.All.Manoa.10Jun2018004236.txt'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgcID1 = table['pgcID']
checkinTime1 = [' '.join(dummy.split()) for dummy in table['checkinTime']]

inFile  = 'EDD.inclination.All.Guest.10Jun2018004249.txt'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgcID2 = table['pgcID']
inputTable2 = [' '.join(dummy.split()) for dummy in table['inputTable']]
email2 = [' '.join(dummy.split()) for dummy in table['email']]
checkinTime2 = [' '.join(dummy.split()) for dummy in table['checkinTime']]


myDict = dict()
for i in range(len(pgcID1)):
    add_time(myDict, checkinTime1[i])
for i in range(len(pgcID2)):
    add_time(myDict, checkinTime2[i])

days, numbers = time_serie(myDict, window=5)


myDict_ = dict()
for i in range(len(pgcID2)):
    add_time(myDict_, checkinTime2[i])

days_, numbers_ = time_serie(myDict_, window=5, start="2018-05-01")

fig, ax = plt.subplots()

# plot
p1, = ax.plot(days, numbers, label="Everybody")
p2, = ax.plot(days_, numbers_, label="Amateurs")

plt.gcf().autofmt_xdate()

ax.set_ylabel("No. of galaxies", fontsize=12)
ax.set_xlabel("Date", fontsize=12)

date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")
ax.set_title("Last update: "+date)

# Legend
lns = [p1, p2]
ax.legend(handles=lns, loc='best')

#mpld3.show(fig)



ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='--', linewidth=1)
ax.xaxis.grid(color='gray', linestyle='--', linewidth=1)

plt.show()
        
