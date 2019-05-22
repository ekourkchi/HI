pro wise_driz_bp16, name, preserve=preserve
;+
; WISE_DRIZ_BP16 - write out driz images with BITPIX = 16
;
; Usage: wise_driz_bp16,hostname [, /preserve ]
;
; PARAMS:
;	name	- host name for galaxy images.  Looks in 
;		  !GLGA_WISE_DATA+'data/sort/'+name for images.
;
; KEYWORDS:
;	preserve	- set to keep original file in <filename>+'_orig',
;			  else original file is deleted.
;
; HISTORY:
;	13jun2012	- jdn, initial version
;
;-
; loop over names list
for j=0,n_elements(name)-1 do begin
	;
	; look in glga wise data directory for each host
	ddir = !GLGA_WISE_DATA+'data/sort/'+name[j] + '/'
	;
	; get list of files in driz directories
	flist = file_search(ddir+'driz?/'+name[j]+'*_unc.fits',count=nf)
	;
	; got files?
	if nf gt 0 then begin
		;
		; loop over files
		for i=0,nf-1 do begin
			file = flist[i]	; this file
			;
			; only gzip mask files (already BITPIX=8)
			if strpos(file,'_msk') ge 0 then begin
			    ;
			    ; only gzip if needed
			    if strpos(file,'.gz') lt 0 then $
				spawn,'gzip '+file
			;
			; not a (BP=8) mask file
			endif else begin
			    print, "Ehsan  ... "+file
			    hdr = headfits(file)
			    bp = sxpar(hdr,'BITPIX')
			    ;
			    ; BITPIX = 16 already
			    if bp eq 16 then begin
				; only gzip if needed
				if strpos(file,'.gz') lt 0 then $
					spawn,'gzip '+file
			    ;
			    ; not BITPIX = 16, so read in and re-scale
			    endif else begin
			    	

			    	data = mrdfits(file,0,hdr,/fscale,/silent)
			    	;
			    				    	
			    	; keep if requested, else remove
			    	if keyword_set(preserve) then $
				    	spawn,'mv '+file+' '+file+'_orig' $
			    	else    spawn,'rm '+file
		    	    	; rescale to BITPIX = 16 and compress
		    	    	
		    	    	
		    	    	
		    	    	do_it = (1 eq 1)
		    	    	if strpos(file,'_unc') ge 0 then begin
		    	    	    

		    	    	    data[where(finite(data, /nan))] = 200
		    	    	    data[where(data gt 200, n_clip)] = 200
		    	    	    
                                    med = median(data)
                                    mea = mean(data)
                                    data_clip = data[where(data gt 0, n_clip)]
                                    
                                    while abs(mea-med)/med gt 2 do begin
                                        data_clip = data_clip[where(data_clip lt stdev(data_clip), n_clip)]
                                        med = median(data_clip)
                                        mea = mean(data_clip)
                                    endwhile
                                    
                                    if n_clip gt 1 then begin
                                        maximum = median(data_clip)+10*stdev(data_clip)
                                        data[where(data gt maximum)] = maximum
                                    endif else do_it = (1 eq 0)
		    	    	
		    	    	endif
		    	    	
		    	    	
			    	if do_it then mymwrfits,data,file,hdr, $
					/create,/compress,/iscale
			    endelse
			endelse
		endfor	; loop over files
	; no files
	endif else print,'No files found: '+ddir+'driz?/'+name[j]+'*_unc.fits'
endfor	; loop over names list
;
return
end
