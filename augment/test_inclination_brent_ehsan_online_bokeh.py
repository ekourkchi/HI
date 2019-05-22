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
import time
import datetime
from bokeh.plotting import *
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, Range1d, Label, TapTool, OpenURL, CustomJS

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
    inFile = 'EDD.inclination.All.Manoa.06Jun2018151330.txt'
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
    inFile = 'EDD.inclination.All.Guest.06Jun2018151339.txt'
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

######################################
######################################
######################################
######################################

inFile = 'old_Inclinations.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_old    = table['pgc']
inc_old    = table['inc']
flag_old   = table['flag']
user_old   = [' '.join(dummy.split()) for dummy in table['user']]


#name    = 'ehsan'
#myEmail = 'ekourkchi@gmail.com'

#name    = 'amber'
#myEmail = 'mokelkea@hawaii.edu'


name    = 'tully'
myEmail = 'rbtully1@gmail.com'

incDic = getINC()

pgc_common   = []
old_inc       = []
online_inc   = []
No = 0 

for i in range(len(pgc_old)):
    
    if user_old[i]==name and flag_old[i]==0: # and inc_old[i]>67:  # amber 67 ehsan:60
        
        No+=1
        #print pgc_old[i], inc_old[i], 'Python', myEmail
        
        
        if pgc_old[i] in incDic:
        
            inc, stdev, flag, note, n = incMedian(incDic[pgc_old[i]])
            
            if n>=3:
                old_inc.append(inc_old[i])
                pgc_common.append(pgc_old[i])
                online_inc.append(inc)
           
#print No        
        
#fig = py.figure(figsize=(7, 5), dpi=100)
#fig.subplots_adjust(hspace=0.15, top=0.95, bottom=0.15, left=0.15, right=0.95)
#ax = fig.add_subplot(111)    


#p1, = ax.plot([0,100], [0,100], color='black', linestyle='-', label="equality")
#p2, = ax.plot([0,100], [5,105], color='b', linestyle=':', label=r'$\pm5^o$')
#ax.plot([0,100], [-5,95], color='b', linestyle=':')
#p3, = ax.plot([0,100], [10,110], color='r', linestyle='--', label=r'$\pm10^o$')
#ax.plot([0,100], [-10,90], color='r', linestyle='--')
#ax.plot(online_inc, old_inc, 'g.', picker=5, alpha=0.5)


pgc_common = np.asarray(pgc_common)
online_inc = np.asarray(online_inc)
old_inc = np.asarray(old_inc)

N = len(online_inc)
a1 = np.zeros(N)
a2 = np.zeros(N)


a1[np.where(online_inc<80)] = 1
a2[np.where(online_inc>60)] = 1
a = a1 + a2

index = np.where(a==2)
online_inc = online_inc[index]
old_inc = old_inc[index]

delta = online_inc-old_inc
std = np.std(delta)
rms = np.sqrt(np.mean(delta**2))


date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")
    
output_file("test.html")

hover = HoverTool(tooltips=[ 
    ("inc_x", "@inc_x"),
    ("inc_y", "@inc_y"),
    ("PGC", "@PGC"),
    ])

hover.point_policy='snap_to_data'
hover.line_policy='nearest'#'prev'

TOOLS = [hover, 'pan', 'tap', 'wheel_zoom', 'box_zoom', 'reset', 'save']

p = figure(tools=TOOLS, toolbar_location="below", logo="grey",plot_width=500, plot_height=400, title="Last update: "+date)

p.grid.grid_line_color="gainsboro"
    
p.line([0,100], [0,100], line_width=2, color="black", legend="equality")
p.line([0,100], [5,105], line_width=1, color="blue", legend='-/+5 deg', line_dash='dotted')
p.line([0,100], [-5,95], line_width=1, color="blue", line_dash='dotted')
p.line([0,100], [10,110], line_width=1, color="red", legend='-/+10 deg', line_dash='dashed')
p.line([0,100], [-10,90], line_width=1, color="red", line_dash='dashed')

source = ColumnDataSource({'inc_x': online_inc, 'inc_y': old_inc, 'PGC': pgc_common})
render = p.circle('inc_x', 'inc_y', source=source, size=5, color="green", alpha=0.4, hover_color="orange", hover_alpha=0.8, hover_line_color='red',
                  
                  # set visual properties for selected glyphs
                  selection_fill_color="pink",

                  # set visual properties for non-selected glyphs
                  nonselection_fill_alpha=0.3,
                  nonselection_fill_color="green",
                  
                  )

mytext = Label(x=70, y=45, text='RMS: '+"%.1f" % (rms)+' deg')
p.add_layout(mytext)

mytext = Label(x=70, y=40, text='User: ' + name, text_color='green')
p.add_layout(mytext)


p.legend.location = "top_left"
p.x_range = Range1d(35, 95)
p.y_range = Range1d(35, 95)

p.xaxis.axis_label = 'Inclination [deg]'
p.yaxis.axis_label = 'Inclination [deg]'


#url = "http://edd.ifa.hawaii.edu/cf4_photometry/get_sdss_cf4.php?pgc=@PGC"
#taptool = p.select(type=TapTool)
#taptool.callback = OpenURL(url=url)

render.selection_glyph.line_width = 5


code = """
    
    var index_selected = source.selected['1d']['indices'][0];
    var win = window.open("http://edd.ifa.hawaii.edu/cf4_photometry/get_sdss_cf4.php?pgc="+source.data['PGC'][index_selected]+"#t01", "EDDesn", "width=800, height=700");
    try {win.focus();} catch (e){}

"""

taptool = p.select(type=TapTool)
taptool.callback = CustomJS(args=dict(source=source), code=code)





show(p)

   
   
   










