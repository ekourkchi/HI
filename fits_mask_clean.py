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


if '.' not in sys.argv[1]:
  prefix=sys.argv[1]
  endfix='fits'
else:
  prefix=sys.argv[1].split('.')[0]
  endfix=sys.argv[1].split('.')[1]
  if endfix == '': endfix='fits'


filename = prefix+'.'+endfix
outfile = prefix+'_clean.fits'

hdulist = pyfits.open(filename)
prihdr = hdulist[0].header


mask_file = 'pgc218_sdss_mask.fits'
hdulist_mask = pyfits.open(mask_file)
mask = hdulist_mask[0].data


data = hdulist[0].data
nx, ny =  np.shape(data)
indices = np.where(mask >0 )
data[indices] = None


if True:
    

    date = subprocess.check_output(["date"])
    date = date[0:len(date)-1]
    prihdr['history'] = 'File modified by \'ehsan\' with \"fits_mask_clean.py\"'
    prihdr['history'] = 'on ' + date   
    prihdr['history'] = 'mask file: ' + mask_file
    
    if os.path.isfile(outfile):
      xcmd('rm '+outfile, True)
    
    try: 
        hdulist.writeto(outfile)
        print outfile+' ... created ...'
    except: 
        print "Some erro happened ... no cleaning"
    
 

