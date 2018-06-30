#***************************************************************************
#
#  File: scheduler.py (sapphire.utility)
#  Date created: 06/30/2018
#  Date edited: 06/30/2018
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

def findRunnable(schedule):
    validSchedule = []
    
    for item in schedule:
        parts = item.split(' ')

        now = datetime.datetime.now()
        if not isinstance(parts[0], int) or datetime.datetime.fromtimestamp(parts[0]) > now:
            #validSchedule.append(' '.join(parts[1:]))
            #validSchedule.append([' '.join(parts[1:])])
            if isinstance(parts[0], int): validSchedule.append([parts[0], ' '.join(parts[1:])])
            else: validSchedule.append([0, ' '.join(parts)])
                        

    return validSchedule
