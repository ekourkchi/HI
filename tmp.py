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



######################################
def make_sdss(pgc, ra, dec, size, band):
    
    pgc_band_root ='.'

    
###########################################################################
    with cd(pgc_band_root):
      fout=open('montage.csh','w')
      montage = '''
      rm *tbl
      rm -rf projected
      mkdir  projected
      mImgtbl tmp rimages.tbl
      mProjExec -p tmp rimages.tbl tmp.hdr projected stats.tbl
      mImgtbl projected pimages.tbl
      mAdd -p projected pimages.tbl tmp.hdr tmp.fits
      mConvert -b -32 tmp.fits tmp.fits
      rm *area*fits
      rm *tbl
      rm -rf projected
      '''
      fout.write(montage+'\n')
      fout.close()
      
      if size > 1.1:
          size = 1.1
      
      naxis = int(size*3600 / 0.396)
      crpix = naxis/2
      hdr = ''
      hdr += 'SIMPLE = T' + '\n'
      hdr += 'BITPIX = -32' + '\n'
      hdr += 'NAXIS = 2' + '\n'
      hdr += 'NAXIS1 = '+str(naxis) + '\n'
      hdr += 'NAXIS2 = '+str(naxis) + '\n'
      hdr += 'CTYPE1 = \'RA---TAN\'' + '\n'
      hdr += 'CTYPE2 = \'DEC--TAN\'' + '\n'
      hdr += 'CRVAL1 = ' +str(ra)+ '\n'
      hdr += 'CRVAL2 = ' +str(dec)+ '\n'
      hdr += 'CRPIX1 = '+str(crpix) + '\n'
      hdr += 'CRPIX2 = '+str(crpix) + '\n'
      hdr += 'CDELT1 = -1.1E-04' + '\n'
      hdr += 'CDELT2 = 1.1E-04' + '\n'
      hdr += 'CROTA2 = 0.000000' + '\n'
      hdr += 'EQUINOX = 2000.0' + '\n'
      hdr += 'BSCALE = 1' + '\n'
      hdr += 'BZERO = 0' + '\n'
      hdr += 'EXPTIME = 1.0' + '\n'
      hdr += 'ZP = 16.40006562 ' + '\n'
      hdr += 'OBJECT = ' + 'pgc'+str(pgc) + '\n'
      hdr += 'HISTORY = \'email: <ehsan@ifa.hawaii.edu>\'' + '\n'  
      hdr += 'HISTORY = \'by: esnsdssget.py\'' + '\n'  
      hdr += 'END' + '\n'

      fout=open('tmp.hdr','w')
      fout.write(hdr)
      fout.close()
      
      xcmd('csh montage.csh', True)
      xcmd('mv tmp.fits '+'pgc'+str(pgc)+'_'+band+'.fits', True)
      xcmd('rm montage.csh', True)
      xcmd('rm tmp.hdr', True)
      xcmd('rm -rf tmp', True)
      
###########################################################################
