#***************************************************************************
#
#  File: scheduler.py (sapphire.utility)
#  Date created: 06/30/2018
#  Date edited: 07/04/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Helper functions for running code at a specific time
#
#***************************************************************************

import datetime
import sapphire.utility

def getSchedule(name):
    schedule = []
    
    with open(sapphire.utility.schedule_dir + name + ".dat", 'r') as f:
        for line in f:
            schedule.append(line.rstrip())

    return schedule

def writeSchedule(name, schedule):
    with open(sapphire.utility.schedule_dir + name + ".dat", 'w') as f:
        for item in schedule:
            f.write(str(item) + "\n")

# NOTE: also returns the original schedule without the runnable items
def findRunnable(schedule):
    validSchedule = []
    nonRunnableLines = []
    
    for item in schedule:
        parts = item.split(' ')
        
        now = datetime.datetime.now()
        if datetime.datetime.fromtimestamp(int(parts[0])) < now:
            validSchedule.append([parts[0], ' '.join(parts[1:])])
        else:
            nonRunnableLines.append(item)
                        
    return validSchedule, nonRunnableLines
