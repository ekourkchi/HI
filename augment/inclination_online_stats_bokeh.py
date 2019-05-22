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
from bokeh.plotting import *
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, Range1d, Label, TapTool, OpenURL, CustomJS


inFile  = 'EDD_distance_cf4_v23.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgc = table['pgc']
inc     = table['inc']
inc_e   = table['inc_e']
inc_flg = table['inc_flg']
inc_n   = table['inc_n']

inFile  = 'EDD.inclination.All.Manoa.26Nov2018151327.txt'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgcID1 = table['pgcID']
checkinTime1 = [' '.join(dummy.split()) for dummy in table['checkinTime']]

inFile  = 'EDD.inclination.All.Guest.26Nov2018151255.txt'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgcID2 = table['pgcID']
inputTable2 = [' '.join(dummy.split()) for dummy in table['inputTable']]
email2 = [' '.join(dummy.split()) for dummy in table['email']]


pgcID = np.concatenate((pgcID1, pgcID2))

Na = len(pgc)
N3 = 0
N2 = 0
N1 = 0
N4 = 0 
N5 = 0

N0 = 0
for i in range(len(pgc)):
    
    if inc_flg[i]>0: N0+=1
    

for i in range(Na):
    
    if pgc[i] in pgcID:
        ind = np.where(pgcID==pgc[i])
        N =  len(ind[0])
        
        if N>=5: N5+=1
        if N>=4: N4+=1
        if N>=3: N3+=1
        if N>=2: N2+=1
        if N>=1: N1+=1

        
print Na, N1, N2, N3, N4, N5, len(pgcID)

date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")

        
hover = HoverTool(tooltips=[ 
    ("# of galaxies", "@numbers"),
    ])  
        
        
output_file("test.html")
TOOLS = [hover, 'save']


fruits = ['Total', 'N1', 'N2', 'N3', 'N4', 'N5']

p = figure(x_range=fruits, tools=TOOLS, toolbar_location="below",plot_width=450, plot_height=350, title="Last update: "+date)

source = ColumnDataSource(data=dict(top=[Na], bottom=[Na-N0], left=[0.5], right=[6.5], numbers=[N0]))
p.quad(top='top', bottom='bottom', left='left', right='right', color="black", alpha=0.2, source=source)

f = ['Total']
source = ColumnDataSource(data=dict(f=f, numbers=[Na]))
p.vbar(x='f', top='numbers', width=0.5, color='blue', alpha=0.95, source=source)

f = ['N1']
source = ColumnDataSource(data=dict(f=f, numbers=[N1]))
p.vbar(x='f', top='numbers', width=0.5, color='red', alpha=0.95, source=source)

f = ['N2']
source = ColumnDataSource(data=dict(f=f, numbers=[N2]))
p.vbar(x='f', top='numbers', width=0.5, color='orange', alpha=0.95, source=source)

f = ['N3']
source = ColumnDataSource(data=dict(f=f, numbers=[N3]))
p.vbar(x='f', top='numbers', width=0.5, color='green', alpha=0.95, source=source)


f = ['N4']
source = ColumnDataSource(data=dict(f=f, numbers=[N4]))
p.vbar(x='f', top='numbers', width=0.5, color='dodgerblue', alpha=0.95, source=source)


f = ['N5']
source = ColumnDataSource(data=dict(f=f, numbers=[N5]))
p.vbar(x='f', top='numbers', width=0.5, color='darkorchid', alpha=0.95, source=source)

p.xgrid.grid_line_color = "grey"
p.ygrid.grid_line_color = "grey"

p.y_range.start = 0
p.yaxis.axis_label = 'No. of galaxies'
p.yaxis.axis_label_text_font_size = "14pt"

p.xaxis.axis_label = 'No. of measurements'
p.xaxis.axis_label_text_font_size = "14pt"
p.xaxis.major_label_text_font = "18pt"


mytext = Label(x=1.27, y=N1-1500, text="%d"% (100.*N1/Na)+"%", text_color='black', text_font_size='10pt')
p.add_layout(mytext)

mytext = Label(x=2.27, y=N2-1500, text="%d"% (100.*N2/Na)+"%", text_color='black', text_font_size='11pt')
p.add_layout(mytext)

mytext = Label(x=3.27, y=N3-1500, text="%d"% (100.*N3/Na)+"%", text_color='black', text_font_size='11pt')
p.add_layout(mytext)

mytext = Label(x=4.27, y=N4-1500, text="%d"% (100.*N4/Na)+"%", text_color='black', text_font_size='11pt')
p.add_layout(mytext)

mytext = Label(x=5.27, y=N5-1500, text="%d"% (100.*N5/Na)+"%", text_color='black', text_font_size='11pt')
p.add_layout(mytext)

mytext = Label(x=3, y=17000, text="Rejected Galaxies", text_color='gray', text_font_size='14pt')
p.add_layout(mytext)


show(p)






        
        
