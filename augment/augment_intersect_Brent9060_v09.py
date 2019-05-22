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
import pylab as py
from astropy.table import Table, Column 

import sqlcl

inFile = 'wise_all.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
wise_name = table['ID']
wise_pgc  = table['PGC']


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

#################
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
###############################
def get_scales(photometry, nskip=29):
    
    table = np.genfromtxt(photometry , delimiter=',', filling_values=None, names=True, dtype=None, skip_header=nskip)
    
    try: ebv = float(table['ebv']) 
    except: ebv=-9.99
    try: a_gal = float(table['a_gal']) 
    except: a_gal=-9.99
    try: central_mu = float(table['central_mu']) 
    except: central_mu=-9.99
    try: mu_90 = float(table['mu_90']) 
    except: mu_90=-9.99
    try: mu_50 = float(table['mu_50']) 
    except: mu_50=-9.99
    try: concentration = float(table['concentration']) 
    except: concentration=-9.99
    try: m_255 = float(table['m_255']) 
    except: m_255=-9.99
    try: disc_mu0 = float(table['disc_mu0']) 
    except: disc_mu0=-9.99
    try: scale_length_h = float(table['scale_length_h']) 
    except: scale_length_h=-9.99
    try: R_asy = float(table['R_asy']) 
    except: R_asy=-9.99
    try: R_90 = float(table['R_90']) 
    except: R_90=-9.99
    try: R_80 = float(table['R_80']) 
    except: R_80=-9.99
    try: R_50 = float(table['R_50']) 
    except: R_50=-9.99
    try: R_20 = float(table['R_20']) 
    except: R_20=-9.99
    try: R_255 = float(table['R_255']) 
    except: R_255=-9.99
    try: d_m_ext = float(table['d_m_ext']) 
    except: d_m_ext=-9.99
    
    return ebv, a_gal, central_mu, mu_50, mu_90, m_255, disc_mu0, scale_length_h, R_50, R_90, R_255, concentration, d_m_ext

###############################
### For a given photometry file, this returns the magnitude value
def get_mag(photometry, index=2, header=None):
    
    if header is not None:
        if os.path.exists(photometry):
           with open(photometry) as f:
               for line in f:
                   foundit = False
                   once = True
                   if line.split(" ")[0]== '#':
                       line_split = line.split(" ")
                       not_void = 0 
                       key = None
                       for thing in line_split:
                           if thing != '':
                                not_void+=1
                           if not_void==2 and once: 
                               key=thing
                               once = False
                           if not_void==3 and key==header: 
                               foundit = True
                               break
                       if foundit: return np.float(thing)
    
    if header is not None: return 0    
    
    if os.path.exists(photometry):
      with open(photometry) as f:
	counter = 1
	for line in f:
	  if counter == 14:
	    line_split = line.split(" ")
	    not_void = 0 
	    for thing in line_split:
	      if thing != '': not_void+=1
	      if not_void==index: 
		break
	    return np.float(thing)
	  counter+=1
###############################
###############################

### For a given photometry file, this returns the magnitude value
def get_mag_f(photometry, index=2, header=None):
    
    if header is not None:
        if os.path.exists(photometry):
           with open(photometry) as f:
               for line in f:
                   foundit = False
                   once = True
                   if line.split(" ")[0]== '#':
                       line_split = line.split(" ")
                       not_void = 0 
                       key = None
                       for thing in line_split:
                           if thing != '':
                                not_void+=1
                           if not_void==2 and once: 
                               key=thing
                               once = False
                           if not_void==3 and key==header: 
                               foundit = True
                               break
                       if foundit: return np.float(thing)
    
    if header is not None: return 0
    
    if os.path.exists(photometry):
      with open(photometry) as f:
	counter = 1
	for line in f:
	  if line.split(" ")[0]!= '#' and line.split(" ")[0]!='#\n':
	    line_split = line.split(" ")
	    not_void = 0 
	    for thing in line_split:
	      if thing != '': 
                  not_void+=1
                  set_param = True
	      if not_void==index: 
		break
	    return np.float(thing)
	  counter+=1
	  
	  
def get_mag_wise(photometry, index=2):
    
    mag = get_mag_f(photometry, index=index)
    
    if mag!=None:
        return mag
    else:
        return -1000
###############################
def get_semimajor(filename):
    
          with open(filename) as f:
            counter = 1
            for line in f:
              if counter == 14:
                line_split = line.split(" ")
                not_void = 0 
                for thing in line_split:
                  if thing != '': not_void+=1
                  if not_void==1: 
                    break
                return np.float(thing)    
              counter+=1             


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
###############################
def isInSDSS_DR12(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcl.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
  
###############################
###############################
def get_ellipse_wise(filename):
          
          ra_cen = -1
          dec_cen = -1
          semimajor = -1
          semiminor = -1
          PA = -1
          with open(filename) as f:
            counter = 1
            for line in f:
              if line.split(" ")[0]!= '#' and line.split(" ")[0]!='#\n': # counter == 17:
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
#################################
def get_quality(filename, nline=40):
    
  line_no = 0
  seprator = ' '
  for line in open(filename, 'r'):
    columns = line.split(seprator)
    line_no+=1
    if len(columns) >= 2 and line_no==nline:
	  key  = columns[0]
	  j = 1
	  while columns[j] == '' or columns[j] == '=': j+=1
	  return int(columns[j])
  return -1

#################################
def read_note(filename):

  qa_note =  filename
  note = ' '
  if os.path.exists(qa_note):
     with open(qa_note) as f:
	counter = 1
	for line in f:
	  if counter == 11:
	    line_split = line.split("=")
	    note =  line_split[1]
	    note = note[0:len(note)-1]
	  counter+=1       
       
  return note

#################################
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

#################
def QA_SDSS_DONE(pgc, ra):
    
    
    databse = '/home/ehsan/db_esn/'+'/cf4_sdss/data/'
    
    name = 'pgc'+str(pgc)
    if os.path.exists(databse+ra_db(ra)+'/sdss/fits/'+name+'_qa.txt'):
        return True
        
    return False   
#################
def QA_WISE_DONE(pgc, ra):
    
    global wise_name, wise_pgc
    
    databse = '/home/ehsan/db_esn/'+'/cf4_wise/data/'
    
    if pgc in wise_pgc:
        i_lst = np.where(pgc == wise_pgc)
        name = wise_name[i_lst][0] 
        if os.path.exists(databse+ra_db(ra)+'/wise/fits/'+name+'_qa.txt'):
            return True
    
    name = 'pgc'+str(pgc)
    if os.path.exists(databse+ra_db(ra)+'/wise/fits/'+name+'_qa.txt'):
        return True
        
    return False    

#######################################
#######################################
def getINC(exclude_Email=[]):
    
    #### Manoa
    inFile = 'EDD.inclination.All.Manoa.03Jul2018141447.txt'
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
    inFile = 'EDD.inclination.All.Guest.03Jul2018141515.txt'
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

########################################################### TEST

#print get_mag_wise('/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/cf4_wise/data/001D/photometry/NGC7821_w1_asymptotic.dat', index=1)

#print get_mag_f('/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/cf4_wise/data/001D/photometry/NGC7821_w1_asymptotic.dat', header='A_Gal:')


#print get_mag('/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/cf4_sdss/data/018D/photometry/pgc1264576_g_asymptotic.dat')

#print get_mag('/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/cf4_sdss/data/018D/photometry/pgc1264576_g_asymptotic.dat', index=1)

#print get_mag('/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/cf4_sdss/data/018D/photometry/pgc1264576_g_asymptotic.dat', header='A_Gal:')

#sys.exit()

########################################################### Begin
inFile  = 'EDD_distance_cf4_v19.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc     = table['pgc']
ra      = table['ra']
dec     = table['dec'] 
gl      = table['gl']
gb      = table['gb']
sgl       = table['sgl']
sgb       = table['sgb']
d25       = table['d25']
b_a       = table['b_a']
pa        = table['pa']
ty        = table['ty']  
type      = table['type']
sdss      = table['sdss'] 
alfa100_  = table['alfa100']
QA_sdss   = table['QA_sdss']  
QA_wise   = table['QA_wise'] 

############################################################
inFile = 'All_LEDA_EDD.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_leda    = table['pgc']
ra_leda     = table['al2000']
ra_leda *= 15.
dec_leda    = table['de2000']
l_leda      = table['l2']
b_leda      = table['b2']
sgl_leda    = table['sgl']
sgb_leda    = table['sgb']
logd25_leda = table['logd25']
logr25_leda = table['logr25']
pa_leda     = table['pa']
ty_leda     = table['t']
type_leda   = table['type']
############################################################



pgc_     = []
ra_      = []
dec_     = []
l_       = []
b_       = []
sgl_     = []
sgb_     = []
sdss_    = []
d25_     = []
alfa100  = []
QA       = []
QA_wise  = []
pa_      = []
b_a_     = []
ty_      = []
type_    = []


for i in  range(len(pgc)): # range(100):
    if not pgc[i] in pgc_:
        pgc_.append(pgc[i])
        ra_.append(ra[i])
        dec_.append(dec[i])
        l_.append(gl[i])
        b_.append(gb[i])
        sgl_.append(sgl[i])
        sgb_.append(sgb[i])
        d25_.append(d25[i])
        sdss_.append(sdss[i]) 
        pa_.append(pa[i]) 
        b_a_.append(b_a[i])
        ty_.append(ty[i])
        alfa100.append(alfa100_[i])

          
        if QA_SDSS_DONE(pgc[i], ra[i]):
            QA.append(1) 
        else: QA.append(0) 
        
        if QA_WISE_DONE(pgc[i], ra[i]):
            QA_wise.append(1) 
        else: QA_wise.append(0)        
        
        type_.append(type[i])
#####################################################

#####################################################

print "Adding Types from the LEDA catalog"


pgc_      = np.asarray(pgc_)
ra_       = np.asarray(ra_)
dec_      = np.asarray(dec_)
l_        = np.asarray(l_)
b_        = np.asarray(b_)
sgl_      = np.asarray(sgl_)
sgb_      = np.asarray(sgb_)
d25_      = np.asarray(d25_)
b_a_      = np.asarray(b_a_)
pa_       = np.asarray(pa_)
ty_       = np.asarray(ty_)
type_     = np.asarray(type_)
sdss_     = np.asarray(sdss_)
alfa100    = np.asarray(alfa100)
QA        = np.asarray(QA)
QA_wise   = np.asarray(QA_wise)


index     = np.argsort(pgc_)
pgc_      = pgc_[index]
ra_       = ra_[index]
dec_      = dec_[index]
l_        = l_[index]
b_        = b_[index]
sgl_      = sgl_[index]
sgb_      = sgb_[index]
d25_      = d25_[index]
b_a_      = b_a_[index]
pa_       = pa_[index]
ty_       = ty_[index]
type_     = type_[index]
sdss_     = sdss_[index]
alfa100    = alfa100[index]
QA        = QA[index]
QA_wise   = QA_wise[index]


for i in range(len(pgc_)):
    
    gal = pgc_[i]
    if gal in [58411,58239,17170,1977897,9476]:
        sdss_[i] = 0 
#####################################################################
print "Taking Care of inclinations ..."
incDic = getINC()


print "Taking Care of flags ..."


location_sdss  = '/home/ehsan/db_esn/cf4_sdss/data/'
location_wise  = '/home/ehsan/db_esn/cf4_wise/data/'

N = len(pgc_)

Squality     = np.zeros(N)
Wquality     = np.zeros(N)
disturbed   = np.zeros((N,), dtype='a1')
trail       = np.zeros((N,), dtype='a1')
not_spiral  = np.zeros((N,), dtype='a1')
face_on     = np.zeros((N,), dtype='a1')
faint       = np.zeros((N,), dtype='a1')
crowded     = np.zeros((N,), dtype='a1')
over_masked = np.zeros((N,), dtype='a1')
fov         = np.zeros((N,), dtype='a1')
multiple    = np.zeros((N,), dtype='a1')
bright_star = np.zeros((N,), dtype='a1')
uncertain   = np.zeros((N,), dtype='a1')
note        = np.zeros((N,), dtype='a100')
source      = np.zeros((N,), dtype='a4')


uu_mag   = np.zeros((N,))
gg_mag   = np.zeros((N,))
rr_mag   = np.zeros((N,))
ii_mag   = np.zeros((N,))
zz_mag   = np.zeros((N,))
Sba      = np.zeros((N,))
Spa      = np.zeros((N,))
u_Rasy   = np.zeros((N,))
g_Rasy   = np.zeros((N,))
r_Rasy   = np.zeros((N,))
i_Rasy   = np.zeros((N,))
z_Rasy   = np.zeros((N,))
A_u      = np.zeros((N,))
A_g      = np.zeros((N,))
A_r      = np.zeros((N,))
A_i      = np.zeros((N,))
A_z      = np.zeros((N,))

ebv      = np.zeros((N,))

mu0_u    = np.zeros((N,))
mu0_g    = np.zeros((N,))
mu0_r    = np.zeros((N,))
mu0_i    = np.zeros((N,))
mu0_z    = np.zeros((N,))

mu50_u   = np.zeros((N,))
mu50_g   = np.zeros((N,))
mu50_r   = np.zeros((N,))
mu50_i   = np.zeros((N,))
mu50_z   = np.zeros((N,))

mu90_u   = np.zeros((N,))
mu90_g   = np.zeros((N,))
mu90_r   = np.zeros((N,))
mu90_i   = np.zeros((N,))
mu90_z   = np.zeros((N,))

m255_u   = np.zeros((N,))
m255_g   = np.zeros((N,))
m255_r   = np.zeros((N,))
m255_i   = np.zeros((N,))
m255_z   = np.zeros((N,))

disc_mu0_u    = np.zeros((N,))
disc_mu0_g    = np.zeros((N,))
disc_mu0_r    = np.zeros((N,))
disc_mu0_i    = np.zeros((N,))
disc_mu0_z    = np.zeros((N,))

SLh_u    = np.zeros((N,))
SLh_g    = np.zeros((N,))
SLh_r    = np.zeros((N,))
SLh_i    = np.zeros((N,))
SLh_z    = np.zeros((N,))

R50_u    = np.zeros((N,))
R50_g    = np.zeros((N,))
R50_r    = np.zeros((N,))
R50_i    = np.zeros((N,))
R50_z    = np.zeros((N,))

R90_u    = np.zeros((N,))
R90_g    = np.zeros((N,))
R90_r    = np.zeros((N,))
R90_i    = np.zeros((N,))
R90_z    = np.zeros((N,))

R255_u   = np.zeros((N,))
R255_g   = np.zeros((N,))
R255_r   = np.zeros((N,))
R255_i   = np.zeros((N,))
R255_z   = np.zeros((N,))

Cntion_u = np.zeros((N,))
Cntion_g = np.zeros((N,))
Cntion_r = np.zeros((N,))
Cntion_i = np.zeros((N,))
Cntion_z = np.zeros((N,))

d_m_ext_u = np.zeros((N,))
d_m_ext_g = np.zeros((N,))
d_m_ext_r = np.zeros((N,))
d_m_ext_i = np.zeros((N,))
d_m_ext_z = np.zeros((N,))

w1_mag   = np.zeros((N,))
w2_mag   = np.zeros((N,))
Wba      = np.zeros((N,))
Wpa      = np.zeros((N,))
w1_Rasy  = np.zeros((N,))
w2_Rasy  = np.zeros((N,))
A_w1     = np.zeros((N,))
A_w2     = np.zeros((N,))


mu0_w1    = np.zeros((N,))
mu50_w1   = np.zeros((N,))
mu90_w1   = np.zeros((N,))
m255_w1   = np.zeros((N,))
disc_mu0_w1    = np.zeros((N,))
SLh_w1    = np.zeros((N,))
R50_w1    = np.zeros((N,))
R90_w1    = np.zeros((N,))
R255_w1   = np.zeros((N,))
Cntion_w1 = np.zeros((N,))

mu0_w2    = np.zeros((N,))
mu50_w2   = np.zeros((N,))
mu90_w2   = np.zeros((N,))
m255_w2   = np.zeros((N,))
disc_mu0_w2    = np.zeros((N,))
SLh_w2    = np.zeros((N,))
R50_w2    = np.zeros((N,))
R90_w2    = np.zeros((N,))
R255_w2   = np.zeros((N,))
Cntion_w2 = np.zeros((N,))

d_m_ext_w1 = np.zeros((N,))
d_m_ext_w2 = np.zeros((N,))

inc      = np.zeros((N,))
inc_e    = np.zeros((N,))
inc_flg  = np.zeros((N,))
inc_note = np.zeros((N,), dtype='a80')
inc_n    = np.zeros((N,))



for i in range(len(pgc_)):
    
    
    ## inclination
    if pgc_[i] in incDic:
        inc[i], inc_e[i], inc_flg[i], inc_note[i], inc_n[i]= incMedian(incDic[pgc_[i]])

    
    radb    = ra_db(ra_[i])
    pgcname = 'pgc'+str(pgc_[i])
    qa_txt_sdss = location_sdss + radb + '/sdss/fits/' + pgcname+'_qa.txt'
    photometry_sdss =  location_sdss + radb +'/photometry/'+pgcname
 
 
##################################################################### Taking care of photometry results
    
    if os.path.exists(qa_txt_sdss):
        
        ebv[i] = -9.99
        Squality[i] = get_quality(qa_txt_sdss)
        if os.path.exists(photometry_sdss+'_u_asymptotic.dat'): 
            uu_mag[i] = get_mag(photometry_sdss+'_u_asymptotic.dat')
            u_Rasy[i] = get_mag(photometry_sdss+'_u_asymptotic.dat', index=1)/60.
            A_u[i]    = get_mag(photometry_sdss+'_u_asymptotic.dat', header='A_Gal:')
        if os.path.exists(photometry_sdss+'_u.scales.dat'):     
            ebv[i], A_u[i], mu0_u[i], mu50_u[i], mu90_u[i], m255_u[i], disc_mu0_u[i], SLh_u[i], R50_u[i], R90_u[i], R255_u[i], Cntion_u[i], d_m_ext_u[i] = get_scales(photometry_sdss+'_u.scales.dat')
            
            
        if os.path.exists(photometry_sdss+'_g_asymptotic.dat'): 
            gg_mag[i] = get_mag(photometry_sdss+'_g_asymptotic.dat')
            g_Rasy[i] = get_mag(photometry_sdss+'_g_asymptotic.dat', index=1)/60.
            A_g[i]    = get_mag(photometry_sdss+'_g_asymptotic.dat', header='A_Gal:')
        if os.path.exists(photometry_sdss+'_g.scales.dat'):     
            ebv[i], A_g[i], mu0_g[i], mu50_g[i], mu90_g[i], m255_g[i], disc_mu0_g[i], SLh_g[i], R50_g[i], R90_g[i], R255_g[i], Cntion_g[i], d_m_ext_g[i] = get_scales(photometry_sdss+'_g.scales.dat')            
            
        if os.path.exists(photometry_sdss+'_r_asymptotic.dat'): 
            rr_mag[i] = get_mag(photometry_sdss+'_r_asymptotic.dat')
            r_Rasy[i] = get_mag(photometry_sdss+'_r_asymptotic.dat', index=1)/60.
            A_r[i]    = get_mag(photometry_sdss+'_r_asymptotic.dat', header='A_Gal:')
        if os.path.exists(photometry_sdss+'_r.scales.dat'):     
            ebv[i], A_r[i], mu0_r[i], mu50_r[i], mu90_r[i], m255_r[i], disc_mu0_r[i], SLh_r[i], R50_r[i], R90_r[i], R255_r[i], Cntion_r[i], d_m_ext_r[i] = get_scales(photometry_sdss+'_r.scales.dat')            
            
        if os.path.exists(photometry_sdss+'_i_asymptotic.dat'): 
            ii_mag[i] = get_mag(photometry_sdss+'_i_asymptotic.dat')
            i_Rasy[i] = get_mag(photometry_sdss+'_i_asymptotic.dat', index=1)/60.
            A_i[i]    = get_mag(photometry_sdss+'_i_asymptotic.dat', header='A_Gal:')
        if os.path.exists(photometry_sdss+'_i.scales.dat'):     
            ebv[i], A_i[i], mu0_i[i], mu50_i[i], mu90_i[i], m255_i[i], disc_mu0_i[i], SLh_i[i], R50_i[i], R90_i[i], R255_i[i], Cntion_i[i], d_m_ext_i[i] = get_scales(photometry_sdss+'_i.scales.dat')           
            
        if os.path.exists(photometry_sdss+'_z_asymptotic.dat'): 
            zz_mag[i] = get_mag(photometry_sdss+'_z_asymptotic.dat')
            z_Rasy[i] = get_mag(photometry_sdss+'_z_asymptotic.dat', index=1)/60.
            A_z[i]    = get_mag(photometry_sdss+'_z_asymptotic.dat', header='A_Gal:')
        if os.path.exists(photometry_sdss+'_z.scales.dat'):     
            ebv[i], A_z[i], mu0_z[i], mu50_z[i], mu90_z[i], m255_z[i], disc_mu0_z[i], SLh_z[i], R50_z[i], R90_z[i], R255_z[i], Cntion_z[i], d_m_ext_z[i] = get_scales(photometry_sdss+'_z.scales.dat')            


        ellipsefile = location_sdss + radb +'/photometry/'+pgcname+'_g_ellipsepar.dat'
        if os.path.exists(ellipsefile): 
            ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse(ellipsefile)
            Sba[i] = min([semimajor,semiminor])/max([semiminor,semimajor])
            Spa[i] = PA
            
        ellipsefile = location_sdss + radb +'/photometry/'+pgcname+'_r_ellipsepar.dat'
        if os.path.exists(ellipsefile): 
            ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse(ellipsefile)
            Sba[i] = min([semimajor,semiminor])/max([semiminor,semimajor])
            Spa[i] = PA            
            

        ellipsefile = location_sdss + radb +'/photometry/'+pgcname+'_i_ellipsepar.dat'
        if os.path.exists(ellipsefile): 
            ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse(ellipsefile)
            Sba[i] = min([semimajor,semiminor])/max([semiminor,semimajor])
            Spa[i] = PA




    if pgc_[i] in wise_pgc:
        i_lst = np.where(wise_pgc == pgc_[i])
        galname = wise_name[i_lst][0]
        qa_txt_wise = location_wise + radb + '/wise/fits/' + galname+'_qa.txt'
        if not os.path.exists(qa_txt_wise):
               galname = 'pgc'+str(pgc_[i])
    else:
        galname = 'pgc'+str(pgc_[i])
        
    qa_txt_wise = location_wise + radb + '/wise/fits/' + galname+'_qa.txt'
    photometry_wise =  location_wise + radb +'/photometry/'+galname
        
    if os.path.exists(qa_txt_wise):
        
        tmp = -9.99
        Wquality[i] = get_quality(qa_txt_wise)
        if os.path.exists(photometry_wise+'_w1_asymptotic.dat'): 
            w1_mag[i]  = get_mag_wise(photometry_wise+'_w1_asymptotic.dat')
            w1_Rasy[i] = get_mag_wise(photometry_wise+'_w1_asymptotic.dat', index=1)/60.
            A_w1[i]    = get_mag_f(photometry_wise+'_w1_asymptotic.dat', header='A_Gal:')
        if os.path.exists(photometry_wise+'_w1.scales.dat'):     
            tmp, A_w1[i], mu0_w1[i], mu50_w1[i], mu90_w1[i], m255_w1[i], disc_mu0_w1[i], SLh_w1[i], R50_w1[i], R90_w1[i], R255_w1[i], Cntion_w1[i], d_m_ext_w1[i] = get_scales(photometry_wise+'_w1.scales.dat')  
                        
        if os.path.exists(photometry_wise+'_w2_asymptotic.dat'): 
            w2_mag[i]  = get_mag_wise(photometry_wise+'_w2_asymptotic.dat')
            w2_Rasy[i] = get_mag_wise(photometry_wise+'_w2_asymptotic.dat', index=1)/60.
            A_w2[i]    = get_mag_f(photometry_wise+'_w2_asymptotic.dat', header='A_Gal:')
        if os.path.exists(photometry_wise+'_w2.scales.dat'):     
            tmp, A_w2[i], mu0_w2[i], mu50_w2[i], mu90_w2[i], m255_w2[i], disc_mu0_w2[i], SLh_w2[i], R50_w2[i], R90_w2[i], R255_w2[i], Cntion_w2[i], d_m_ext_w2[i] = get_scales(photometry_wise+'_w2.scales.dat')             
        
        if ebv[i]<0 and tmp>0:
            ebv[i] = tmp

        ellipsefile = location_wise + radb +'/photometry/'+galname+'_w2_ellipsepar.dat'
        if os.path.exists(ellipsefile): 
           ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse_wise(ellipsefile)
           Wba[i] = min([semimajor,semiminor])/max([semiminor,semimajor])
           Wpa[i] = PA
            
        ellipsefile = location_wise + radb +'/photometry/'+galname+'_w1_ellipsepar.dat'
        if os.path.exists(ellipsefile): 
           ra_cen, dec_cen, semimajor, semiminor, PA = get_ellipse_wise(ellipsefile)
           Wba[i] = min([semimajor,semiminor])/max([semiminor,semimajor])
           Wpa[i] = PA
    
##################################################################### Taking care of flags

    found = False
    if os.path.exists(qa_txt_sdss):
        qa_txt  = qa_txt_sdss
        found = True
        source[i] = 'SDSS'
    else:
        if QA_wise[i]==1:
            if pgc_[i] in wise_pgc:
                i_lst = np.where(wise_pgc == pgc_[i])
                galname = wise_name[i_lst][0]
                qa_txt_wise = location_wise + radb + '/wise/fits/' + galname+'_qa.txt'
                if not os.path.exists(qa_txt_wise):
                    galname = 'pgc'+str(pgc_[i])
            else:
                galname = 'pgc'+str(pgc_[i])
                
            qa_txt_wise = location_wise + radb + '/wise/fits/' + galname+'_qa.txt'
            if os.path.exists(qa_txt_wise):
                qa_txt  = qa_txt_wise
                found = True
                source[i] = 'WISE'
            else: 
                #print galname
                #print galname, ra[i], dec[i], d25[i], d25[i]*b_a[i], PA[i], Ty[i]
                source[i] = 'NONE'
            
            
    if found:

        if get_quality(qa_txt, nline=41)==1: disturbed[i]='D'
        if get_quality(qa_txt, nline=42)==1: trail[i]='L'
        if get_quality(qa_txt, nline=43)==1: not_spiral[i]='P'
        if get_quality(qa_txt, nline=44)==1: face_on[i]='F'
        if get_quality(qa_txt, nline=45)==1: faint[i]='N'
        if get_quality(qa_txt, nline=46)==1: crowded[i]='C'
        if get_quality(qa_txt, nline=47)==1: over_masked[i]='O'
        if get_quality(qa_txt, nline=20)==1: fov[i]='V'
        if get_quality(qa_txt, nline=19)==1: multiple[i]='M'
        if get_quality(qa_txt, nline=18)==1: bright_star[i]='B'  
        if get_quality(qa_txt, nline=17)==1: uncertain[i]='U'
        note[i]= read_note(qa_txt)  
    





#####################################################################

myTable = Table()
myTable.add_column(Column(data=pgc_, name='pgc'))
myTable.add_column(Column(data=ra_, name='ra', format='%0.4f'))
myTable.add_column(Column(data=dec_, name='dec', format='%0.4f'))
myTable.add_column(Column(data=l_, name='gl', format='%0.4f'))
myTable.add_column(Column(data=b_, name='gb', format='%0.4f'))
myTable.add_column(Column(data=sgl_, name='sgl', format='%0.4f'))
myTable.add_column(Column(data=sgb_, name='sgb', format='%0.4f'))
myTable.add_column(Column(data=d25_, name='d25', format='%0.2f'))
myTable.add_column(Column(data=b_a_, name='b_a', format='%0.2f'))
myTable.add_column(Column(data=pa_, name='pa', format='%0.1f'))
myTable.add_column(Column(data=ty_, name='ty', format='%0.1f'))
myTable.add_column(Column(data=type_, name='type'))
myTable.add_column(Column(data=sdss_, name='sdss'))
myTable.add_column(Column(data=alfa100, name='alfa100'))
myTable.add_column(Column(data=QA, name='QA_sdss'))
myTable.add_column(Column(data=QA_wise, name='QA_wise'))

myTable.add_column(Column(data=ebv, name='ebv', format='%0.3f'))

myTable.add_column(Column(data=uu_mag, name='u_mag', format='%0.2f'))
myTable.add_column(Column(data=gg_mag, name='g_mag', format='%0.2f'))
myTable.add_column(Column(data=rr_mag, name='r_mag', format='%0.2f'))
myTable.add_column(Column(data=ii_mag, name='i_mag', format='%0.2f'))
myTable.add_column(Column(data=zz_mag, name='z_mag', format='%0.2f'))

myTable.add_column(Column(data=u_Rasy, name='u_Rasy', format='%0.2f'))
myTable.add_column(Column(data=g_Rasy, name='g_Rasy', format='%0.2f'))
myTable.add_column(Column(data=r_Rasy, name='r_Rasy', format='%0.2f'))
myTable.add_column(Column(data=i_Rasy, name='i_Rasy', format='%0.2f'))
myTable.add_column(Column(data=z_Rasy, name='z_Rasy', format='%0.2f'))

myTable.add_column(Column(data=A_u, name='A_u', format='%0.3f'))
myTable.add_column(Column(data=A_g, name='A_g', format='%0.3f'))
myTable.add_column(Column(data=A_r, name='A_r', format='%0.3f'))
myTable.add_column(Column(data=A_i, name='A_i', format='%0.3f'))
myTable.add_column(Column(data=A_z, name='A_z', format='%0.3f'))

myTable.add_column(Column(data=Sba, name='Sba', format='%0.2f'))
myTable.add_column(Column(data=Spa, name='Spa', format='%0.2f'))


myTable.add_column(Column(data=mu0_u, name='mu0_u', format='%0.2f'))
myTable.add_column(Column(data=mu0_g, name='mu0_g', format='%0.2f'))
myTable.add_column(Column(data=mu0_r, name='mu0_r', format='%0.2f'))
myTable.add_column(Column(data=mu0_i, name='mu0_i', format='%0.2f'))
myTable.add_column(Column(data=mu0_z, name='mu0_z', format='%0.2f'))

myTable.add_column(Column(data=mu50_u, name='mu50_u', format='%0.2f'))
myTable.add_column(Column(data=mu50_g, name='mu50_g', format='%0.2f'))
myTable.add_column(Column(data=mu50_r, name='mu50_r', format='%0.2f'))
myTable.add_column(Column(data=mu50_i, name='mu50_i', format='%0.2f'))
myTable.add_column(Column(data=mu50_z, name='mu50_z', format='%0.2f'))

myTable.add_column(Column(data=mu90_u, name='mu90_u', format='%0.2f'))
myTable.add_column(Column(data=mu90_g, name='mu90_g', format='%0.2f'))
myTable.add_column(Column(data=mu90_r, name='mu90_r', format='%0.2f'))
myTable.add_column(Column(data=mu90_i, name='mu90_i', format='%0.2f'))
myTable.add_column(Column(data=mu90_z, name='mu90_z', format='%0.2f'))

myTable.add_column(Column(data=m255_u, name='m255_u', format='%0.2f'))
myTable.add_column(Column(data=m255_g, name='m255_g', format='%0.2f'))
myTable.add_column(Column(data=m255_r, name='m255_r', format='%0.2f'))
myTable.add_column(Column(data=m255_i, name='m255_i', format='%0.2f'))
myTable.add_column(Column(data=m255_z, name='m255_z', format='%0.2f'))

myTable.add_column(Column(data=disc_mu0_u, name='disc_mu0_u', format='%0.2f'))
myTable.add_column(Column(data=disc_mu0_g, name='disc_mu0_g', format='%0.2f'))
myTable.add_column(Column(data=disc_mu0_r, name='disc_mu0_r', format='%0.2f'))
myTable.add_column(Column(data=disc_mu0_i, name='disc_mu0_i', format='%0.2f'))
myTable.add_column(Column(data=disc_mu0_z, name='disc_mu0_z', format='%0.2f'))

myTable.add_column(Column(data=SLh_u, name='h_u', format='%0.2f'))
myTable.add_column(Column(data=SLh_g, name='h_g', format='%0.2f'))
myTable.add_column(Column(data=SLh_r, name='h_r', format='%0.2f'))
myTable.add_column(Column(data=SLh_i, name='h_i', format='%0.2f'))
myTable.add_column(Column(data=SLh_z, name='h_z', format='%0.2f'))

myTable.add_column(Column(data=R50_u, name='R50_u', format='%0.2f'))
myTable.add_column(Column(data=R50_g, name='R50_g', format='%0.2f'))
myTable.add_column(Column(data=R50_r, name='R50_r', format='%0.2f'))
myTable.add_column(Column(data=R50_i, name='R50_i', format='%0.2f'))
myTable.add_column(Column(data=R50_z, name='R50_z', format='%0.2f'))

myTable.add_column(Column(data=R90_u, name='R90_u', format='%0.2f'))
myTable.add_column(Column(data=R90_g, name='R90_g', format='%0.2f'))
myTable.add_column(Column(data=R90_r, name='R90_r', format='%0.2f'))
myTable.add_column(Column(data=R90_i, name='R90_i', format='%0.2f'))
myTable.add_column(Column(data=R90_z, name='R90_z', format='%0.2f'))

myTable.add_column(Column(data=R255_u, name='R255_u', format='%0.2f'))
myTable.add_column(Column(data=R255_g, name='R255_g', format='%0.2f'))
myTable.add_column(Column(data=R255_r, name='R255_r', format='%0.2f'))
myTable.add_column(Column(data=R255_i, name='R255_i', format='%0.2f'))
myTable.add_column(Column(data=R255_z, name='R255_z', format='%0.2f'))

myTable.add_column(Column(data=Cntion_u, name='C82_u', format='%0.2f'))
myTable.add_column(Column(data=Cntion_g, name='C82_g', format='%0.2f'))
myTable.add_column(Column(data=Cntion_r, name='C82_r', format='%0.2f'))
myTable.add_column(Column(data=Cntion_i, name='C82_i', format='%0.2f'))
myTable.add_column(Column(data=Cntion_z, name='C82_z', format='%0.2f'))

myTable.add_column(Column(data=d_m_ext_u, name='d_m_ext_u', format='%0.4f'))
myTable.add_column(Column(data=d_m_ext_g, name='d_m_ext_g', format='%0.4f'))
myTable.add_column(Column(data=d_m_ext_r, name='d_m_ext_r', format='%0.4f'))
myTable.add_column(Column(data=d_m_ext_i, name='d_m_ext_i', format='%0.4f'))
myTable.add_column(Column(data=d_m_ext_z, name='d_m_ext_z', format='%0.4f'))

myTable.add_column(Column(data=w1_mag, name='w1_mag', format='%0.2f'))
myTable.add_column(Column(data=w2_mag, name='w2_mag', format='%0.2f'))

myTable.add_column(Column(data=w1_Rasy, name='w1_Rasy', format='%0.2f'))
myTable.add_column(Column(data=w2_Rasy, name='w2_Rasy', format='%0.2f'))

myTable.add_column(Column(data=A_w1, name='A_w1', format='%0.3f'))
myTable.add_column(Column(data=A_w2, name='A_w2', format='%0.3f'))

myTable.add_column(Column(data=Wba, name='Wba', format='%0.2f'))
myTable.add_column(Column(data=Wpa, name='Wpa', format='%0.2f'))

myTable.add_column(Column(data=mu0_w1, name='mu0_w1', format='%0.2f'))
myTable.add_column(Column(data=mu0_w2, name='mu0_w2', format='%0.2f'))

myTable.add_column(Column(data=mu50_w1, name='mu50_w1', format='%0.2f'))
myTable.add_column(Column(data=mu50_w2, name='mu50_w2', format='%0.2f'))

myTable.add_column(Column(data=mu90_w1, name='mu90_w1', format='%0.2f'))
myTable.add_column(Column(data=mu90_w2, name='mu90_w2', format='%0.2f'))

myTable.add_column(Column(data=m255_w1, name='m255_w1', format='%0.2f'))
myTable.add_column(Column(data=m255_w2, name='m255_w2', format='%0.2f'))

myTable.add_column(Column(data=disc_mu0_w1, name='disc_mu0_w1', format='%0.2f'))
myTable.add_column(Column(data=disc_mu0_w2, name='disc_mu0_w2', format='%0.2f'))

myTable.add_column(Column(data=SLh_w1, name='h_w1', format='%0.2f'))
myTable.add_column(Column(data=SLh_w2, name='h_w2', format='%0.2f'))

myTable.add_column(Column(data=R50_w1, name='R50_w1', format='%0.2f'))
myTable.add_column(Column(data=R50_w2, name='R50_w2', format='%0.2f'))

myTable.add_column(Column(data=R90_w1, name='R90_w1', format='%0.2f'))
myTable.add_column(Column(data=R90_w2, name='R90_w2', format='%0.2f'))

myTable.add_column(Column(data=R255_w1, name='R255_w1', format='%0.2f'))
myTable.add_column(Column(data=R255_w2, name='R255_w2', format='%0.2f'))

myTable.add_column(Column(data=Cntion_w1, name='C82_w1', format='%0.2f'))
myTable.add_column(Column(data=Cntion_w2, name='C82_w2', format='%0.2f'))

myTable.add_column(Column(data=d_m_ext_w1, name='d_m_ext_w1', format='%0.4f'))
myTable.add_column(Column(data=d_m_ext_w2, name='d_m_ext_w2', format='%0.4f'))

myTable.add_column(Column(data=Squality,  name='Sqlt', dtype=np.dtype(int)))
myTable.add_column(Column(data=Wquality,  name='Wqlt', dtype=np.dtype(int)))

#myTable.add_column(Column(data=source,  name='source', dtype='S4'))


myTable.add_column(Column(data=disturbed,  name='dst', dtype='S1'))
myTable.add_column(Column(data=trail,  name='trl', dtype='S1'))
myTable.add_column(Column(data=not_spiral,  name='nsp', dtype='S1'))
myTable.add_column(Column(data=face_on,  name='fon', dtype='S1'))
myTable.add_column(Column(data=faint,  name='fnt', dtype='S1'))
myTable.add_column(Column(data=crowded,  name='cwd', dtype='S1'))
myTable.add_column(Column(data=over_masked,  name='ovm', dtype='S1'))
myTable.add_column(Column(data=fov,  name='fov', dtype='S1'))
myTable.add_column(Column(data=multiple,  name='mlp', dtype='S1'))
myTable.add_column(Column(data=bright_star,  name='bts', dtype='S1'))
myTable.add_column(Column(data=uncertain,  name='unc', dtype='S1'))
myTable.add_column(Column(data=note,  name='note', dtype='S100'))

myTable.add_column(Column(data=inc, name='inc', format='%0.2f'))
myTable.add_column(Column(data=inc_e, name='inc_e', format='%0.2f'))
myTable.add_column(Column(data=inc_flg, name='inc_flg', format='%1d'))
myTable.add_column(Column(data=inc_n, name='inc_n', format='%2d'))
myTable.add_column(Column(data=inc_note,  name='inc_note', dtype='S80'))

myTable.write('EDD_distance_cf4_v20.csv', format='ascii.fixed_width',delimiter='|', bookend=False, overwrite=True) 
