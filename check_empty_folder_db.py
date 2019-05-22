#!/usr/bin/python
import sys
import os
import subprocess
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import pyfits
import glob

################################################################# 
#################################

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

#################################
if __name__ == '__main__':

  mypath = '/home/ehsan/db_esn/SDSS_GOLD/'
  folder_list = glob.glob(mypath+'pgc*')
  
  #print folder_list[0:5]
  
  for folder in folder_list:
      
      string = xcmd('ls '+folder,False)
      list = string.split('\n')
      if len(list) == 1: 
          print folder
          print list
          xcmd('rm -rf '+folder,True)
