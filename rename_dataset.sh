#!/bin/bash
dirs=$(ls -1 $1)

for dir in $dirs; do
	if [ -d "$dir" ]; then
	    rename -v .jpg _$dir.jpg $dir/*.jpg
	fi
done
