#!/bin/bash

image_path="/home/lurps/ba_schraven/datasets/obj_detection_frames"
result_path="/home/lurps/ba_schraven/results/cloud/obj_detection"
cmd="python /home/lurps/catkin_ws/src/obj_detection/cloud_vision.py"

find $image_path -name *.jpg | while read line; do
	file_name=$(basename $line);
	result_file=$(echo $file_name | sed 's/.jpg/.txt/g');
	result=$result_path"/"$result_file;
	
	echo $result_file;
	$cmd $line > $result;
done;
