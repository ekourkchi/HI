#!/bin/sh

export ra=$1
export dec=$2
export srv=\'$3\'
export outFits=\'$4\'
export imsize=$5

# echo QueryDSS, [$ra, $dec], survey=$srv, out=$outFits, ImSize=$imsize

idl << EOF > logidl.out
 QueryDSS, [$ra, $dec], survey=$srv, out=$outFits, ImSize=$imsize
EOF
