#!/usr/bin/python
import sys
import os.path
import subprocess
import glob

from time import time

import numpy as np
from math import *
from astrometry.util.starutil_numpy import * 
from astrometry.libkd import spherematch
import random 

import pyfits
#from pyfits import *
from numpy import radians, degrees, sin, cos, arctan2, hypot
#from k3match import *
from astropy.io import fits


##########################################
# Previous Tries 

### This is the pilot_01 Tester --- for SDSS
pilot_01 = [47346, 31037, 23069, 23340, 53043, 32774, 10496, 70175, 38392, 54234, 5344, 39114, 39224, 23071, 50042, 52307, 49468, 7262, 35999, 39308, 42544, 48959, 41779, 51955, 71926, 51253, 55665, 43707, 49820, 9549, 32251, 37591, 49497, 49347, 50317, 51706, 41061, 50676, 45795, 26690, 33964, 40621, 43330, 10010, 51587, 45848, 34917, 43020, 37525, 69270, 65131, 39950, 38492, 38031, 57261, 50216, 255, 40119, 23028, 5688, 42707, 26390, 32321, 72788, 32763, 32207, 28148, 38897, 32648, 22506, 8913, 25910, 9272, 54267, 31059, 30895, 44086, 28010, 52877, 46952, 39040, 60291, 29956, 10766, 56537, 51610, 35224, 19743, 57627, 27734, 34248, 21676, 30531, 56094, 34971, 47985, 65506, 20458, 798, 29415, 45787, 47422, 41578, 49158, 28590, 24490, 8173, 41755, 58960, 66151, 21684, 25237, 29427, 49041, 4896, 34718, 36493, 31708, 37429, 58501, 34913, 2479, 30885, 43837, 55097, 39390, 54761, 37723, 71883, 1841, 49112, 41088, 46636, 59681, 61008, 35249, 42898, 53231, 21918, 28324, 33866, 5792, 39366, 57522, 46386, 23725, 41766, 23512, 53802, 33401, 86292, 40516, 36536, 12333, 36102, 49889, 33940, 36996, 354, 71826, 49322, 23646, 42396, 36979, 47869, 64638, 28274, 303, 5450, 67120, 4116, 51498, 67205, 47680, 1921, 56287, 50092, 22389, 205, 28821, 40330, 54385, 29468, 28126, 56108, 58538, 31697, 58059, 59657, 48118, 26287, 39150, 68552, 23447, 55867, 23441, 51741, 39113, 43575, 31578, 24024, 31687, 45844, 62651, 48286, 7096, 33760, 24829, 58574, 35225, 9753, 53301, 62143, 45939, 27727, 21831, 56323, 24204, 6528, 37976, 40111, 5879, 46816, 1995, 15574, 51266, 49790, 67598, 54691, 25341, 50167, 68134, 43338, 66328, 24178, 92865, 33925, 23227, 1739846, 24977, 46644, 27711, 56050, 57273, 73199, 118, 34595, 28818, 5032, 9118, 58347, 55724, 32796, 38627, 43390, 69597, 70321, 3098573, 58388, 47534, 53421, 142828, 37030, 52139, 44803, 1736432, 213804, 29969, 2793659, 22218, 91487, 28103, 53872, 90515, 23869, 87296, 52613, 31971, 1322354, 34529, 23597, 48632, 39322, 74240, 29813, 4398, 39330, 140542, 27221, 166411, 2806867, 47896, 91191, 83548, 38963, 31696, 49294, 48409, 41807, 91775, 1672298, 41716, 1305231, 41442, 39833, 67867, 35380, 1701087]
#308



## This is PS_tester
PS_tester = [45947, 21684, 34718, 43863, 34913, 30818, 41958, 37429, 41020, 19652, 9510, 43517, 47971, 23169, 43837, 37723, 39366, 52167, 61220, 12514, 21918, 54262, 32786, 50897, 49995, 60436, 70020, 35621, 10029, 53332, 40516, 59634, 11941, 50853, 43341, 25781, 27232, 35405, 46321, 23646, 66622, 40761, 10542, 6627, 26871, 49489, 47680, 22827, 50017, 59498, 23519, 47935, 11074, 51155, 26765, 6982, 49838, 55349, 22381, 55475, 39113, 34692, 64552, 59735, 151574, 50210, 47305, 22880, 12775, 62651, 56366, 50262, 32708, 37740, 53864, 40408, 507, 33869, 60049, 24469, 23465, 71288, 58514, 49137, 90968, 61254, 53891, 59376, 54400, 25111, 68009, 91489, 6678, 24977, 24012, 67626, 23026, 47966, 4010299, 22918, 60271, 58700, 91110, 52350, 91488, 43840, 23033, 55844, 40943, 38457, 91516, 67891, 51293, 214939, 22218, 91009, 51230, 30263, 39038, 51144, 165902, 169959, 100776, 33529, 22630, 90854, 139387, 3460270, 49294, 38963, 140542, 142843, 1331483, 39342, 23531, 91191, 1701087, 39833, 48409, 41716, 1672298, 1305231, 35380, 91775]


### This is the pilot_02 Tester --- for SDSS
pilot_02 = [23340, 54234, 5344, 70175, 16636, 40622, 47346, 31037, 10496, 38392, 23069, 7262, 35088, 25640, 39114, 51286, 7806, 39308, 42544, 50782, 52307, 42530, 41779, 51253, 43707, 49497, 71926, 55647, 37591, 9549, 49820, 55665, 38748, 51706, 40284, 39925, 26690, 33964, 50676, 43330, 45795, 52641, 49347, 50317, 37525, 41811, 69270, 38031, 37624, 65131, 38492, 34561, 36607, 45848, 46127, 32763, 54018, 53217, 26390, 32778, 33635, 65022, 12772, 49359, 45684, 16144, 40607, 31059, 44086, 35675, 28148, 32648, 30895, 30714, 48749, 8232, 51901, 30322, 6826, 28351, 28010, 49236, 27681, 36930, 48332, 38851, 35224, 39040, 35991, 47985, 56094, 38916, 798, 25946, 39479, 27734, 2268, 49881, 34248, 35742, 43470, 23616, 40342, 10065, 41307, 35347, 60045, 61824, 36238, 42045, 45947, 35437, 22957, 46427, 21684, 34913, 41958, 34718, 26246, 36079, 35507, 36466, 30885, 23567, 23769, 23169, 59551, 51953, 1781, 40205, 39393, 37449, 34719, 61008, 37619, 35362, 36197, 48206, 23522, 29747, 25562, 31311, 21976, 32532, 38881, 58390, 16322, 39344, 55800, 42681, 46386, 40516, 57407, 53332, 42791, 72367, 16241, 27666, 49138, 70040, 38410, 43341, 43017, 23232, 9354, 42083, 44017, 53959, 23337, 2889, 11793, 49489, 25185, 56287, 22796, 29296, 71102, 32519, 59498, 67737, 41110, 38749, 48291, 69016, 46089, 45700, 67201, 28088, 21580, 71420, 73123, 47053, 67506, 29127, 45274, 70532, 39150, 52607, 32707, 33599, 19817, 33012, 29126, 23852, 30013, 22443, 25496, 46302, 11971, 1158, 91346, 14849, 57478, 29413, 48497, 68571, 50976, 5457, 69705, 35142, 38132, 37323, 49839, 30628, 55873, 32871, 26190, 71288, 38709, 33875, 41974, 25406, 22994, 50994, 34236, 57370, 35978, 1740300, 36316, 51725, 86944, 25521, 27544, 56195, 53014, 32443, 43077, 91731, 57338, 55, 38128, 36547, 45943, 39658, 5661, 71250, 90449, 44147, 39822, 55227, 56870, 35813, 86922, 51358, 43272, 90916, 51230, 90795, 51418, 40766, 1717815, 52280, 36976, 3996526, 64874, 43769, 90502, 169959, 2176737, 27954, 29717, 1387750, 48632, 1322354, 90854, 30862, 83548, 91191, 39342, 47896, 23531, 35803, 2806867, 42914, 49294, 38963, 34686, 41807, 67867, 39833, 35380, 1701087, 41716, 48409, 41442, 91775, 1672298, 1305231]

# Total number of objects: 308
# in common with pilot_01: 80 
# in common with Ps_tester: 28




### This is the pilot_03 Tester --- for SDSS
pilot_03 = [25248, 51932, 53043, 32774, 47346, 4540, 23069, 40622, 5344, 38392, 23340, 7806, 7262, 50973, 43397, 39308, 51286, 39114, 50782, 48959, 39328, 50042, 32251, 49820, 38748, 51955, 51253, 9549, 49497, 37591, 55647, 43707, 55665, 39925, 26690, 51706, 36875, 52641, 43330, 50676, 41061, 28700, 50587, 40284, 36607, 43147, 65131, 38492, 5268, 45848, 46127, 41811, 55588, 51587, 34917, 60459, 50216, 52266, 32321, 36431, 32207, 12772, 5688, 44961, 31302, 54095, 48749, 9272, 38897, 31059, 30714, 22506, 44086, 32648, 40607, 25910, 54267, 43345, 36930, 19743, 30322, 32767, 47788, 38851, 37290, 49236, 39152, 55057, 20458, 46563, 49881, 69650, 57799, 36029, 30531, 65506, 35991, 2268, 22446, 2232, 57284, 52564, 51846, 47422, 48392, 36932, 28714, 40801, 24490, 54428, 25237, 33446, 21684, 49464, 40566, 33333, 36493, 46427, 55281, 28617, 52247, 23769, 40530, 2479, 39390, 23169, 55097, 22277, 71883, 19274, 43939, 21847, 51450, 47495, 31145, 52167, 36660, 3667, 45549, 12514, 33188, 28324, 45322, 30569, 33401, 70020, 58305, 23512, 60330, 48207, 49234, 52092, 23362, 46180, 52190, 24567, 50087, 50853, 33408, 28197, 26495, 4561, 4148, 73176, 34675, 42319, 9376, 37614, 56287, 19627, 37308, 38964, 1932, 8556, 11793, 68110, 41050, 42938, 61970, 38815, 55078, 10331, 25145, 12531, 53317, 36441, 23753, 68552, 39150, 2607686, 36727, 5198, 67406, 51741, 50450, 35061, 50190, 52558, 21549, 23812, 58141, 58633, 59250, 90846, 56994, 51711, 47809, 22443, 50590, 70723, 58503, 27371, 53965, 8571, 26461, 507, 34459, 55200, 4520, 71345, 17095, 8163, 59783, 54123, 46556, 6636, 92910, 5220, 55518, 71508, 55739, 23707, 56097, 71890, 54440, 9738, 69284, 55923, 55161, 90833, 32248, 90949, 72325, 5032, 23385, 55, 1748393, 27113, 52965, 23341, 66882, 58347, 93847, 70100, 55530, 56655, 58989, 89610, 70594, 1426610, 86633, 142824, 54158, 42921, 51569, 1353445, 84619, 27574, 55118, 92835, 30715, 49177, 32679, 142822, 24871, 31971, 3098045, 200155, 257, 90402, 23152, 38878, 1752474, 87296, 34529, 140526, 83548, 23605, 38989, 1275824, 140542, 2816197, 72046, 1331483, 51745, 27221, 951281, 41807, 39833, 91775, 48409, 41716, 41442, 1672298, 1701087, 1305231, 67867, 35380]
# Total number of objects: 308
# in common with pilot_01: 82 
# in common with Ps_tester: 17 
# in common with pilot_02: 69

### This is the pilot_05 Tester --- for SDSS
pilot_05 = [23069, 16636, 70175, 51932, 31037, 38392, 54234, 40622, 53043, 5344, 4540, 35913, 39224, 42530, 47947, 42544, 23071, 39308, 52307, 25640, 7262, 41472, 41779, 49820, 55647, 51253, 9549, 32251, 37591, 38748, 49497, 55665, 51955, 36875, 40621, 26690, 45795, 28700, 49347, 10010, 43330, 50317, 51706, 39925, 5268, 43020, 39950, 51973, 34561, 40537, 42747, 46127, 51587, 65131, 25308, 65022, 31302, 32763, 52266, 26856, 49359, 28196, 16144, 10673, 42707, 32207, 51901, 25910, 35675, 31059, 9272, 30714, 40607, 28148, 8232, 44432, 32648, 41599, 38283, 46952, 36930, 27681, 60291, 6826, 39040, 52877, 59083, 28010, 54377, 47234, 25946, 312, 65506, 41119, 27451, 68535, 38916, 798, 57799, 26752, 41755, 60831, 51685, 52396, 2228, 54690, 47422, 38905, 26740, 31125, 24111, 36493, 39775, 38148, 34995, 23086, 29427, 21684, 35437, 37429, 26932, 48925, 40205, 6292, 9414, 21847, 24351, 1841, 49069, 40775, 51002, 50889, 48206, 32671, 49993, 34719, 57178, 31311, 33074, 35900, 36660, 34733, 42898, 48207, 25102, 60330, 41066, 32540, 29919, 55388, 37418, 68919, 39344, 42230, 15977, 42791, 36825, 70765, 26412, 66579, 27666, 23646, 28833, 12163, 58523, 26304, 34211, 69172, 47093, 28274, 52908, 61058, 55954, 10542, 4734, 37614, 7328, 22389, 13279, 2621, 34508, 52395, 10512, 28830, 43142, 46851, 57353, 49838, 41048, 50455, 28088, 70435, 42277, 73123, 2607686, 12466, 9869, 55793, 29955, 37629, 42406, 45097, 15512, 37259, 57590, 55492, 36060, 45552, 38823, 7556, 53864, 27549, 60049, 4585, 40038, 29413, 24509, 48318, 27328, 37861, 23018, 47378, 34139, 52456, 49814, 54393, 23676, 55996, 55905, 41170, 71770, 60512, 54058, 38137, 11255, 66789, 1478, 6687, 87191, 4018118, 31233, 7292, 45265, 90776, 10310, 50115, 57122, 70296, 36132, 45388, 27228, 30464, 26443, 9033, 90695, 68779, 1912053, 3098573, 142852, 43364, 4891, 40307, 69421, 56948, 50198, 4607, 32679, 165127, 39050, 24056, 1476347, 69347, 24871, 142831, 40409, 56330, 51593, 39109, 1786422, 4000181, 169959, 140526, 1763509, 27839, 39956, 58147, 34686, 1662132, 49294, 91191, 1696726, 213565, 39330, 42914, 84268, 140542, 951281, 1701087, 39833, 48409, 67867, 35380, 41442, 1305231, 41807, 41716, 91775, 1672298]
# Total number of objects: 308
# in common with pilot_01: 76 
# in common with Ps_tester: 19 
# in common with pilot_02: 81
# in common with pilot_03: 69
##########################################

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

##########################################
#################################

def fits32(filename):
  
      if '.' not in filename:
	prefix=filename
	endfix='fits'
      else:
	prefix=filename.split('.')[0]
	endfix=filename.split('.')[1]
	if endfix == '': endfix='fits'


      filename = prefix+'.'+endfix


      hdulist = pyfits.open(filename)
      prihdr = hdulist[0].header

      #bscale =  prihdr['BSCALE'] 
      #bzero =   prihdr['BZERO']
      ## don't turn it on -- for general use (python bug)
      #print "checksum1: ", np.sum(hdulist[0].data)
      print "Current BITPIX: ", prihdr['bitpix']

      if prihdr['bitpix'] != -32:
	  prihdr['bitpix'] = -32
	  
	  # take a bakcup
	  cmd = 'cp ' + filename +'  '+ filename+'.back'
	  xcmd(cmd, True)
	
	  date = subprocess.check_output(["date"])
	  date = date[0:len(date)-1]
	  prihdr['history'] = 'File modified by \'ehsan\' with \"PStesters_to_db_runsex.py\"'
	  prihdr['history'] = 'on ' + date   
	  prihdr['history'] = 'email: <ehsan@ifa.hawaii.edu>' 
	  
	  #hdulist.flush()
	  if os.path.isfile('tmp.fits'):
	    xcmd('rm tmp.fits', True)

	  hdulist.writeto('tmp.fits')
	  
	  hdulist = pyfits.open('tmp.fits', mode='update')
	  prihdr = hdulist[0].header
	  prihdr['BSCALE'] = 1.
	  prihdr['BZERO'] = 0.
	  hdulist.flush() 
	  
	  ## don't turn it on -- for general use (python bug)
	  #print "checksum2: ", np.sum(hdulist[0].data)
	  cmd = 'mv tmp.fits ' + prefix+'.'+endfix
	  xcmd(cmd, True)


#################################    
def read_file(fname, n_skip = 1, seprator = ','):
  
                # how columns are seprated
  
  list_name = []
  list_ra   = []
  list_dec  = []
  list_a    = []
  list_b    = []
  list_pa   = []
  list_ty   = []
  
  line_no = 0
  for line in open(fname, 'r+'):
    
    columns = line.split(seprator)
    
    line_no+=1
    if len(columns) >= 2:
        
        if line_no>n_skip: 
	  
	  n = 0
	  i = 0
	  while n < len(columns):
	    
	    if columns[n] != '' and i==0:
	       list_name.append(columns[n])
	       i+=1
	       n+=1
	       continue
	    
	    if columns[n] != '' and i==1:
	       list_ra.append(float(columns[n]))
	       i+=1
	       n+=1
	       continue       
	    if columns[n] != '' and i==2:
	       list_dec.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue
	    if columns[n] != '' and i==3:
	       list_a.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==4:
	       list_b.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==5:
	       list_pa.append(float(columns[n])) 
	       i+=1
	       n+=1
	       continue	     
	    if columns[n] != '' and i==6:
	       type = columns[n]
	       type = type[0:len(type)-1]
	       list_ty.append(type)
	       i+=1
	       n+=1
	       continue	     	     
	    n+=1

  
  list_name = np.asarray(list_name)
  list_ra   = np.asarray(list_ra)
  list_dec  = np.asarray(list_dec)
  list_a    = np.asarray(list_a)
  list_b    = np.asarray(list_b)
  list_pa   = np.asarray(list_pa)
  list_ty   = np.asarray(list_ty)
  
  return list_name, list_ra, list_dec, list_a, list_b, list_pa, list_ty
#################################################################

def angleto3Dradius(angle, isDegree=True):
  
  if isDegree:
    angle = angle*pi/180.
  
  
  return sqrt((sin(angle))**2 + (1-cos(angle))**2)

#################################################################
def SDSS_db_avilability(pgc, ra, dec, toDbase=False):
   
   pgc_dir = "pgc"+str(pgc)
   directory = "/home/ehsan/Dropbox/Home/PanStarrs/Jan/HI/SDSS_ALL_Images/"+pgc_dir
   isDirAvailable =  os.path.isdir(directory)
   db_dir = "/home/ehsan/db_esn/data_pilot_05/"
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
     
     
     for filters in ['u', 'g', 'r', 'i', 'z']:
        fname = directory+'/'+pgc_dir+'_'+filters+'.fits.gz'
        fname2 = '/home/ehsan/Dropbox/Home/PanStarrs/Jan/HI/SDSS+/'+pgc_dir+'_'+filters+'.fits.gz'
        if os.path.exists(fname):
	   
	   file_existence += 1
	   if toDbase:
	      command = ["cp", fname, desitination]
	      subprocess.call(command)
	      subprocess.call(['gunzip', '-f', desitination+pgc_dir+'_'+filters+'.fits.gz'])
	      fits32(desitination+pgc_dir+'_'+filters+'.fits')
	      subprocess.call(['gzip', desitination+pgc_dir+'_'+filters+'.fits'])   # zipping back
           
        elif os.path.exists(fname2):
	   file_existence += 1
	   if toDbase:
	      command = ["cp", fname2, desitination]
	      subprocess.call(command)
	      subprocess.call(['gunzip', '-f', desitination+pgc_dir+'_'+filters+'.fits.gz'])
	      fits32(desitination+pgc_dir+'_'+filters+'.fits')
	      subprocess.call(['gzip', desitination+pgc_dir+'_'+filters+'.fits'])   # zipping back
   
   
     #if toDbase and file_existence > 0:
       #cmd = "run_sex " + desitination+pgc_dir + ' ' + str(ra) + ' ' + str(dec)
       #xcmd(cmd, True)
       
   return file_existence



 
######################################
def PSRS_db_avilability(pgc, ra, dec, toDbase=False):

  db_dir = "/home/ehsan/db_esn/data_pilot_05/"


  if True:
      
    pgc_dir = "pgc"+str(pgc)
    directory = "/run/media/ehsan/ifa2_esn/my_PS_db/PS_pool/"+pgc_dir
    isDirAvailable =  os.path.isdir(directory)

    if isDirAvailable:
        
      ra_id = str(int(np.floor(ra)))
      if ra < 10:
	ra_id = '00'+ra_id+'D'
      elif ra < 100:
	ra_id = '0'+ra_id+'D'
      else:
	ra_id = ra_id+'D'
      
      desitination = db_dir + ra_id + '/panstarrs/fits/'
      file_existence = 0
      
      for filters in ['g', 'r', 'i', 'z']:
	  fname = directory+'/'+pgc_dir+'_'+filters+'.fits'
	  destin_fname = desitination+'PS_'+pgc_dir+'_'+filters+'.fits'
	  if os.path.exists(fname):
	    print fname, destin_fname
	    cmd = "cp "+fname+" "+destin_fname
	    if toDbase: xcmd(cmd, True)
	    file_existence+=1

           
     
      #if toDbase and file_existence > 0:
        #cmd = "run_sex_pstarrs " + desitination+'PS_'+pgc_dir + ' ' + str(ra) + ' ' + str(dec)
        #xcmd(cmd, True)

  return file_existence
######################################

if __name__ == '__main__':

  inFile = 'has_Hall.SDSS.csv'
  table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
  pgc     = table['pgc']
  ra      = table['ra']
  dec     = table['dec']
  sdss    = table['SDSS']
  hall    = table['Hall2012']
  
  inFile  = 'edd_HI_ba_T_9060.short.csv'
  table   = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
  d25     = table['d25']
  b_a     = table['b_a']
  PA      = table['PA']
  Ty      = table['Ty']
  
  ##############################################
  ### This is to find candidates for a-pass
  #for ind in range(len(pgc)):
    #if SDSS_db_avilability(pgc[ind], ra[ind], dec[ind]) == 5 and dec[ind]<20:
      #print ind, pgc[ind], ra[ind], dec[ind], d25[ind]
   
  #sys.exit()
  ##############################################
  
  
  
  happy = 0
  
  while not happy:
	selected_pgc = []
	selected_ind = []
	N = len(d25)
	for d_ in np.arange(3,0.2,-0.1):
	    
	    q1 = np.zeros(N)
	    q2 = np.zeros(N)
	    q1[np.where(d25<d_)] = 1
	    q2[np.where(d25>=d_-0.1)] = 1
	    q = q1 + q2
	    D_ind = np.where(q==2)
	    D_ind = D_ind[0]
	    
	    
	    m = len(D_ind)
	    p = 0
	    while p < 11:
	      
	      j = int(random.uniform(0, m))
	      ind = D_ind[j]
	      
	      if sdss[ind] == 1 and SDSS_db_avilability(pgc[ind], ra[ind], dec[ind]) == 5 and not pgc[ind] in selected_pgc:
		selected_pgc.append(pgc[ind])
		selected_ind.append(ind)
		p+=1
	    
	  
	print selected_pgc
	print len(selected_pgc)
	
	bb = 0 
	cc = 0 
	dd = 0 
	ee = 0 
	for s_pgc in selected_pgc:
            if s_pgc in pilot_01: bb+=1
            if s_pgc in pilot_02: dd+=1
            if s_pgc in pilot_03: ee+=1
            if s_pgc in PS_tester: cc+=1

	print bb, dd, ee, cc
	happy = input("Are you happy (0/1): ")

  
  for i in range(len(selected_ind)):
    ind = selected_ind[i]
    SDSS_db_avilability(pgc[ind], ra[ind], dec[ind], toDbase=True)
    #PSRS_db_avilability(pgc[ind], ra[ind], dec[ind], toDbase=True)
  

   
  print
  print
  print '# This is the glga qa file ....'
  for i in range(len(selected_ind)):
    ind = selected_ind[i]
    print 'pgc'+str(pgc[ind]), ra[ind], dec[ind], d25[ind], d25[ind]*b_a[ind], PA[ind], Ty[ind]


  ### if you have the list and you forgot to generate the glga list
  #for id in pilot_05:
      #ind = 0 
      #while pgc[ind] != id: ind+=1
      #print 'pgc'+str(pgc[ind]), ra[ind], dec[ind], d25[ind], d25[ind]*b_a[ind], PA[ind], Ty[ind]

     
  
