#!/usr/bin/python
import sys
import os
import subprocess
import math
import numpy as np



inFile = 'wise_all.csv'
table = np.genfromtxt( inFile , delimiter=',', filling_values=None, names=True, dtype=None)
wise_name = table['ID']
wise_pgc  = table['PGC']


###############################
if (len(sys.argv) < 2):
    print "\n Not enough input arguments ..."
    print >> sys.stderr, " Use \"python "+sys.argv[0]+" <RA.deg> <DEC.deg>\" \n"
    print
    print " Ehsan Kourkchi June, 20, 2017"
    print
    exit(1)   


pgc = int(sys.argv[1])
found = False
for j in range(len(wise_pgc)):
    
    if wise_pgc[j]==pgc: 
        print wise_name[j]
        found = True
        break

    

if not found:
   print 'pgc'+str(pgc)




