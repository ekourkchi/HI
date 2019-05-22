function mosaic_max_imsize, dir, fspec, verbose=verbose
;+
;	mosaic_max_imsize - determine maximum image size based on
;		collection of images in dir
;
;-
; list of files to check
if n_params(0) lt 2 then begin
	fsp = ''
	read,'File spec for images: ',fsp
endif else fsp = fspec
;
; get list of images
flist = file_search(dir+'/'+fsp,count=nf)
;
; default if no files found
mis = [-1., -1.]
;
; found images
if nf gt 0 then begin
	;
	; collect ras and decs
	ras = [-1.]
	dcs = [-999.]
	;
	; loop over each image
	for i=0,nf-1 do begin
		;
		; extract atrometry from hdr
		print, "Ehsan  ... "+flist[i]
		hdr=headfits(flist[i])
		
		extast,hdr,astr
		;
		; get image dimensions
		nx = sxpar(hdr,'NAXIS1')
		ny = sxpar(hdr,'NAXIS2')
		;
		; convert corners of each image to ra,dec
		xs = [0., 0., nx, nx]
		ys = [0., ny, ny, 0.]
		xy2ad, xs, ys, astr, a, d
		;
		; collect into arrays
		ras = [ras, a]
		dcs = [dcs, d]
	endfor
	;
	; trim
	ras = ras[1:*]
	dcs = dcs[1:*]
	;
	; compute average
	ims,ras,rav,rsg,rwt
	ims,dcs,dav,dsg,dwt
	;
	; avoid un-weighted points (bad)
	good = where(rwt gt 0 and dwt gt 0, ngood)
	;
	; get extrema
	rmx = max(ras[good])
	rmn = min(ras[good])
	dmx = max(dcs[good])
	dmn = min(dcs[good])
	;
	; get ra diff at average dec
	gcirc,2,rmn,dav,rmx,dav,xsz
	;
	; get dec diff at average ra
	gcirc,2,rav,dmn,rav,dmx,ysz
	;
	; print results if requested
	if keyword_set(verbose) then begin
		print,'Coords (ra,dec:degrees)'
		print,'Avg: ',rav,dav
		print,'Max: ',rmx,dmx
		print,'Min: ',rmn,dmn
		print,'Sizes (arcsecs)'
		print,'Xsz: ',xsz
		print,'Ysz: ',ysz
	endif
	;
	; pack for return
	mis = [xsz,ysz]
endif else print,'No files found for file spec: ',fsp
return,mis
end
