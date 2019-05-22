#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 

#################
# it gets two sets of pgc cataloges and remove the second catalog from the first
# this functions returns the indices of the first catalog that are NOT removed.



# J2000
# example: 004244.4+411608.0
ra_dec = sys.argv[1]
print ra_dec[0:8], ra_dec[8:17]

ra_h = ra_dec[0:2]
ra_m = ra_dec[2:4]
ra_s = ra_dec[4:8]
print ra_h+":"+ra_m+":"+ra_s
ra_deg = 15.*(float(ra_h)+float(ra_m)/60.+float(ra_s)/3600.)


dec_d = ra_dec[8:11]
dec_m = ra_dec[11:13]
dec_s = ra_dec[13:17]
print dec_d+":"+dec_m+":"+dec_s
s = np.sign(float(dec_d))
dec_deg = s*(np.abs(float(dec_d))+float(dec_m)/60.+float(dec_s)/3600.)

print ra_deg, dec_deg