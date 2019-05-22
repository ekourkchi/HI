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

def deg2HMS(ra='', dec='', round=False):
  RA, DEC, rs, ds = '', '', '', ''
  if dec:
    if str(dec)[0] == '-':
      ds, dec = '-', abs(dec)
    deg = int(dec)
    decM = abs(int((dec-deg)*60))
    if round:
      decS = int((abs((dec-deg)*60)-decM)*60)
    else:
      decS = (abs((dec-deg)*60)-decM)*60
    DEC = '{0}{1} {2} {3}'.format(ds, deg, decM, decS)
    Ddec = '{0}{1}'.format(ds, deg)
    Mdec = '{0}'.format(decM)
    Sdec = '{0}'.format(decS)
    
  
  if ra:
    if str(ra)[0] == '-':
      rs, ra = '-', abs(ra)
    raH = int(ra/15)
    raM = int(((ra/15)-raH)*60)
    if round:
      raS = int(((((ra/15)-raH)*60)-raM)*60)
    else:
      raS = ((((ra/15)-raH)*60)-raM)*60
    RA = '{0}{1} {2} {3}'.format(rs, raH, raM, raS)
    Hra = '{0}{1}'.format(rs, raH)
    Mra = '{0}'.format(raM)
    Sra = '{0}'.format(raS)
  
  if ra and dec:
    return (RA, DEC)
  else:
    if RA:
      return Hra, Mra, Sra
    if DEC:
      return Ddec, Mdec, Sdec
    
#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.


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


#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.


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

###############################
def isInSDSS_DR12(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcl.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0
  
###############################

def isInSDSS_DR7(ra, dec):
  
  querry = "select dbo.fInFootprintEq("+str(ra)+","+str(dec)+", 1)"
  lines = sqlcldr7.query(querry).readlines()
  if lines[2] == "True\n": 
    return 1
  else: 
    return 0

###############################

def really_isInSDSS_DR12(ra, dec):
  querry = "SELECT TOP 10 p.fieldID FROM Field AS p WHERE "+str(dec)+" BETWEEN p.decMin AND p.decMAx AND "+str(ra)+"  BETWEEN p.raMin AND p.raMax"
  lines = sqlcl.query(querry).readlines()
  if len(lines) == 2: 
    return 0
  else: 
    return 1

###############################

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
    s = -1.
  elif s == 0 and ra_dec[8] == '+':
    s = 1.


  dec_deg = s*(np.abs(float(dec_d))+float(dec_m)/60.+float(dec_s)/3600.)

  return ra_hex, dec_hex, ra_deg, dec_deg


def hms_dms(ra_hex, dec_hex):
  
  ra_h = np.int(ra_hex[0:2])
  ra_m = np.int(ra_hex[3:5])
  ra_s = np.float(ra_hex[6:10])
  
  dec_d = np.int(dec_hex[0:3])
  dec_m = np.int(dec_hex[4:6])
  dec_s = np.float(dec_hex[7:11])
  
  return [ra_h, ra_m, ra_s, dec_d, dec_m, dec_s]
  
  

###############################



inFile = 'wise_photometry.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)

pgc        = table['PGC']
name       = table['Name']
ra         = table['RAJ']   # deg
dec        = table['DEJ']   # deg
a          = table['MAJ']   # arcmin
b          = table['MIN']   # arcmin

PA         = table['PA']

u          = table['u']     # 
g          = table['g']     # 
r          = table['r']     # 
ii          = table['i']     # 
z          = table['z']     # 




n_selected = len(pgc)



with open('html_db/wise_photometry.tbl.html', 'w+') as f:
  
  
  # There are bunch of java-scripts which are called, all available in "esn.js"
  s = """
 

<table class="wiki">

<tr style="background-color: #B6B6B4;"><td> no </td><td> PGC </td><td> Name </td><td> RA </td><td> DEC </td><td>  u </td><td>  g </td><td> r </td><td> i  </td><td> z </td><td> semi-major </td><td> b/a </td><td> PA </td><td> NED </td><td> SDSS </td><td> IRSA </td></tr>
<tr style="background-color: #B6B6B4;"><td> # </td><td> (EDD) </td><td>  </td><td> (deg) </td><td> (deg) </td><td>  (mag) </td><td>  (mag) </td><td> (mag) </td><td> (mag) </td><td> (mag) </td><td> (arcmin) </td><td> </td><td> (deg) </td><td> r=0.1' </td><td> DR12 </td><td>  </td></tr>
\n"""
  f.write(s)
  no = 0 

  for i in range(n_selected):
        
        no += 1
        print no, "of", n_selected


	
	ned_radius = 0.1  # arcmin = 6 arcsec
	hms = deg2HMS(ra=ra[i])
	dms = deg2HMS(dec=dec[i])
	


	size = a[i]/30.
	if size < 0.035: size = 0.035
	if size > 1 : size = 1


        # This says each row turns yellow on click-on
	s = '\n<tr onclick=\"javascript: toggleBgColor(this);\">'
	
	s += "<td> " + str(no) + " " + " </td>"
	
	s += " <td> " + "<a class=\"ext-link\"  href=\"javascript:edd("+str(pgc[i])+")\" onclick=\"edd("+str(pgc[i])+"); return false;\"><span class=\"icon\"> "+str(pgc[i])+" </span></a>" + " </td>"
	s += " <td> " + str(name[i]) + " </td>"
	#s += " <td> " + ra_hex + " </td>"
	#s += " <td> " + dec_hex + " </td>"
	s += " <td> " + '{:.4f}'.format(ra[i]) + " </td>"
	s += " <td> " + '{:.4f}'.format(dec[i]) + " </td>"

	if u[i] > 0: 
	  s += " <td> " + str(u[i]) + " </td>"
	else: 
	  s += " <td> " + " " + " </td>"
	  
	if g[i] > 0: 
	  s += " <td> " + str(g[i]) + " </td>"
	else: 
	  s += " <td> " + " " + " </td>"

	if r[i] > 0: 
	  s += " <td> " + str(r[i]) + " </td>"
	else: 
	  s += " <td> " + " " + " </td>"

	if ii[i] > 0: 
	  s += " <td> " + str(ii[i]) + " </td>"
	else: 
	  s += " <td> " + " " + " </td>"

	if z[i] > 0: 
	  s += " <td> " + str(z[i]) + " </td>"
	else: 
	  s += " <td> " + " " + " </td>"


	s += " <td> " + str(a[i])

	s += " <td> " + '{:.2f}'.format(b[i]/a[i]) + " </td>"

	s += " <td> " + '{:.1f}'.format(PA[i]) + " </td>"


        java_ned = "ned("+str(hms[0])+","+str(hms[1])+","+str(hms[2])+","+str([0])+","+str(dms[1])+","+str(dms[2])+")"
	s += " <td> " + "<a class=\"ext-link\"  target=\"ned_blank\"  href=\"javascript:" + java_ned + "\" onclick=\""+ java_ned +"; return false;\"><span class=\"icon\"> NED </span></a>" + " </td>"


	if isInSDSS_DR12(ra[i], dec[i]) == 1: 
	  s += " <td> " + "<button onclick=\"sdss("+str(ra[i])+","+str(dec[i])+","+str(0.2*a[i])+")\">SDSS</button>" + " </td>"
	elif really_isInSDSS_DR12(ra[i], dec) == 1:
	  s += " <td> " + "<button onclick=\"sdss("+str(ra[i])+","+str(dec[i])+","+str(0.2*a[i])+")\">SDSS</button>" + " </td>"
	else:
	  s += " <td> " + " </td>"

	s += " <td> " + "<button onclick=\"irsa("+str(ra[i])+","+str(dec[i])+","+str(size)+")\">IRSA</button>" + " </td>"


	s += "</tr>\n"
	
	f.write(s)


  s = "\n</table>\n\n"
  
  
  ## Print the date after the table is generated
  s += """
 <div id="altlinks">
   <br />
   <ul>
      <li class="last first">
      <a rel="nofollow">Created on """+ subprocess.check_output(["date"]) + """</a>
      </li>
   </ul>
 </div>  
 """

  f.write(s)
  # for-loop ends


