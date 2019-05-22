#!/usr/bin/python
import sys
import os
import subprocess
import math
import glob



#################################################################

if __name__ == '__main__':
  
  for filename in glob.glob('html_make/*make*py'):
    
    print "making " + filename + "  ... "
    subprocess.check_output(["python" , filename])
