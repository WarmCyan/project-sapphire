#***************************************************************************
#
#  File: __init__.py (sapphire.utility)
#  Date created: 05/17/2018
#  Date edited: 06/21/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Various global utility and config functions for sapphire
#
#***************************************************************************

import datetime
from pytz import timezone

import uuid
import json

from sapphire.utility.exceptions import BadSettings
from sapphire.utility.logging import registerLogger, ConsoleLogger


feed_scrape_raw_dir = ""
feed_scrape_tmp_dir = ""
metadata_queue_dir = ""
content_scrape_raw_dir = ""
content_store_dir = ""

metadata_store = ""

stats_dir = ""

db_host = ""
db_user = ""
db_password = ""
db_db = ""


rootUUID = uuid.UUID('{00000000-0000-0000-0000-000000000000}')


# datetime format directives from https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

def readConfig(config):
    global feed_scrape_raw_dir
    global feed_scrape_tmp_dir
    global metadata_queue_dir
    global metadata_store
    global content_scrape_raw_dir
    global content_store_dir
    global stats_dir
    
    global db_host
    global db_user
    global db_password
    global db_db
    
    settings = {}
    with open(config, 'r') as f:
        settings = json.load(f)
        
    try: feed_scrape_raw_dir = settings["feed_scrape_raw_dir"]
    except KeyError: raise BadSettings("Setting 'feed_scrape_raw_dir' not found")

    try: feed_scrape_tmp_dir = settings["feed_scrape_tmp_dir"]
    except KeyError: raise BadSettings("Setting 'feed_scrape_tmp_dir' not found")
    
    try: metadata_queue_dir = settings["metadata_queue_dir"]
    except KeyError: raise BadSettings("Setting 'metadata_queue_dir' not found")

    try: metadata_store = settings["metadata_store"]
    except KeyError: raise BadSettings("Setting 'metadata_store' not found")
    
    try: content_store_dir = settings["content_store_dir"]
    except KeyError: raise BadSettings("Setting 'content_store_dir' not found")
    
    try: content_scrape_raw_dir = settings["content_scrape_raw_dir"]
    except KeyError: raise BadSettings("Setting 'content_scrape_raw_dir' not found")
    
    try: stats_dir = settings["stats_dir"]
    except KeyError: raise BadSettings("Setting 'stats_dir' not found")
    
    feed_scrape_raw_dir = cleanFolderSetting(feed_scrape_raw_dir)
    feed_scrape_tmp_dir = cleanFolderSetting(feed_scrape_tmp_dir)
    metadata_queue_dir = cleanFolderSetting(metadata_queue_dir)
    content_scrape_raw_dir = cleanFolderSetting(content_scrape_raw_dir)
    content_store_dir = cleanFolderSetting(content_store_dir)
    stats_dir = cleanFolderSetting(stats_dir)

    try: db_host = settings["db_host"]
    except KeyError: raise BadSettings("Setting 'db_host' not found")
    
    try: db_user = settings["db_user"]
    except KeyError: raise BadSettings("Setting 'db_user' not found")
    
    try: db_password = settings["db_password"]
    except KeyError: raise BadSettings("Setting 'db_password' not found")
    
    try: db_db = settings["db_db"]
    except KeyError: raise BadSettings("Setting 'db_db' not found")

    try: 
        cl = settings["ConsoleLogger"]
        
        try: channels = cl["channels"]
        except KeyError: raise BadSettings("Setting 'channels' not found under ConsoleLogger")
        
        try: sources = cl["sources"]
        except KeyError: raise BadSettings("Setting 'sources' not found under ConsoleLogger")

        try: preChannel = cl["prepend_channel"]
        except KeyError: raise BadSettings("Setting 'prepend_channel' not found under ConsoleLogger")
        
        try: preSource = cl["prepend_source"]
        except KeyError: raise BadSettings("Setting 'prepend_source' not found under ConsoleLogger")

        logger = ConsoleLogger(channels, sources, preChannel, preSource)
        registerLogger(logger)
    except: pass

def writeConfig():
    pass
    

# makes sure it ends in "/"
def cleanFolderSetting(folder):
    if folder[-1] != "/":
        folder = folder + "/"
    return folder


# (don't call these)
def _getFormattedTimestamp(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def _getFileFormattedTimestamp(dt):
    return dt.strftime("%Y.%m.%d_%H.%M.%S")

def _getUTCTime(dt):
    dt = dt.astimezone(timezone('UTC'))
    return dt


# CALL THESE
def getTimestamp(dt):
    return _getFormattedTimestamp(_getUTCTime(dt))

def getFileTimeStamp(dt):
    return _getFileFormattedTimestamp(_getUTCTime(dt))

def getDT(strTime):
    return datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")

#def getCurrentTimestamp():
    #return getCorrectTimestamp(datetime.datetime.now())

def getNamespaceUUID(namespaceString):
    return uuid.uuid5(rootUUID, namespaceString)
