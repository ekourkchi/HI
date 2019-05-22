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
from bokeh.plotting import *
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, HoverTool

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
    days_string = []
    numbers = []

    while current_day!=tomorrow:
        
        c0 = datetime.datetime.strptime(current_day, "%Y-%m-%d")
        
        if current_day in myDict:
            days.append(c0)
            days_string.append(c0.strftime('%Y-%m-%d'))
            numbers.append(myDict[current_day])
        else: 
            days.append(c0)
            days_string.append(c0.strftime('%Y-%m-%d'))
            numbers.append(0)
        
        c =  c0 + datetime.timedelta(days=1)
        current_day = c.strftime('%Y-%m-%d')

    numbers = smooth(numbers, window)
    
    return days, numbers, days_string
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

days, numbers, days_string = time_serie(myDict, window=5)

print days

myDict_ = dict()
for i in range(len(pgcID2)):
    add_time(myDict_, checkinTime2[i])

days_, numbers_, days_string_ = time_serie(myDict_, window=5, start="2018-05-01")


date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")

output_file("test.html")



hover = HoverTool(tooltips=[ 
    ("Date", "@days_string"),
    ("# of galaxies", "@numbers"),
    ])

TOOLS = [hover,'pan', 'tap', 'wheel_zoom', 'box_zoom', 'reset', 'save']

p = figure(tools=TOOLS, toolbar_location="right", logo="grey",plot_width=500, plot_height=400, x_axis_type="datetime", title="Last update: "+date)

p.background_fill_color = "beige"
p.grid.grid_line_color="gainsboro"

# plot
source = ColumnDataSource({'days':days, 'numbers':numbers, 'days_string':days_string})
p.line('days', 'numbers', source=source, line_width=2, color="blue", alpha=0.5, legend="Everybody")

source = ColumnDataSource({'days':days_, 'numbers':numbers_, 'days_string':days_string})
p.line('days', 'numbers', source=source, line_width=2, color="red", alpha=0.5, legend="Amateurs")

p.legend.location = "top_left"

p.yaxis.axis_label = "No. of galaxies"
p.yaxis.axis_label_text_color = "black"
p.yaxis.axis_label_text_font_size = "14pt"



p.xaxis.axis_label = "Date"
p.xaxis.axis_label_text_color = "black"
p.xaxis.axis_label_text_font_size = "14pt"



script, div = components(p)
script = '\n'.join(['' + line for line in script.split('\n')])

with open("Output.txt", "w") as text_file:
    text_file.write(div)
    text_file.write(script)

show(p)
#save(p)
  
