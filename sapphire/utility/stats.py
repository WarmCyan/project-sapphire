#***************************************************************************
#
#  File: stats.py (sapphire.utility)
#  Date created: 06/21/2018
#  Date edited: 07/19/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Helper functions for collecting and storing engine statistics
#
#***************************************************************************

import os
import datetime
import csv
import pandas as pd

import sapphire.utility # TODO: is this actually necessary?

def _folderSize(path):
    total = 0
    file_count = 0
    
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
            file_count += 1
        elif entry.is_dir():
            sub_size, sub_count = _folderSize(entry.path)
            total += sub_size
            file_count += sub_count
    return total, file_count
        
# NOTE: returns string
def humanizeSize(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "EB"]
    unitIndex = 0
            
    while size > 1024:
        size /= 1024
        unitIndex += 1

    return '{0:.{1}f}'.format(size, 1) + " " + units[unitIndex]

def calculateFileStats(path):
    size, count = _folderSize(path)
    humansize = humanizeSize(size)
    return humansize, count, size
    
def updateFileStats(name, folderpath):
    humansize, count, size = calculateFileStats(folderpath)
    with open(sapphire.utility.stats_dir + name + "_filesize", 'w') as file:
        file.write(str(humansize))
    with open(sapphire.utility.stats_dir + name + "_filesize_raw", 'w') as file:
        file.write(str(size))
    with open(sapphire.utility.stats_dir + name + "_filecount", 'w') as file:
        file.write(str(count))

    return humansize, count, size # just in case you want to do something with displaying data without recalling calculate function

def updateTotalFileStats():
    # get a list of all files in the stats dir
    filesizeFiles = []
    filecountFiles = []
    
    for entry in os.scandir(sapphire.utility.stats_dir):
        if entry.is_file():
            if entry.name.endswith("_filesize_raw") and not entry.name.startswith("total"):
                filesizeFiles.append(entry.path)
            elif entry.name.endswith("_filecount") and not entry.name.startswith("total"):
                filecountFiles.append(entry.path)
    
    # loop through sizes and do the math
    totalSize = 0
    for path in filesizeFiles: 
        with open(path, 'r') as file:
            size = int(file.read())
            totalSize += size
    totalSizeReadable = humanizeSize(totalSize)
    
    # loop through counts and do the math
    totalCount = 0
    for path in filecountFiles: 
        with open(path, 'r') as file:
            count = int(file.read())
            totalCount += count

    # write all the things!
    with open(sapphire.utility.stats_dir + "total_filesize", 'w') as file:
        file.write(str(totalSizeReadable))
    with open(sapphire.utility.stats_dir + "total_filesize_raw", 'w') as file:
        file.write(str(totalSize))
    with open(sapphire.utility.stats_dir + "total_filecount", 'w') as file:
        file.write(str(totalCount))

def getTotalFileStats():
    with open(sapphire.utility.stats_dir + "total_filesize", 'r') as file:
        size = file.readline()
    with open(sapphire.utility.stats_dir + "total_filecount", 'r') as file:
        count = file.readline()
    return size, count

def updateStatus(name, status):
    if name is not None:
        with open(sapphire.utility.stats_dir + name + "_status", 'w') as file:
            file.write(status)
            
def updateLastTime(name):
    with open(sapphire.utility.stats_dir + name + "_timestamp", 'w') as file:
        file.write(sapphire.utility.getTimestamp(datetime.datetime.now()))
    
def recordAllSpaceStats():
    spaceStatsTimeline = sapphire.utility.stats_dir + "space_stats_timeline.csv"
    
    
    # get a listing of all files to keep a record of
    filesList = []
    statsNames = []

    for entry in os.scandir(sapphire.utility.stats_dir):
        if entry.is_file() and (entry.name.endswith("_filesize_raw") or entry.name.endswith("_filecount")):
            filesList.append(entry.path)
            statsNames.append(entry.name)

    statsNames.append("time")

    # get the row of data from each individual file
    row = {}
    row["time"] = int(datetime.datetime.now().timestamp())
    for i in range(0, len(filesList)):
        with open(filesList[i], 'r') as file:
            row[statsNames[i]] = int(file.read())
    
    # make the timeline file if it doesn't exist   
    if not os.path.exists(spaceStatsTimeline):
        sapphire.utility.logging.log("Timeline file doesn't exist, creating '" + spaceStatsTimeline + "'...", "WARNING", source="Utility")
        with open(spaceStatsTimeline, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n',fieldnames=statsNames)
            writer.writeheader()

    # read in the csv, add new row to it, and write it back out
    table = pd.read_csv(spaceStatsTimeline)
    rowFrame = pd.io.json.json_normalize(row)
    table = pd.concat([table, rowFrame])
    table.to_csv(spaceStatsTimeline, index=False)            
