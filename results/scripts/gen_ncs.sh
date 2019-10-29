#!/bin/bash

image_path="/home/pi/ba_schraven/datasets/obj_detection_frames"
result_path="/home/pi/ba_schraven/results/ncs/obj_detection"
WD="/home/pi/ba_schraven/YoloV2NCS"
cmd="python3 ./detectionExample/Main.py --image"

find $image_path -name '*.jpg' | while read line; do
	file_name=$(basename $line);
	result_file=$(echo $file_name | sed 's/.jpg/.txt/g');
	result=$result_path"/"$result_file;
	
	cd $WD;
	echo $(pwd);

	echo $result_file;
	$cmd $line | grep 'total time is' | cut -d' ' -f6 >> /home/pi/ncs_latency.txt;
	cp -v $WD/result.jpg $result_path/$file_name;
	cp -v $WD/result.txt $result;
done;
