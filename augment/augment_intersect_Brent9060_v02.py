#!/usr/bin/python
import sys
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
#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.
##########################################
###############################

def cordiante_parser(ra_dec):
  
  # J2000
  # example: 004244.4+411608.0
  while ra_dec[0] == ' ': ra_dec = ra_dec[1:]

  ra_h = ra_dec[0:2]
  ra_m = ra_dec[2:4]
  ra_s = ra_dec[4:8]

  ra_deg = 15.*(float(ra_h)+float(ra_m)/60.+float(ra_s)/3600.)


  dec_d = ra_dec[8:11]
  dec_m = ra_dec[11:13]
  dec_s = ra_dec[13:17]

  s = np.sign(float(dec_d))

  if s == 0 and ra_dec[8] == '-':
    s = -1.
  elif s == 0 and ra_dec[8] == '+':
    s = 1.


  dec_deg = s*(np.abs(float(dec_d))+float(dec_m)/60.+float(dec_s)/3600.)

  return ra_deg, dec_deg


###############################


###############################
def isInSDSS_DR12(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcl.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
  
###############################
def extract_pgc(ID):
    
    return int(ID[3:10])
##########################################

def read_glga(filename):
  
  pgc_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    pgc = columns[0]
    pgc_ID = pgc[3:len(pgc)]
    pgc_lst.append(int(pgc_ID))
  
  return pgc_lst 

##########################################

def read_glga_wise(filename):
  
  name_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    name_ID = columns[0]
    name_lst.append(name_ID)
  
  return name_lst 

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
#################################################################
def SDSS_db_avilability(pgc, ra, dec, Filters=['u', 'g', 'r', 'i', 'z'], db_dir='', toDbase=False):
   
   pgc_dir = "pgc"+str(pgc)
   directory = "/home/ehsan/db_esn/Alfalfa70_SDSS_REPO/"+pgc_dir
   isDirAvailable =  os.path.isdir(directory)
   
   file_existence = 0
   
   if isDirAvailable:
     
     ra_id = str(int(np.floor(ra)))
     if ra < 10:
       ra_id = '00'+ra_id+'D'
     elif ra < 100:
       ra_id = '0'+ra_id+'D'
     else:
       ra_id = ra_id+'D'
     

     desitination = db_dir + ra_id + '/sdss/fits/'
     
     
     for filters in Filters:
        fname = directory+'/'+pgc_dir+'_'+filters+'.fits.gz'
        fname2 = '/home/ehsan/Dropbox/Home/PanStarrs/Jan/HI/SDSS+/'+pgc_dir+'_'+filters+'.fits.gz'
        if os.path.exists(fname):
	   
	   file_existence += 1
	   if toDbase:
	      command = ["cp", fname, desitination]
	      subprocess.call(command)
	      subprocess.call(['gunzip', '-f', desitination+pgc_dir+'_'+filters+'.fits.gz'])
           


   return file_existence


#################################################################
def exclude(pgc, pgc_ex):
  
  pgc = np.asarray(pgc)
  pgc_ex = np.asarray(pgc_ex)
  pgc_ex = np.sort(pgc_ex)
  
  n0 = len(pgc)
  n_ex = len(pgc_ex)
  
  indices = np.arange(n0)
  ind_srot = np.argsort(pgc)
  indices = indices[ind_srot]
  pgc = pgc[ind_srot]
  
  j = 0 
  for i in range(n_ex):
    while(pgc[j] < pgc_ex[i] and pgc[j]  < n0):
      j+=1
    if pgc[j] == pgc_ex[i]:
      indices[j] = -1   # will be excluded
      j+=1
  
  return (indices[np.where(indices > -1)],)
  

#################


def intersect(pgc, pgc_ex):
  
  pgc = np.asarray(pgc)
  pgc_ex = np.asarray(pgc_ex)
  pgc_ex = np.sort(pgc_ex)
  
  n0 = len(pgc)
  n_ex = len(pgc_ex)
  
  indices = np.arange(n0)
  ind_srot = np.argsort(pgc)
  indices = indices[ind_srot]
  pgc = pgc[ind_srot]
  
  j = 0 
  common_indices = []
  for i in range(n_ex):
    while(pgc[j] < pgc_ex[i] and pgc[j]  < n0):
      j+=1
    if pgc[j] == pgc_ex[i]:
      common_indices.append(indices[j])   # will be kept (that's in the intersect region)
      j+=1
  
  indices = np.asarray(common_indices)
  return (indices,)
  

#################
def QA_SDSS_DONE(pgc, ra):
    
    
    databse = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/'+'/cf4_sdss/data/'
    
    name = 'pgc'+str(pgc)
    if os.path.exists(databse+ra_db(ra)+'/sdss/fits/'+name+'_qa.txt'):
        return True
        
    return False   
#################
def QA_WISE_DONE(pgc, ra):
    
    global wise_name, wise_pgc
    
    databse = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/'+'/cf4_wise/data/'
    
    if pgc in wise_pgc:
        i_lst = np.where(pgc == wise_pgc)
        name = wise_name[i_lst][0] 
        if os.path.exists(databse+ra_db(ra)+'/wise/fits/'+name+'_qa.txt'):
            return True
    
    name = 'pgc'+str(pgc)
    if os.path.exists(databse+ra_db(ra)+'/wise/fits/'+name+'_qa.txt'):
        return True
        
    return False    
    
########################################################### Begin
inFile = '../brent_list/edd_HI_ba_T_9060.short.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc      = table['PGC']
d25      = table['d25']
l = table['l']
b = table['b']
sgl = table['sgl']
sgb = table['sgb']
b_a     = table['b_a']
PA      = table['PA']
Ty      = table['Ty']

inFile = '../has_Hall.SDSS.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc_p      = table['pgc']
ra      = table['ra']
dec      = table['dec']
sdss    = table['SDSS']
############################################################
inFile = 'a70_Tge1_ige60_Wge70_SNgt5.9832.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc_ex      = table['PGC']
lgd25_ex      = table['lgd25']
l_ex = table['l']
b_ex = table['b']
sgl_ex = table['sgl']
sgb_ex = table['sgb']
lgr25_ex     = table['lgr25']
Ty_ex        = table['T']
b_a_ex = 1./(10**lgr25_ex)

pa_ex = b_a_ex*0.


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
for i in range(len(pgc_ex)):
    for j in range(len(pgc_leda)):
        if pgc_ex[i] == pgc_leda[j]:
            pa_ex[i] = pa_leda[j]
            break








### END



inFile = 'a70_Tge1_ige60_Wge70_SNgt5.9832_has_SDSS.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc_ex_p      = table['pgc']
ra_ex      = table['ra']
dec_ex      = table['dec']
sdss_ex    = table['SDSS']
############################################################



pgc_  = []
ra_   = []
dec_  = []
l_    = []
b_    = []
sgl_  = []
sgb_  = []
sdss_ = []
d25_  = []
alfalfa70 = []
QA   = []
QA_wise = []
pa_  = []
b_a_ = []
ty_  = []
type_ = []


for i in range(len(pgc)):
    if not pgc[i] in pgc_:
        pgc_.append(pgc[i])
        ra_.append(ra[i])
        dec_.append(dec[i])
        l_.append(l[i])
        b_.append(b[i])
        sgl_.append(sgl[i])
        sgb_.append(sgb[i])
        d25_.append(d25[i])
        sdss_.append(sdss[i]) 
        pa_.append(PA[i]) 
        b_a_.append(b_a[i])
        ty_.append(Ty[i])
        if pgc[i] in pgc_ex:
          alfalfa70.append(1) 
        else:
          alfalfa70.append(0) 
          
        if QA_SDSS_DONE(pgc[i], ra[i]):
            QA.append(1) 
        else: QA.append(0) 
        
        if QA_WISE_DONE(pgc[i], ra[i]):
            QA_wise.append(1) 
        else: QA_wise.append(0)        
        

for i in range(len(pgc_ex)):
    if not pgc_ex[i] in pgc_:
        pgc_.append(pgc_ex[i])
        ra_.append(ra_ex[i])
        dec_.append(dec_ex[i])
        l_.append(l_ex[i])
        b_.append(b_ex[i])
        sgl_.append(sgl_ex[i])
        sgb_.append(sgb_ex[i])
        d25_.append(0.1*(10**lgd25_ex[i]))
        sdss_.append(sdss_ex[i]) 
        pa_.append(pa_ex[i])
        b_a_.append(b_a_ex[i])
        ty_.append(Ty_ex[i])
        alfalfa70.append(1) 
        if QA_SDSS_DONE(pgc_ex[i], ra_ex[i]):
            QA.append(1) 
        else: QA.append(0) 

        if  QA_WISE_DONE(pgc_ex[i], ra_ex[i]):
            QA_wise.append(1) 
        else: QA_wise.append(0) 





inFile = 'leda_nancy.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_nancy    = table['pgc']
ra_nancy     = table['al2000']
ra_nancy *= 15.
dec_nancy    = table['de2000']
l_nancy      = table['l2']
b_nancy      = table['b2']
sgl_nancy    = table['sgl']
sgb_nancy    = table['sgb']
logd25_nancy = table['logd25']
logr25_nancy = table['logr25']
pa_nancy     = table['pa']
ty_nancy     = table['t']
type_nancy   = table['type']

for i in range(len(pgc_nancy)):

    
    if not pgc_nancy[i] in pgc_:
                pgc_.append(pgc_nancy[i])
                ra_.append(ra_nancy[i])
                dec_.append(dec_nancy[i])
                l_.append(l_nancy[i])
                b_.append(b_nancy[i])
                sgl_.append(sgl_nancy[i])
                sgb_.append(sgb_nancy[i])
                d25_.append(0.1*(10**logd25_nancy[i]))
                
                if isInSDSS_DR12(ra_nancy[i], dec_nancy[i]) == 1:
                    sdss_.append(1) 
                else:
                    sdss_.append(0) 
                
                
                
                pa_.append(pa_nancy[i])
                b_a_.append(1./(10**logr25_nancy[i]))
                ty_.append(ty_nancy[i])
                alfalfa70.append(0) 
                if QA_SDSS_DONE(pgc_nancy[i], ra_nancy[i]):
                    QA.append(1) 
                else: QA.append(0) 

                if  QA_WISE_DONE(pgc_nancy[i], ra_nancy[i]):
                    QA_wise.append(1) 
                else: QA_wise.append(0)   







###  12257 Perseus
###  40201 Virgo
###  40303 Virgo
###  40811 Virgo
###  41763 Virgo
pgc_add = [12257, 40201, 40303, 40811, 41763]
#####################################################

inFile = 'TFcalibrators.csv'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc_TFcalibrators    = table['PGC']

p = 0 
for i in range(len(pgc_TFcalibrators)):
    
    new_pgc = pgc_TFcalibrators[i]
    if not new_pgc in pgc_:
        pgc_add.append(new_pgc)
        p+=1
 
print "New TF gals: #", p


#####################################################
inFile = 'cand_100007.59.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_TFcalibrators    = table['PGC']

p = 0 
for i in range(len(pgc_TFcalibrators)):
    
    new_pgc = pgc_TFcalibrators[i]
    if not new_pgc in pgc_:
        pgc_add.append(new_pgc)
        p+=1
 
print "New TF gals: #", p

#####################################################

inFile = 'TFcalibrators_Arecibo.csv'
table = np.genfromtxt(inFile , delimiter='|', filling_values=None, names=True, dtype=None)
pgc_TF_arecibo    = table['PGC']
RADE_TF_arecibo   = table['RADE']
TY_TF_arecibo     = table['T']
logr25_TF_arecibo = table['logr25']
Glon_TF_arecibo = table['Glon']
Glat_TF_arecibo = table['Glat']
SGL_TF_arecibo = table['SGL']
SGB_TF_arecibo = table['SGB']
b_a_TF_arecibo = 1./(10**logr25_TF_arecibo)

p = 0 
for i in range(len(pgc_TF_arecibo)):
    
    new_pgc = pgc_TF_arecibo[i]
    if not new_pgc in pgc_:
        pgc_add.append(new_pgc)
        p+=1
 
print "New TF gals: #", p

#####################################################
for i in range(len(pgc_add)):
    
    j = 0
    for j in range(len(pgc_leda)):
        if pgc_leda[j] == pgc_add[i]:
            if not pgc_add[i] in pgc_:
                
                pgc_.append(pgc_leda[j])
                
                if pgc_add[i] in pgc_TF_arecibo:
                    
                    i_lst = np.where(pgc_add[i] == pgc_TF_arecibo)[0]
                    
                    rag, decg  = cordiante_parser(RADE_TF_arecibo[i_lst][0])
                    ra_.append(rag)
                    ra000 = rag
                    dec000 = decg
                    dec_.append(decg)
                    b_a_.append(b_a_TF_arecibo[i_lst][0])
                    ty_.append(TY_TF_arecibo[i_lst][0])
                    l_.append(Glon_TF_arecibo[i_lst][0])
                    b_.append(Glat_TF_arecibo[i_lst][0])
                    sgl_.append(SGL_TF_arecibo[i_lst][0])
                    sgb_.append(SGB_TF_arecibo[i_lst][0])
                else:
                    ra000 = ra_leda[j]
                    dec000 = dec_leda[j]
                    ra_.append(ra_leda[j])
                    dec_.append(dec_leda[j])
                    b_a_.append(1./(10**logr25_leda[j]))
                    ty_.append(ty_leda[j])
                    l_.append(l_leda[j])
                    b_.append(b_leda[j])
                    sgl_.append(sgl_leda[j])
                    sgb_.append(sgb_leda[j])
  
                d25_.append(0.1*(10**logd25_leda[j]))
                
                if isInSDSS_DR12(ra000, dec000) == 1:
                   sdss_.append(1) 
                else:
                   sdss_.append(0)
                   
                pa_.append(pa_leda[j])
                
                
                alfalfa70.append(0) 
                if QA_SDSS_DONE(pgc_leda[j], ra000):
                    QA.append(1) 
                else: QA.append(0) 

                if  QA_WISE_DONE(pgc_leda[j], ra000):
                    QA_wise.append(1) 
                else: QA_wise.append(0)             
            
            break
 



for i in range(len(pgc_)):
    myType =''
    for j in range(len(pgc_leda)):
        if pgc_[i] == pgc_leda[j]:
            myType = type_leda[j]
            break
    type_.append(myType)



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
alfalfa70 = np.asarray(alfalfa70)
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
alfalfa70 = alfalfa70[index]
QA        = QA[index]
QA_wise   = QA_wise[index]


for i in range(len(pgc_)):
    
    gal = pgc_[i]
    if gal in [58411,58239,17170,1977897]:
        sdss_[i] = 0 





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
myTable.add_column(Column(data=alfalfa70, name='alfalfa70'))
myTable.add_column(Column(data=QA, name='QA_sdss'))
myTable.add_column(Column(data=QA_wise, name='QA_wise'))
myTable.write('EDD_distance_cf4_v10.csv', format='ascii.fixed_width',delimiter='|', bookend=False) 

#sum = 0
#db_dir = '/run/media/ehsan/6ccd3c78-12e8-4f00-815d-faf200b314cf/ehsan/db_esn/data_alf_test/'
#with open('data_set_12.glga', 'w') as file:
    #for i in range(len(pgc_)):
        
        #if alfalfa70[i] == 1 and QA[i] == 1:
            
            ##print pgc_[i], SDSS_db_avilability(pgc_[i], ra_[i], dec_[i])
            #if SDSS_db_avilability(pgc_[i], ra_[i], dec_[i], Filters=['g','r','i'])==3: 
                #for j in range(len(pgc)):
                    #if pgc[j] == pgc_[i]:
                       #ty0  =  Ty[j]
                       #pa0  =  PA[j]
                       #b_a0 =  b_a[j]
                       ##print 'pgc'+str(pgc_[i]), ra_[i], dec_[i], d25_[i], d25_[i]*b_a0, pa0, ty0
                       ##file.write('{0} {1} {2} {3} {4} {5} {6}\n'.format('pgc'+str(pgc_[i]), ra_[i], dec_[i], d25_[i], d25_[i]*b_a0, pa0, ty0))
                       ##SDSS_db_avilability(pgc_[i], ra_[i], dec_[i], db_dir=db_dir, toDbase=True)

                       #sum+=1
                       #break
        
        

#print sum
    
    

############################################################
### WISE 

#inFile = 'wise_needs_qa_pgc.csv'
#table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

#pgc_wise       = table['pgc']
#name_wise      = table['name']

#pgc_wise_ = []
#name_wise_ = []
#d25_wise_ = []
#sdss_wise_ = []
#ra_wise_ = []
#dec_wise_ = []

#with open('wise_needs_qa_cosmicflows_set02.glga', 'w') as file:
    #for i in range(len(pgc_wise)):
        
        #print i
        #for j in range(len(pgc_)):
          ##if int(pgc_wise[i]) == pgc_[j] and (dec_[j]<-20 or (d25_[j]>1.5 and sdss_[j]==0)): # wise_needs_qa_cosmicflows_set01
          #if int(pgc_wise[i]) == pgc_[j] and (dec_[j]>=-20 and (d25_[j]<=1.5 and sdss_[j]==0)): # wise_needs_qa_cosmicflows_set02
           
           #pgc_wise_.append(pgc_wise[i])
           #name_wise_.append(name_wise[i])
           #d25_wise_.append(d25_[j])
           #sdss_wise_.append(sdss_[j])
           #ra_wise_.append(ra_[j])
           #dec_wise_.append(dec_[j])
           
           #ind = j
           #file.write('{0} {1} {2} {3} {4} {5} {6}\n'.format(name_wise[i], ra_[ind], dec_[ind], d25_[ind], d25_[ind]*b_a_[ind], pa_[ind], type_[ind]))
           #break
       
    
    
#print len(pgc_wise_)   
#myTable = Table()
#myTable.add_column(Column(data=pgc_wise_, name='pgc'))
#myTable.add_column(Column(data=name_wise_, name='name'))
#myTable.add_column(Column(data=ra_wise_, name='ra', format='%0.4f'))
#myTable.add_column(Column(data=dec_wise_, name='dec', format='%0.4f'))
#myTable.add_column(Column(data=d25_wise_, name='d25_arcmin', format='%0.2f'))
#myTable.add_column(Column(data=sdss_wise_, name='sdss'))
#myTable.write('wise_needs_qa_cosmicflows_set02.csv', format='ascii.fixed_width',delimiter=',', bookend=False) 

#print sum(sdss_wise_)

############################################################


