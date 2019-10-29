#!/usr/bin/env python
import sys
import os
import os.path
import numpy as np

# valid     12          157     51      522     378
#           category    left1   top1    left2   top2
# test      Prediction: Monitor     Location:   127   541    50   366
#                       category                left1 left2  top1 top2
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


def getTest(data):
    if(len(data) > 0):
        category = ""
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

        for i in range(len(data)):
            if(str(data[i]).find("Prediction:") > -1):
                p_category = i + 1
            elif(str(data[i]).find("Location:") > -1):
                p_left = i + 1
                p_top = i + 3
                p_right = i + 2
                p_bottom = i + 4

        category = data[p_category]
        left = data[p_left]
        top = data[p_top]
        right = data[p_right]
        bottom = data[p_bottom]

        return [category, left, top, right, bottom]

    else:
        return []


def borderFit(tleft, ttop, tright, tbottom, vleft, vtop, vright, vbottom):
    if(vleft < tleft < vright or
            vtop < ttop < vbottom or
            vleft < tright < vright or
            vtop < tbottom < vbottom):
        return True

    return False


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

        test = list()
        valid = list()
        for e in test_str:
            test.append(getTest(str(e).split(" ")))
        for e in valid_str:
            valid.append(str(e).split(" "))

        # print(test)
        # print(valid)

        # check for TP and FP
        for t in test:
            if(len(t) > 1):
                for v in valid:
                    if(len(v) > 1):
                        if(category.index(t[0]) == int(v[0]) and
                                borderFit(t[1], t[2], t[3], t[4],
                                          v[1], v[2], v[3], v[4])):
                            tp[category.index(t[0])] += 1

                            for i in range(1, len(t)):
                                t[i] = int(t[i])
                            for i in range(1, len(v)):
                                v[i] = int(v[i])

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
                        if(category.index(t[0]) == int(v[0])):
                            if(not borderFit(t[1], t[2], t[3], t[4],
                                             v[1], v[2], v[3], v[4])):
                                fn[int(v[0])] += 1
                        else:
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
