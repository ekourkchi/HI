import sys
#import numpy as np

##########################################
# Reading the input file
# Assumes the first column as date with yyyy-mm-dd format
# 2nd column is hour (0-24)
# 3rd column is the dsired value, e.g. seeing
def read_file(fname, n_skip = 0):
  
  seprator = ','               # how columns are seprated
  

  pgc      = []
  objname  = []
  objtype  = []
  al2000   = []
  de2000   = []
  l2       = []
  b2       = []
  sgl      = []
  sgb      = []
  type     = []
  logd25   = []
  e_logd25 = []
  
  
  
  line_no = 0
  for line in open(fname, 'r'):
    columns = line.split(seprator)
    line_no+=1
    if len(columns) ==12:
        
        if line_no>n_skip: 
          pgc.append(columns[0])
          objname.append(columns[9])
          objtype.append(columns[10])
          al2000.append(columns[1])
          de2000.append(columns[2])
          l2.append(columns[3])
          b2.append(columns[4])
          sgl.append(columns[5])
          sgb.append(columns[6])
          type.append(columns[11])
          logd25.append(columns[7])
          e_logd25.append(columns[8])

  

  return pgc, objname, objtype, al2000, de2000, l2, b2, sgl, sgb, type, logd25, e_logd25

##########################################

################################
#if (len(sys.argv) < 1):
    #print "\n Not enough input arguments ..."
    #print >> sys.stderr, " Use \"python "+sys.argv[0]+" <pgc> \" \n"
    #print
    #print " Ehsan Kourkchi June, 13, 2017"
    #print
    #exit(1) 


pgc, objname, objtype, al2000, de2000, l2, b2, sgl, sgb, type, logd25, e_logd25 = read_file('/netdisks/users/ehsan/python/kleda_orig.csv' , n_skip = 1)


found = False
for i in range(len(pgc)):
    
     if pgc[i] == sys.argv[1]:

        s= ''
        s = s+pgc[i]+' '
        s = s+objname[i]+' '
        s = s+ objtype[i]+ ' '
        s = s+ al2000[i]+ ' '
        s = s+ de2000[i]+ ' '
        s = s+ l2[i]+ ' '
        s = s+ b2[i]+ ' '
        s = s+ sgl[i]+ ' '
        s = s+ sgb[i]+ ' '
        s = s+ type[i]+ ' '
        s = s+ logd25[i]+ ' '
        s = s+ e_logd25[i]
    
        print s

        
        found = True
        break



