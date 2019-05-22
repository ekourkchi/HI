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

    
#######
def read_glga(filename):
  
  pgc_lst = []
  seprator = ' ' 
  for org_line in open(filename, 'r'):
    columns = org_line.split(seprator)
    pgc = columns[0]
    pgc_ID = pgc[3:len(pgc)]
    pgc_lst.append(int(pgc_ID))
  
  return pgc_lst    
    
#######

 
if __name__ == '__main__':
    
  print read_glga('data_set_41.glga')
  


  
  






     
  
