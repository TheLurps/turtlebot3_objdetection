#!/bin/bash

image_path="/home/lurps/ba_schraven/datasets/obj_detection_frames"
result_path="/home/lurps/ba_schraven/results/bag/obj_detection"
WD="/home/lurps/catkin_ws/src/obj_detection/Minimal-Bag-of-Visual-Words-Image-Classifier"
cmd="python $WD/classify.py -c $WD/OfficeHomeDataset_smallv2_codebook.file -m $WD/OfficeHomeDataset_smallv2_trainingdata.svm.model"

find $image_path -name *.jpg | while read line; do
	file_name=$(basename $line);
	result_file=$(echo $file_name | sed 's/.jpg/.txt/g');
	result=$result_path"/"$result_file;
	
	echo $result_file;
	$cmd $line;
	cp -v $WD/OfficeHomeDataset_smallv2_trainingdata.svm.prediction $result;
done;
