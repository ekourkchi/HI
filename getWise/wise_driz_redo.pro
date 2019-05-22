pro wise_driz_redo, lfile, inband, clean=clean, shrink=shrink, nobp16=nobp16, $
	bmeth=bmeth
;+
; wise_driz_redo - re-process failed WISE images with drizzling using ICORE
;
; lfile - galaxy list with one entry per galaxy with the following columns:
;	id
;	ra,dec	- decimal degrees
;	majdiam,mindiam	- arcminutes
;	pa	- position angle in degrees
;	type	- galaxy Hubble type (string)
;
; inband - the band number to redo: 1,2,3, or 4
;
; KEYWORDS:
;	CLEAN	- set to remove intermediate files (recommended)
;	SHRINK	- set to limit image size by adjusting pixel scale
;	NPBP16	- set to prevent FITS scaling into 16 bit integers
;	BMETH	- value for background method: 0, 1, or 2
;			defaults to 2 (see ICORE docs)
;
; Version Info: $Id$
;-

;
; get list
readcol,lfile,names,sra,sdec,majdiam,form='a,d,d,f',com='#'
;
; 3 arcmin is minimum size
sz = (majdiam * 4.0)>3.
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
band=['w1','w2','w3','w4']
nband = n_elements(band)
;
; check band
if inband lt 1 or inband gt 4 then begin
	print,'Illegal redo value, returning: ', inband
	return
endif
sband = strtrim(strn(inband),2)
iband = inband - 1
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
; loop over hosts
ng=n_elements(names)
for ig=0,ng-1 do begin
	;
	; current coordinates
	ra=sra[ig]
	dec=sdec[ig]
	;
	; current directory
	dir=root+names[ig]+'/'
	;
	; go to directory
	cd,dir,curr=cwd
	;
	; gunzip if we've done this before
	spawn,'gunzip *-w'+sband+'-???-1b.*gz'
	;
	; get to work and print our status
	print,ig+1,'/',ng,names[ig],form='(i5,a1,i5,2x,a)'
	;
	; move originals
	spawn,'mv driz'+sband+' driz'+sband+'_orig'
	spawn,'mv icore_'+sband+'.log icore_'+sband+'.log_orig'
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
	;
	; process band
	print,'Processing ',band[iband],' data...'
	cmd = 'icore_driz_wise ' + names[ig] + ' ' + $
		string(ra,format='(f13.8)') + ' ' + $
		string(dec,format='(f13.8)') + ' ' + $
		string(size/3600.,format='(f8.5)') + ' ' + $
		strn(iband+1) + ' ' + strn(psc*shfact) + $
		' ' + strn(bmeth) + ' | tee icore_' + $
		strn(iband+1) + '.log'
	print,cmd
	spawn,cmd
	print,'Done processing ',names[ig],': ',band[iband], ' data.'
	if not keyword_set(nobp16) then $
		wise_driz_bp16,names[ig] $
	else	spawn,'gzip driz'+sband+'/'+names[ig]+'_*.fits'
	if keyword_set(clean) then begin
		print,'Cleaning up...'
		spawn,'rm driz'+sband+'/*.fits'
		print,'Done cleaning up.'
	endif
	spawn,'gzip *-1b.fits &'
	cd,cwd
endfor	; loop over hosts
;
return
end
