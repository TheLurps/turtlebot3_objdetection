#!/bin/bash

image_path="/home/lurps/ba_schraven/datasets/obj_detection_frames"
result_path="/home/lurps/ba_schraven/results/yolo/obj_detection"
WD="/home/lurps/catkin_ws/src/obj_detection/darknet"
cmd="./darknet detector test custom/OfficeHomeDataset_smallv2.data custom/OfficeHomeDataset_smallv2/yolov2-tiny-deploy.cfg custom/OfficeHomeDataset_smallv2/yolov2-tiny_190000.weights"

find $image_path -name *.jpg | while read line; do
	file_name=$(basename $line);
	result_file=$(echo $file_name | sed 's/.jpg/.txt/g');
	result=$result_path"/"$result_file;
	
	cd $WD;
	echo $(pwd);

	echo $result_file;
	$cmd $line;
	cp -v $WD/predictions.jpg $result_path/$file_name;
	cp -v $WD/prediction_details.txt $result;
done;
