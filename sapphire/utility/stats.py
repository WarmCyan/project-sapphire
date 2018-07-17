#***************************************************************************
#
#  File: stats.py (sapphire.utility)
#  Date created: 06/21/2018
#  Date edited: 07/17/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Helper functions for collecting and storing engine statistics
#
#***************************************************************************

import os
import datetime

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
    
