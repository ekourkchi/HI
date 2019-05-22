import pyfits
import os,sys,math
import subprocess
import numpy as np
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





filename = sys.argv[1]


hdulist = pyfits.open(filename)


data = hdulist[0].data
nx, ny =  np.shape(data)
indices = np.where(data == 0 )
data[indices] = None


if True:
    


    
    if os.path.isfile(filename):
      xcmd('rm '+filename, True)
    
    try: 
        hdulist.writeto(filename)
        print outfile+' ... created ...'
    except: 
        print "Some erro happened ... no cleaning"
    
 

