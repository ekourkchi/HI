;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
function radir, ra

   if ra lt 10 then directory='00'+strtrim(string(floor(ra)),2)+'D'
   if ra ge 10 and ra lt 100 then directory='0'+strtrim(string(floor(ra)),2)+'D'
   if ra ge 100 then directory=strtrim(string(floor(ra)),2)+'D'
    


return, directory
end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Function separation, ra, dec
    
   ;; North ecliptic pole: RA=270, Dec= 66.56071
   ang1 = sqrt((ra-270)^2+(dec-66.56071)^2)

   ;; South ecliptic pole: RA=90, Dec= -66.56071
   ang2 = sqrt((ra-90)^2+(dec+66.56071)^2)
   
   return, min([ang1,ang2])

end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


pro wise_driz_proc,lfile,update=update,clean=clean,nobp16=nobp16, $
	shrink=shrink, limit=limit, todatabase=todatabase, fromobj=fromobj, bmeth=bmeth
;+
; wise_driz_proc - process WISE images with drizzling using ICORE
;
; lfile - galaxy list with one entry per galaxy with the following columns:
;	id
;	ra,dec	- decimal degrees
;	majdiam,mindiam	- arcminutes
;	pa	- position angle in degrees
;	type	- galaxy Hubble type (string)
;
; KEYWORDS:
;	UPDATE	- set to update previous run, otherwise will not re-process
;	CLEAN	- set to remove intermediate files (recommended)
;	NPBP16	- set to prevent FITS scaling into 16 bit integers
;	SHRINK	- set to limit image size by adjusting pixel scale
;	LIMIT   - set to number limit per band of images retrieved (def: 200)
;	BMETH	- value for background method: 0, 1, or 2
;			defaults to 2 (see ICORE docs)
;
; Version Info: $Id: wise_driz_proc.pro,v 1.10 2015/03/01 02:20:20 neill Exp $
;-
; read input
readcol,lfile,id,sra,sdec,majdiam,mindiam,pa,format='a,d,d,f,f,f'
nobj = n_elements(sra)
name = strtrim(id,2)
;
; check size limit
;
; 3 arcmin is minimum size
r=((majdiam*6.0)>3.) / 60.
sz = (majdiam * 6.0)>3.
bg = where(majdiam ge 50., nbg)
if nbg gt 0 then sz[bg] = majdiam[bg] * 1.5
bg = where(majdiam lt 50. and majdiam ge 30., nbg)
if nbg gt 0 then sz[bg] = majdiam[bg] * 2.0
bg = where(majdiam lt 30 and majdiam ge 20., nbg)
if nbg gt 0 then sz[bg] = majdiam[bg] * 2.5
bg = where(majdiam lt 20 and majdiam ge 10., nbg)
if nbg gt 0 then sz[bg] = majdiam[bg] * 3.0
;
; list of spectral bands
band=['w1','w2','w3']
nband = n_elements(band)
;
; nframes
if keyword_set(limit) then begin
	if limit gt 1 then begin
		lstr = strtrim(strn(limit),2)
		nframes = lstr+','+lstr+','+lstr
	endif else $
		nframes = '200,200,200'
endif else	nframes = 'all,all,all'




;
; check bmeth
if keyword_set(bmeth) then begin
	if bmeth lt 0 or bmeth gt 2 then begin
		print,'Illegal bmeth value, returning: ', bmeth
		return
	endif
endif else bmeth = 2


;
; pixel size
psc = 1.0
;
; directories
root = !GLGA_WISE_DATA + 'data/sort/'
;

ig_start=0L
if keyword_set(fromobj) then begin
    for ig=0L,nobj-1L do begin
          if strcmp(fromobj,name[ig]) then begin
               ig_start = ig+0L
               break
          endif
    endfor
endif




; loop over objects
for ig=ig_start,nobj-1L do begin
    ; check for existing directory
    if file_test(root+name[ig]) ne 0 then begin
	cmd = 'mv '+root+name[ig]+' '+root+name[ig]+'_old'
	spawn,cmd
    endif
    ; get the frames
    
   
    if not keyword_set(limit) and majdiam[ig] gt 7 then nframes = '40,40,40'
    if not keyword_set(limit) and majdiam[ig] le 7 then nframes = '200,200,200'
    
    angle = separation(sra[ig], sdec[ig])
    
    if not keyword_set(limit) and majdiam[ig] le 7 and majdiam[ig] gt 4 and angle gt 10 then nframes = 'all,all,all'
   
;     print, angle, nframes, majdiam[ig]
;     stop
   
    cmd = 'perl /Users/ehsan/Downloads/getWise/getframesAllSky -ra ' + $
	strtrim(string(sra[ig],form='(f13.6)'),2) + ' -dec ' + $
	strtrim(string(sdec[ig],form='(f13.6)'),2) + ' -sx ' + $
	strtrim(string(r[ig],form='(f9.3)'),2) + ' -sy ' + $
	strtrim(string(r[ig],form='(f9.3)'),2) + ' -outd ' + root+name[ig] + $
	' -bands 1,2,3 -num '+nframes+' -moo 25 -ant 2000 -log ' + $
	name[ig] + '_fetch.log'
    
    print, cmd
    
    spawn,cmd
    ;
    ; current coordinates
    ra=sra[ig]
    dec=sdec[ig]
    ;
    ; current directory
    dir=root+name[ig]+'/'
    ;
    ; does directory exist?
    if file_test(dir,/directory) then begin
      ;
      ; Do only if not processed already or requesting update
      if not file_test(dir+'driz1/'+name[ig]+'_w1.fit*') or $
	 keyword_set(update) then begin
	;
	; go to directory
	cd,dir,curr=cwd
	;
	; are there any files here?
	if file_test('*-int-1b.fit*') then begin
		;
		; get to work and print our status
		print,ig+1,'/',nobj,name[ig],form='(i5,a1,i5,2x,a)'
		;
		; are we updating?
		if keyword_set(update) then begin
			spawn,'rm -rf icore_?.log driz?'
		endif
		;
		; get maximum image size based on image collection
		imsize = max(mosaic_max_imsize('./','*-int-1b.fit*',/verbose))
		;
		; size cannot exceed capacity of images
		size = min([sz[ig]*60.,imsize])	; size in arcseconds
		;
		; test if not resizing
        	if not keyword_set(shrink) then begin
	    		pxsiz = size / psc
	    		if pxsiz gt 3600 then $
		    	    print,'Warning - image will have dimensions: ', $
			    	pxsiz,' by ', pxsiz
			shfact = 1.0
		;
		; calculate shrink factor
        	endif else begin
			; automatic shrink calculation
			if shrink le 1. then begin
				shfact = 1.0
				pxsiz = size / psc
				; shrink until under maximum size
				while pxsiz gt 3600 do begin
					shfact = shfact + 1.0
					pxsiz = size / ( psc * shfact )
				endwhile
			; or use keyword shrink factor
			endif else begin
				shfact = shrink
			endelse
		endelse
		if shfact ne 1. then $
			print,'Shrink factor = ',shfact,form='(a,f7.2)'
		
		; loop over bands
		for iband=0,nband-1 do begin
			print,'Processing ',band[iband],' data...'
			cmd = 'icore_driz_wise ' + name[ig] + ' ' + $
				string(ra,format='(f13.8)') + ' ' + $
				string(dec,format='(f13.8)') + ' ' + $
				string(size/3600.,format='(f8.5)') + ' ' + $
				strn(iband+1) + ' ' + strn(psc*shfact) + $
                                ' ' + strn(bmeth) + ' | tee icore_' + $
                                strn(iband+1) + '.log'
			print,cmd
; 			exit
                        spawn,'gunzip *fits.gz'
			spawn,cmd
			print,'Done processing ',name[ig],': ',band[iband], $
				' data.'
		endfor	; loop over bands
		if not keyword_set(nobp16) then wise_driz_bp16,name[ig], /preserve

		
		if keyword_set(clean) then begin
			print,'Cleaning up...'
			spawn,'rm driz?/*-1b.fits'
			spawn,'gzip driz?/*.fits'
			spawn,'rm *-1b.fits'
			print,'Done cleaning up.'
		endif
		
		if keyword_set(todatabase) then begin
                        
                        radirect = !GLGA_WISE_DATA + 'data/'+radir(ra)+'/wise/fits/'
                        spawn,'gzip driz?/*.fits'
                        spawn,'cp driz?/*.fits.gz '+radirect
                        spawn,'rm '+radirect+'*_cov.fits.gz '
                        spawn,'rm '+radirect+'*_msk.fits.gz '
                        spawn,'rm '+radirect+'*_std.fits.gz '
                        spawn,'rm -rf '+root+name[ig]
                        
		endif
		
		
		
	endif
	cd,cwd
	spawn,'rm ' + name[ig] + '_fetch.log'
	spawn,'rm query.tbl'
      endif else print,dir+name[ig]+' already processed.'
    endif else print,'No directory for host: ',name[ig]
endfor	; loop over hosts
;
return
end








