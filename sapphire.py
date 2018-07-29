#***************************************************************************
#
#  File: sapphire.py
#  Date created: 06/21/2018
#  Date edited: 07/29/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Application for running sapphire backend engine
#
#***************************************************************************

import sys
import os
import pycolor
import time
import datetime

from sapphire.managers import article
import sapphire.utility
import sapphire.utility.stats


VERSION = "1.0.1"
VERSION_DATE = "07/29/2018"
COPYRIGHT = "Copyright © 2018 Digital Warrior Labs"

execution_unit_name = None
article_man = None

def showHelp():
    print("This is the help menu")


def reportFolderStats(name, folderpath):
    usage, files, size = sapphire.utility.stats.updateFileStats(name, folderpath)
    sapphire.utility.stats.updateTotalFileStats()
    print("\n" + folderpath + ":")
    print(usage)
    print(str(files) + " files")


def initiateSchedule(name):
    now = datetime.datetime.now()
    # TODO: note that this is only temporary
    if name == "feed":
        # find the first instances
        schedule = []
        for time in sapphire.utility.feed_rates["all"]["times"]:
            timedt = sapphire.utility.getDTFromMilitary(str(time))
            if timedt < datetime.datetime.now():
                timedt += datetime.timedelta(1)
            schedule.extend([str(int(timedt.timestamp())) + " scrape feed", str(int(timedt.timestamp())) + " queue"])
        sapphire.utility.scheduler.writeSchedule(name, schedule)
    elif name == "content":
        schedule = [str(int(now.timestamp())) + " scrape article"]
        sapphire.utility.scheduler.writeSchedule(name, schedule)
    elif name == "utility":
        schedule = []
        for entry in sapphire.utility.timeline_times["space"]:
            timedt = sapphire.utility.getDTFromMilitary(str(entry))
            if timedt < datetime.datetime.now():
                timedt += datetime.timedelta(1)
            schedule.append(str(int(timedt.timestamp())) + " record stats")
            sapphire.utility.scheduler.writeSchedule(name, schedule)
        
# NOTE: rate is in seconds
def pollSchedule(name, rate):
    polling = True

    while polling:
        pollTime = sapphire.utility.getTimestamp(datetime.datetime.now())
        pollTimeS = str(int(datetime.datetime.now().timestamp()))
        print("Last polled at " + pollTime + " (" + pollTimeS + ")\r", end='')
        if name is not None:
            sapphire.utility.stats.updateLastTime(name + "_poll")
        
        schedule = sapphire.utility.scheduler.getSchedule(name)
        runnableSchedule, remaining = sapphire.utility.scheduler.findRunnable(schedule)
        for item in runnableSchedule:
            if item[0] != 0:
                readableTime = sapphire.utility.getTimestamp(datetime.datetime.fromtimestamp(int(item[0])))
                print("Running '" + item[1] + "' scheduled for " + readableTime + "...")
                newItems = handleCommand(item[1], True, rate)

                if newItems is not None and not isinstance(newItems, int): remaining.extend(newItems)
                sapphire.utility.scheduler.writeSchedule(name, remaining)
                print("Resuming poll...\r", end='')
        
        time.sleep(rate)
            

# NOTE: this returns any new commands 
# rate is the polling rate
def handleCommand(cmd, poll=False, rate=0):
    parts = cmd.split(' ')
    
    if parts[0] == "exit":
        return -1
    elif parts[0] == "stats":
        reportFolderStats("feed_scrape_raw_dir", sapphire.utility.feed_scrape_raw_dir)
        reportFolderStats("feed_scrape_tmp_dir", sapphire.utility.feed_scrape_tmp_dir)
        reportFolderStats("metadata_queue_dir", sapphire.utility.metadata_queue_dir)
        reportFolderStats("content_scrape_raw_dir", sapphire.utility.content_scrape_raw_dir)
        reportFolderStats("content_store_dir", sapphire.utility.content_store_dir)

        size, count = sapphire.utility.stats.getTotalFileStats()
        print("\nTotal: " + count + " files utilizing " + size)
        return 0
        
    elif parts[0] == "scrape":
        if parts[1] == "feed":
            article_man.scrapeFeeds()

            if poll:
                nextCommands = []
                
                # get the next scrape time
                now = datetime.datetime.now()
                nexttime = now + datetime.timedelta(1)
                nexttime = nexttime.timestamp()
                return [str(int(nexttime)) + " scrape feed", str(int(nexttime)) + " queue"]
                '''
                if "all" in sapphire.utility.feed_rates:
                    now = datetime.datetime.now()

                    # determine if this is a specific time
                    if "times" in sapphire.utility.feed_rates["all"]:
                        nexttime = 0

                        # loop through each time, if the current time is greater than it, and the last poll was less than it, it was that specified time (or a freaky coincidence)
                        for time in sapphire.utility.feed_rates["all"]["times"]:
                            timeDT = sapphire.utility.getDTFromMilitary(str(time))
                            prevPollDT = now - datetime.timedelta(seconds=rate)
                            if now.timestamp() > timeDT.timestamp() and prevPollDT.timestamp() < timeDT.timestamp():
                                #nextCommands.append(str(int(I
                                nexttime = timeDT.timestamp()
                                return [str(int(nexttime)) + " scrape feed", str(int(nexttime)) + " queue"]
                '''
            else: return 0
                            
        elif parts[1] == "article":
            article_man.scrapeNextArticle()

            if poll:
                if sapphire.utility.content_rate is not None:
                    now = datetime.datetime.now()
                    then = now + datetime.timedelta(0,sapphire.utility.content_rate)
                    return [str(int(then.timestamp())) + " scrape article"]
            else: return 0
            
    elif parts[0] == "queue":
        article_man.consumeQueue()
        return 0
    elif parts[0] == "record":
        if parts[1] == "stats":
            print("Recording all space stats...")
            sapphire.utility.stats.recordAllSpaceStats()
            if poll:
                # get the next scrape time
                now = datetime.datetime.now()
                nexttime = now + datetime.timedelta(1)
                return [str(int(nexttime.timestamp())) + " record stats"]
            return 0
    elif parts[0] == "test":
        if parts[1] == "article":
            article_man.testScrapeNextArticle()
            return 0
    return 1

def repl():
    print(pycolor.BRIGHTBLUE + "Sapphire> " + pycolor.RESET, end='')
    command = input()

    status = handleCommand(command)
    if status == 1: print(pycolor.BRIGHTRED + "Unrecognized command '" + command + "'" + pycolor.RESET)
    return status

def repl_loop():
    result = 0
    while result != -1:
        result = repl()



# ----------------------------------------------------------------------
# MAIN PROGRAM FLOW
# ----------------------------------------------------------------------

    
# handle a confused user
if len(sys.argv[1:]) == 0 or sys.argv[1] == 'help' or sys.argv[1] == '-h':
    showHelp()
    exit()

# print fanciness informational stuffs
print("\n=====================================================")
print(pycolor.BRIGHTBLUE + "SAPPHIRE ENGINE" + pycolor.RESET)
print("Version: " + pycolor.BRIGHTYELLOW + VERSION + pycolor.RESET)
print("Date: " + pycolor.BRIGHTYELLOW + VERSION_DATE + pycolor.RESET)
print(COPYRIGHT)
print("=====================================================\n")

# handle the first argument (the mode word)
mode = sys.argv[1]
print("Mode: " + str(mode) + "\n")

# get default config
config_filename = os.getenv("CONF_DIR") + "/sapphire_config.json"

# check for local config
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f == "sapphire_config.json": config_filename = "./sapphire_config.json"

# handle command line arguments
for arg in sys.argv[2:]:
    if arg.startswith("--config"):
        config_filename = arg[arg.index('=')+1:]
    elif arg.startswith("--name"):
        execution_unit_name = arg[arg.index('=')+1:]

article_man = article.ArticleManager(execution_unit_name, config_filename)
print() # add a newline

# handle mode
if mode == "repl":
    repl_loop()
elif mode == "feed":
    initiateSchedule("feed")
    pollSchedule("feed", 5)
elif mode == "content":
    initiateSchedule("content")
    pollSchedule("content", 5)
elif mode == "utility":
    initiateSchedule("utility")
    pollSchedule("utility", 5)
