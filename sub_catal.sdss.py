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
import sqlcldr7

#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.

def isInSDSS_DR12(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcl.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
  

def isInSDSS_DR7(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcldr7.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
 
def really_isInSDSS_DR12(ra, dec):
  querry = "SELECT TOP 10 p.fieldID FROM Field AS p WHERE "+str(dec)+" BETWEEN p.decMin AND p.decMAx AND "+str(ra)+"  BETWEEN p.raMin AND p.raMax"
  lines = sqlcl.query(querry).readlines()
  if len(lines) == 2: 
    return 0
  else: 
    return 1


def cordiante_parser(ra_dec):
  
  # J2000
  # example: 004244.4+411608.0
  while ra_dec[0] == ' ': ra_dec = ra_dec[1:]

  ra_h = ra_dec[0:2]
  ra_m = ra_dec[2:4]
  ra_s = ra_dec[4:8]
  ra_hex = ra_h+":"+ra_m+":"+ra_s
  ra_deg = 15.*(float(ra_h)+float(ra_m)/60.+float(ra_s)/3600.)


  dec_d = ra_dec[8:11]
  dec_m = ra_dec[11:13]
  dec_s = ra_dec[13:17]
  dec_hex = dec_d+":"+dec_m+":"+dec_s
  s = np.sign(float(dec_d))
  
  if s == 0 and ra_dec[8] == '-':
    s = -1
  elif s == 0 and ra_dec[8] == '+':
    s = 1

  
  
  dec_deg = s*(np.abs(float(dec_d))+float(dec_m)/60.+float(dec_s)/3600.)

  return ra_hex, dec_hex, ra_deg, dec_deg



inFile = 'brent_list/edd_HI_ba_T_9060.short.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc         = table['PGC']
radec       = table['RA_J2000_Dec']
d25         = table['d25']
B_mag       = table['Bt']
I_mag       =  table['It']
axial_ratio =  table['b_a']


id = float(sys.argv[1])
no = sys.argv[2]

i = 0
while  pgc[i] != id:
  i+=1

ra_hex, dec_hex, ra, dec = cordiante_parser(radec[i])


edd = "http://edd.ifa.hawaii.edu/get_results_pgc.php?pgc="+str(pgc[i])

sdss =  "http://skyservice.pha.jhu.edu/DR12/ImgCutout/getjpeg.aspx?ra="+str(ra)+"&"+"dec="+str(dec)+"&scale="+str(0.2*d25[i])+"&width=800&height=800&opt=G"


size = d25[i]/30.
if size < 0.035: size = 0.035
if size > 1 : size = 1

irsa = "http://irsa.ipac.caltech.edu/applications/finderchart/#id=Hydra_finderchart_finder_chart&RequestClass=ServerRequest&DoSearch=true&subsize="+str(size)+"&thumbnail_size=medium&sources=DSS,SDSS,twomass,WISE&overlay_catalog=true&catalog_by_radius=true&sdss_radius=5&twomass_radius=5&wise_radius=5&one_to_one=_none_&UserTargetWorldPt="+str(ra)+";"+str(dec)+";EQ_J2000&SimpleTargetPanel.field.resolvedBy=nedthensimbad&dss_bands=poss1_blue,poss1_red,poss2ukstu_blue,poss2ukstu_red,poss2ukstu_ir&SDSS_bands=u,g,r,i,z&twomass_bands=j,h,k&wise_bands=1,2,3,4&projectId=finderchart&searchName=finder_chart&shortDesc=Finder%20Chart&isBookmarkAble=true&isDrillDownRoot=true&isSearchResult=true"




s = ''
s += "|| " + no + " " 
s += " || " + str(pgc[i])
s += " || " + ra_hex
s += " || " + dec_hex
s += " || " + '{:.5f}'.format(ra)
s += " || " + '{:.5f}'.format(dec)
s += " || " + str(d25[i])

if B_mag[i] != 0: 
  s += " || " + str(B_mag[i])
else: 
  s += " || " + " "

if I_mag[i] != 0: 
  s += " || " + str(I_mag[i])
else: 
  s += " || " + " "


s += " || " + str(axial_ratio[i])
s += " || " + "[" + edd + " EDD]"

if isInSDSS_DR12(ra, dec) == 1: 
  s += " || " + "[" + sdss + " SDSS-DR12]"
  hasSDSS = 1
elif really_isInSDSS_DR12(ra, dec) == 1:
  s += " || " + "[" + sdss + " SDSS-DR12]"
  hasSDSS = 1
else:
  s += " || SDSS-DR12"
  hasSDSS = 0
s += " || " + "[" + irsa + " IRSA]"
s += " ||"


if hasSDSS == 1:
  print s 


print ra, dec

