#!/usr/bin/env python3

import json
import datetime
from collections import namedtuple
import csv
import os
from os import listdir
from os.path import isfile, join
import collections
from json import JSONDecoder
from collections import OrderedDict
from datetime import datetime
import csv
import argparse
import sys
import ast

# Parse arguments
parser = argparse.ArgumentParser(usage='python PineappleParser.py -i input.json -o output.csv -f failed.csv')
parser.add_argument("-i", "--input", help="The input JSON file", required = True )
parser.add_argument("-o", "--output", help="The CSV filename (if no file exists will be initialized, otherwise append)", required = True)
parser.add_argument("-f", "--failed", help ="The CSV filename to place the IDs of people who failed the attention check)")
args = parser.parse_args()

jsonFile = args.input
output = args.output
failed = args.failed

def readFile (fileName):
    print (fileName);
    with open (fileName, 'rb') as file:
        fileContent = file.read();
        #jsObject = json.loads(fileContent, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()));
        jsObject = json.loads(fileContent, object_pairs_hook=OrderedDict);      # Changed data structure to OrderedDict to be able to loop through the rules to allow the number of rules to be variable (the version in the line above this does not preserve order). Also this allows #rule-1 to be a valid name (the line above doesn't allow # or -)
    return jsObject;

loadedJSON = readFile(jsonFile)

# Extract values from object
id = loadedJSON['id']
intCond = loadedJSON['intCond']
ordCond = loadedJSON['ordCond']
midQs = loadedJSON['midQs']
pAns = loadedJSON['pAns']
# Pre Questionnaire
age = loadedJSON['preQ']['age']
CVWeakness = loadedJSON['preQ']['CVWeakness']
education = loadedJSON['preQ']['education']
gender = loadedJSON['preQ']['gender']
MLExp = loadedJSON['preQ']['MLExp']
# Post Questionnaire
comments = loadedJSON['postQ']['comments']
weak = loadedJSON['postQ']['weak']
changes = loadedJSON['postQ']['changes']
changesS = loadedJSON['postQ']['changesS']
# Times
start = loadedJSON['time']['start']
end = loadedJSON['time']['end']
firstE = loadedJSON['time']['firstE']
secondE = loadedJSON['time']['secondE']
thirdE = loadedJSON['time']['thirdE']
firstS = loadedJSON['time']['firstS']
secondS = loadedJSON['time']['secondS']
thirdS = loadedJSON['time']['thirdS']
tutBegin = loadedJSON['time']['tutBegin']
finalEnd = loadedJSON['time']['finalEnd']
trust1 = loadedJSON['trust1']
trust2 = loadedJSON['trust2']
trust3 = loadedJSON['trust3']
trustUses = loadedJSON['trustUses']


# Convert text lists into actual lists
midQsList = ast.literal_eval(midQs)
pAnsList = ast.literal_eval(pAns)

# Check conditions
if(ordCond == "0"):
    cAns = [[0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]]
    cAcc = [70, 80, 90]
if(ordCond == "1"):
    cAns = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]]
    cAcc = [80, 80, 80]
if(ordCond == "2"):
    cAns = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]]
    cAcc = [90, 80, 70]

# Calculate accuracy of answers
totalRight = [0, 0, 0, 0]
diffRight = [0, 0, 0, 0]
accuracy = [0, 0, 0, 0]
for i in range(len(cAns)):
    for j in range(len(cAns[i])):
        if pAnsList[i][j] == cAns[i][j]:
            totalRight[i] = totalRight[i] + 1
            if cAns[i][j] == 1:
                diffRight[i] = diffRight[i] + 1
for i in range(len(totalRight)):
    accuracy[i] = float(totalRight[i]) / float(len(cAns[i]))

print(accuracy)
# Throw out data if less than 70% of the responses are correct (50% would be expected value due to chance, based on pilot testing so far only a few errors are expected, the task itself is pretty easy)
taskAcc = float(totalRight[0] + totalRight[1] + totalRight[2]) / float(90)
diffAcc = float(diffRight[0] + diffRight[1] + diffRight[2]) / float(18)
if ((taskAcc < 0.7) or (diffAcc < 0.7)):
    header = ["id", "intCond", "ordCond", "taskAcc"]
    if(os.path.isfile(failed) == False):
        with open(failed, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            filewriter.writerow(header)
        print("Created CSV " + failed)

    row = [id, intCond, ordCond, taskAcc]
    with open(failed, 'a') as csvfile:
        filewriter = csv.writer(csvfile, lineterminator='\n')
        filewriter.writerow(row)
    sys.exit("Failed attention check")

# Calculate times for each round
def get_sec(time_str):
    #Get Seconds from time.
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

times = [get_sec(firstE) - get_sec(firstS), get_sec(secondE) - get_sec(secondS), get_sec(thirdE) - get_sec(thirdS)]
taskTime = times[0] + times[1] + times[2]
totalTime = get_sec(end) - get_sec(start)
turkTime = get_sec(finalEnd) - get_sec(tutBegin)

# Calculate accuracy error for each round
# TODO: how to analyse change in answers across rounds?
# Time series analysis? What's appropriate for this data
for i in range(len(midQsList)):
    midQsList[i] = float(midQsList[i])

predErr = [cAcc[0] - midQsList[0], cAcc[1] - midQsList[1], cAcc[2] - midQsList[2]]
predDiff = midQsList[2] - midQsList[0]
predTaskList = pAnsList[3]
totalIdentified = 0
if (predTaskList[1] == 1):
    totalIdentified = totalIdentified + 1
if (predTaskList[6] == 1):
    totalIdentified = totalIdentified + 1
if (predTaskList[11] == 1):
    totalIdentified = totalIdentified + 1
if (predTaskList[16] == 1):
    totalIdentified = totalIdentified + 1
if (predTaskList[18] == 1):
    totalIdentified = totalIdentified + 1
print(totalIdentified)
predTaskScore = float(totalIdentified) / 5

if ordCond == "0":
    predDiffAcc = predDiff - 20
if ordCond == "1":
    predDiffAcc = predDiff
if ordCond == "2":
    predDiffAcc = predDiff - (-20)

trust1 = int(trust1)
trust2 = int(trust2)
trust3 = int(trust3)
trustAvg = float(trust1 + trust2 + trust3) / float(3)
trustUses = int(trustUses)


header = ["id", "allCond", "intCond", "ordCond", "taskAcc", "predDiff", "predDiffAcc", "changesScale", "predTaskScore", "trustAvg", "trust1", "trust2", "trust3", "trustUses", "acc0", "acc1", "acc2", "err0", "err1", "err2", "taskTime", "totalTime", "turkTime", "time0", "time1", "time2", "comments", "weak", "changes", "age", "CV", "education", "gender", "MLExp"]

# Create CSV file if not already created
flag = 0
if(os.path.isfile(output) == False):
    with open(output, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        filewriter.writerow(header)
    print("Created CSV " + output)
# Check that CSV format matches
else:
    with open(output, 'r') as csvfile:
        filereader = csv.reader(csvfile)
        fileHeader = next(filereader)   # Get the first row as the file header
        if(len(fileHeader) == len(header)):
            for i in range(len(fileHeader)):
                if(fileHeader[i] != header[i]):
                    flag = 1;
        else:
            flag = 1

if(flag == 1):
    print("Existing CSV format does not match file CSV format")
else:
    # Generate row
    row = [id, intCond + "_" + ordCond, intCond, ordCond, taskAcc, predDiff, predDiffAcc, changesS, predTaskScore, trustAvg, trust1, trust2, trust3, trustUses, accuracy[0], accuracy[1], accuracy[2], predErr[0], predErr[1], predErr[2], taskTime, totalTime, turkTime, times[0], times[1], times[2], comments, weak, changes, age, CVWeakness, education, gender, MLExp]
    # Append to CSV
    print("Appending to CSV")
    with open(output, 'a') as csvfile:
        filewriter = csv.writer(csvfile, lineterminator='\n')
        filewriter.writerow(row)
