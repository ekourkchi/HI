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
def removefix(filename):
  
  
  name_list = filename.split('.')
  N = len(name_list)
  if name_list[N-1] == 'fits':
    
    name =''
    for i in range(N-2):
      name = name + name_list[i] + '.'
    name += name_list[N-2]

  return name
#################################


def fits_prep(filename, bitpix, edit_zp=False):
	
      hdulist = pyfits.open(filename)
      prihdr = hdulist[1].header
      
      
      name = removefix(filename)
      
      mask_name = name+'.mk.fits'
      hasMask = False
      if os.path.isfile(mask_name):
	  h = pyfits.open(mask_name)
	  mask = h[1].data
	  hasMask = True


      


      if True:
	  prihdr['bitpix'] = bitpix
	  

	
	  date = subprocess.check_output(["date"])
	  date = date[0:len(date)-1]
	  prihdr['history'] = 'File modified by \'ehsan\' with \"fits_prep.py\"'
	  prihdr['history'] = 'on ' + date   
	  prihdr['history'] = 'email: <ehsan@ifa.hawaii.edu>' 
	  
	  if os.path.isfile(name+'.tmp.fits'):
	    xcmd('rm tmp.fits', True)

	  prihdu = pyfits.PrimaryHDU(hdulist[1].data, header=prihdr)
	  prihdu.writeto(name+'.tmp.fits')
	  
	  
	  if edit_zp:
		hdulist = pyfits.open(name+'.tmp.fits', mode='update')
		prihdr = hdulist[0].header
		prihdr['BSCALE'] = 1.
		prihdr['BZERO'] = 0.
		
		expTime = float(prihdr['EXPTIME'])
		zeroPoint = float(prihdr['HIERARCH FPA.ZP'])
		new_zp = 16.40006562  # mJy / pix
		alpha = 10**(-0.4*(zeroPoint-new_zp))
		hdulist[0].data = data = hdulist[0].data * (alpha / expTime)
		
		prihdr['EXPTIME'] = 1.0
		prihdr['HIERARCH FPA.ZP'] = new_zp
		
		if hasMask:
                   ind = np.where(mask>0)
                   hdulist[0].data[ind] = None
    
		
		hdulist.flush() 
	  
	  ## don't turn it on -- for general use (python bug)
	  #print "checksum2: ", np.sum(hdulist[0].data)
	  cmd = 'mv '+name+'.tmp.fits ' + filename
	  xcmd(cmd, True)


