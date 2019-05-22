#!/bin/sh



export db_dir=$1

export d25=$3
export angle=$4

export pixscl=0.25
export ratio=3    # how many times bigger than d25
export size=`echo "$ratio * $d25 * 60 / $pixscl" | bc -l`
export size=`printf '%.*f\n' 0 $size`



for filter in 'g' 'r' 'i'
 do
 
 export fitsfile=$db_dir/$2_d25x2_rot_$filter.fits
 export pngfile=$db_dir/SDSS_PNG_rotate_finale/$2_d25x2_rot_$filter.png
 
 echo $fitsfile
 echo $pngfile
 
 #################################################
 ds9 -invert -zoom to fit -log -cmap value 1.7 0.6 -colorbar no $fitsfile  &
 sleep 4
 export tmp='xpaget ds9 scale limits'
 export sc_low=`echo $tmp | awk '{print($1)}'`
 export sc_high=`echo $tmp | awk '{print($2)}'`
 xpaset -p ds9 scale limits -0.0001 0.01
 sleep 2
# Rotation happens in the Python code
#  xpaset -p ds9 rotate $angle 
#  xpaset -p ds9 height $size
#  xpaset -p ds9 width $size

 echo 'xpaset -p ds9 export png '$pngfile
 xpaset -p ds9 export png $pngfile
  sleep 2
 xpaset -p ds9  exit 
 sleep 10
#################################################
 done  


# rm $fitsfile
export pgc=\'$2\'
export suffix=\'d25x2_rot\'
export outdir=\'$db_dir/SDSS_PNG_rotate_finale/\'
export root_dir=\'$db_dir\'


export pgc_=$2
export suffix_=d25x2_rot
export outdir_=$db_dir/SDSS_PNG_rotate_finale/
export root_dir_=$db_dir


idl << EOF > logidl.out

 rgb_ps_asinh, /update, pgc=$pgc, suffix=$suffix, nonlinearity=1.2, quality=100, brite=1.2, outdir=$outdir, root_dir=$root_dir
 
 rgb_ps_asinh, /update, pgc=$pgc, suffix=$suffix, nonlinearity=1.2, quality=100, brite=1.2, outdir=$outdir, root_dir=$root_dir, /gonly 
 
 rgb_ps_asinh, /update, pgc=$pgc, suffix=$suffix, nonlinearity=1.2, quality=100, brite=1.2, outdir=$outdir, root_dir=$root_dir, /ronly 
 
 rgb_ps_asinh, /update, pgc=$pgc, suffix=$suffix, nonlinearity=1.2, quality=100, brite=1.2, outdir=$outdir, root_dir=$root_dir, /ionly 
 
EOF

convert -negate ${outdir_}${pgc_}_${suffix_}_g.back.jpg ${outdir_}${pgc_}_${suffix_}_g.back.png
convert -negate ${outdir_}${pgc_}_${suffix_}_r.back.jpg ${outdir_}${pgc_}_${suffix_}_r.back.png
convert -negate ${outdir_}${pgc_}_${suffix_}_i.back.jpg ${outdir_}${pgc_}_${suffix_}_i.back.png

rm ${outdir_}${pgc_}_${suffix_}_g.back.jpg
rm ${outdir_}${pgc_}_${suffix_}_r.back.jpg
rm ${outdir_}${pgc_}_${suffix_}_i.back.jpg

### NOTE: run this in csh









