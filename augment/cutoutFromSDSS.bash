#!/bin/bash

export ra=$1
export dec=$2
export size=$3
export angle=$4

export dsize=`echo  '2*'${size} | bc`

export angle=`echo  '-1*'${angle} | bc`
export root_dir=$5

echo "http://skyserver.sdss.org/dr12/SkyserverWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra=$ra&dec=$dec&scale=0.25&width=$dsize&height=$dsize"

wget -c "http://skyserver.sdss.org/dr12/SkyserverWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra=$ra&dec=$dec&scale=0.25&width=$dsize&height=$dsize" -P $root_dir



mv $root_dir/getjpeg\?TaskName\=Skyserver.Explore.Image\&ra\=$ra\&dec\=$dec\&scale\=0.25\&width\=$dsize\&height\=$dsize $root_dir/test.jpg

mogrify -rotate $angle $root_dir/test.jpg 
export eq=`convert $root_dir/test.jpg -format "%w x %h" info:`
export w=`echo $eq | awk '{print($1)}'` 
export h=`echo $eq | awk '{print($1)}'` 

# export x0=`calc $w/2-$size/2`
export x0=`echo  ${w}'/2-'${size}'/2' | bc`
# export y0=`calc $h/2-$size/2`
export y0=`echo  ${h}'/2-'${size}'/2' | bc`

echo $x0 $y0

convert $root_dir/test.jpg -crop ${size}x${size}+$x0+$y0  $root_dir/test.jpg

