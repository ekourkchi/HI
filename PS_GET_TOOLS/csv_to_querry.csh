#!/usr/bin/csh

# example: 
## csh csv_to_querry.csh all.9060.csv  1001 1500


setenv filename $argv[1]
setenv row_min  $argv[2]
setenv row_max  $argv[3]

# row_min  row_max
python make_panstarrs_main.py $filename catal > $filename'.'$row_min'_'$row_max'.catal'  $row_min $row_max
python make_panstarrs_main.py $filename query > $filename'.'$row_min'_'$row_max'.query'  $row_min $row_max