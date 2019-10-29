#!/usr/bin/env python
import sys
import os
import os.path
import numpy as np

# valid     12          157     51      522     378
#           category    left1   top1    left2   top2
# test      /home/lurps/ba_schraven/datasets/obj_detection_frames/obj_detection_frame0003.jpg,
#            Person,0.77,0.224591329694,0.13250464201,0.370356053114,0.13250464201,0.370356053114,0.238269358873,0.224591329694,0.238269358873,
#            Person,0.75,0.107092872262,0.0742260068655,0.220857590437,0.0742260068655,0.220857590437,0.198343664408,0.107092872262,0.198343664408,
#            Person,0.63,0.00685553252697,0.00315998494625,0.111509785056,0.00315998494625,0.111509785056,0.220468506217,0.00685553252697,0.220468506217
#            category,probability,left,top,right,top,right,bottom,left,bottom
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

category_cloud = [
    # Backpack
    ["Backpack", "Bag", "Handbag", "Luggage & bags"],
    # Batteries
    ["Batteries", "Battery"],
    # Bottle
    ["Bottle"],
    # Bucket
    ["Bucket"],
    # Candles
    ["Candle"],
    # Drill
    ["Drill", "Power tool"],
    # Flipflops
    ["Sandal", "Shoe"],
    # Hammer
    ["Hammer"],
    # Helmet
    ["Helmet", "Motorcycle helmet"],
    # Keyboard
    ["Computer keyboard", "Keyboard"],
    # Knives
    ["Knive", "Kitchenware"],
    # Marker
    ["Marker", "Pencil", "Pen"],
    # Monitor
    ["Computer monitor", "Television"],
    # Mug
    ["Mug"],
    # Pan
    ["Pan", "Kitchen appliance"],
    # Scissors
    ["Scissors"],
    # Screwdriver
    ["Screwdriver"],
    # Sneakers
    ["Shoe", "Sneaker"],
    # Toys
    ["Ball", "Toy"],
    # TrashCan
    ["Trash", "Trashcan"],
    # Webcam
    ["Webcam", "Camera"]
]


def getTest(data):
    if(len(data) > 1):
        num_datasets = int((len(data) - 1) / 10)
        return_value = list()

        for s in range(num_datasets):
            cate = ""
            left = ""
            top = ""
            right = ""
            bottom = ""

            p_category = 0
            p_left = 0
            p_top = 0
            p_right = 0
            p_bottom = 0

            data_old = data
            data = list()
            for d in data_old:
                if(len(d) > 0):
                    data.append(d)

            p_category = 1 + 10 * s
            p_left = 3 + 10 * s
            p_top = 4 + 10 * s
            p_right = 5 + 10 * s
            p_bottom = 8 + 10 * s

            cate = ""
            if (d2_index(data[p_category]) > -1):
                cate = category[d2_index(data[p_category])]
            left = int(round(float(data[p_left]) * 640.0))
            top = int(round(float(data[p_top]) * 480.0))
            right = int(round(float(data[p_right]) * 640.0))
            bottom = int(round(float(data[p_bottom]) * 480.0))

            if (cate != ""):
                return_value.append([cate, left, top, right, bottom])

        return return_value

    else:
        return []


def borderFit(tleft, ttop, tright, tbottom, vleft, vtop, vright, vbottom):
    if(vleft < tleft < vright or
            vtop < ttop < vbottom or
            vleft < tright < vright or
            vtop < tbottom < vbottom):
        return True

    return False


def d2_index(find):
    t_index = -1
    for i in range(len(category)):
        for j in range(len(category_cloud[i])):
            if(find == category_cloud[i][j]):
                t_index = i
                break
    return t_index


tp = np.zeros(len(category))
fp = np.zeros(len(category))
fn = np.zeros(len(category))

iou = [list() for l in range(len(category))]

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

        test_str = [line.rstrip('\n').rstrip('\r') for line in testf]
        valid_str = [line.rstrip('\n').rstrip('\r') for line in validf]

        testf.close()
        validf.close()

        valid = list()
        test = getTest(str(test_str).split(","))

        for e in valid_str:
            valid.append(str(e).split(" "))

        # print(test)
        # print(valid)

        # check for TP and FP
        for t in test:
            if(len(t) > 1):
                for v in valid:
                    if(len(v) > 1):
                        for i in range(1, len(v)):
                            v[i] = int(v[i])
                        if(category.index(t[0]) == int(v[0]) and
                                borderFit(t[1], t[2], t[3], t[4],
                                          v[1], v[2], v[3], v[4])):
                            tp[category.index(t[0])] += 1

                            for i in range(1, len(t)):
                                t[i] = int(t[i])

                            intersection_left = max(t[1], v[1])
                            intersection_top = max(t[2], v[2])
                            intersection_right = min(t[3], v[3])
                            intersection_bottom = min(t[4], v[4])

                            intersection = (
                                intersection_right - intersection_left) * (
                                intersection_bottom - intersection_top)

                            overlap = (t[3] - t[1]) * (t[4] - t[2]) + (
                                v[3] - v[1]) * (v[4] - v[2]) - intersection

                            iou[int(v[0])].append(
                                float(intersection) / float(overlap))

                        else:
                            fp[category.index(t[0])] += 1
                    else:
                        fp[category.index(t[0])] += 1

        # check for FN
        for v in valid:
            if(len(v) > 1):
                for t in test:
                    if(len(t) > 1):
                        for i in range(1, len(v)):
                            v[i] = int(v[i])
                        if(category.index(t[0]) == int(v[0])):
                            if(not borderFit(t[1], t[2], t[3], t[4],
                                             v[1], v[2], v[3], v[4])):
                                fn[int(v[0])] += 1
                        else:
                            if(int(v[0]) < 21):
                                fn[int(v[0])] += 1
                    else:
                        fn[int(v[0])] += 1


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

print("\n\nIoU")
for i in range(len(category)):
    average = 0
    if(len(iou[i]) > 0):
        sum = 0
        for j in iou[i]:
            sum += j

        average = sum / len(iou[i])
    print("\t%s: %s with %s" % (category[i], average, iou[i]))
