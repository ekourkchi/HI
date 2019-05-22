#!/bin/sh



export db_dir=$1

export d25=$3
export angle=$4
export pgc=$2

export pixscl=0.25
export ratio=3    # how many times bigger than d25
export size=`echo "$ratio * $d25 * 60 / $pixscl" | bc -l`
export size=`printf '%.*f\n' 0 $size`



for filter in 'g' 'r' 'i'
 do
 
 export fitsfile=${db_dir}/${pgc}_d25x2_rot_${filter}.fits
 export pngfile=${db_dir}/DSS_PNG_rotate_finale/${pgc}_d25x2_rot_${filter}.png
 
 echo $fitsfile
 echo $pngfile
 
 ##################################################
 ds9 -invert -zoom to fit -log -cmap value 3.9 0.852 -colorbar no $fitsfile  &
 sleep 5
 set myVar=`xpaget ds9 scale limits`
 set sc_low=`echo $myVar | awk '{print($1)}'`
 set sc_high=`echo $myVar | awk '{print($2)}'`
 xpaset -p ds9 scale limits 0 25555
 


 xpaset -p ds9 export png $pngfile
 xpaset -p ds9  exit 
 sleep 5
##################################################
 done  



 
cp ${db_dir}/DSS_PNG_rotate_finale/${pgc}_d25x2_rot_r.png ${db_dir}/DSS_PNG_rotate_finale/${pgc}_d25x2_rot_gri.jpg


 








