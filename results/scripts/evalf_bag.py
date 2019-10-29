#!/usr/bin/env python
import sys
import os
import os.path
import numpy as np

category = [
    "Backpack",
    "Batteries",
    "Bottle",
    "Bucket",
    "Candles",
    "Drill",
    "Flipflops",
    "Hammer",
    "Helmet",
    "Keyboard",
    "Knives",
    "Marker",
    "Monitor",
    "Mug",
    "Pan",
    "Scissors",
    "Screwdriver",
    "Sneakers",
    "Toys",
    "TrashCan",
    "Webcam"
]

tp = np.zeros(len(category))
fp = np.zeros(len(category))
fn = np.zeros(len(category))

if(len(sys.argv) < 3):
    print("usage: python3 %s test_dir valid_dir" % (sys.argv[0]))
    exit()

test_dir_path = sys.argv[1]
valid_dir_path = sys.argv[2]

test_dir = os.listdir(test_dir_path)
valid_dir = os.listdir(valid_dir_path)

new_test_dir = list()
new_valid_dir = list()

for element in test_dir:
    filter_exp = ".txt"
    if(str(element).find(filter_exp, len(element) - len(filter_exp)) > 0):
        new_test_dir.append(element)

for element in valid_dir:
    filter_exp = ".txt"
    if(str(element).find(filter_exp, len(element) - len(filter_exp)) > 0):
        new_valid_dir.append(element)


for f in new_valid_dir:
    test_exists = os.path.isfile(str(test_dir_path) + str(f))
    valid_exists = os.path.isfile(str(valid_dir_path) + str(f))
    if(test_exists and valid_exists):
        testf = open(str(test_dir_path) + str(f), "r")
        validf = open(str(valid_dir_path) + str(f), "r")

        test = [line.rstrip('\n').rstrip('\r') for line in testf]
        valid = [line.rstrip('\n').rstrip('\r') for line in validf]

        testf.close()
        validf.close()

        for valid_entry in valid:
            if(len(valid_entry) > 0):
                valid_para = valid_entry.split(" ")
                valid_id = valid_para[0]

                found = False
                for test_entry in test:
                    if(len(test_entry) > 0):
                        if(test_entry == valid_id):
                            found = True

                if(found):
                    if(int(valid_id) <= len(category)):
                        tp[int(valid_id)] += 1
                else:
                    if(int(valid_id) <= len(category)):
                        fn[int(valid_id)] += 1

        for test_entry in test:
            is_fp = True
            if(len(test_entry) > 0):
                for valid_entry in valid:
                    if(len(valid_entry) > 0):
                        valid_para = valid_entry.split(" ")
                        valid_id = valid_para[0]

                        if(test_entry == valid_id):
                            is_fp = False

            if(is_fp):
                if(len(test_entry) > 0):
                    if(int(test_entry) <= len(category)):
                        fp[int(test_entry)] += 1


print("Test: %s %s" % (test_dir_path, len(new_test_dir)))
print("Valid: %s %s" % (valid_dir_path, len(new_valid_dir)))

print("TP: %s" % (tp))
print("FP: %s" % (fp))
print("FN: %s" % (fn))

precision = np.zeros(len(category))
recall = np.zeros(len(category))

for i in range(len(category)):
    if((float(tp[i]) + float(fp[i])) > 0):
        precision[i] = float(tp[i]) / (float(tp[i]) + float(fp[i]))

    if((float(tp[i]) + float(fn[i])) > 0):
        recall[i] = float(tp[i]) / (float(tp[i]) + float(fn[i]))

print("Precision: %s" % (precision))
print("Recall: %s" % (recall))
