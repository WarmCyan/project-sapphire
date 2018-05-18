import datetime
from pytz import timezone

import json

from sapphire.utility.exceptions import BadSettings


feed_scrape_raw_tmp_dir = ""
feed_scrape_tmp_dir = ""
metadata_queue_dir = ""

metadata_store = ""



def readConfig(config):
    global feed_scrape_raw_tmp_dir
    settings = {}
    with open(config, 'r') as f:
        settings = json.load(f)
        
    try:
        feed_scrape_raw_tmp_dir = settings["feed_scrape_raw_tmp_dir"]
    except KeyError:
        raise BadSettings("Setting 'feed_scrape_raw_tmp_dir' not found")
    

def writeConfig():
    pass
    


# (don't call these)
def _getFormattedTimestamp(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def _getUTCTime(dt):
    dt = dt.astimezone(timezone('UTC'))
    return dt


# CALL THESE
def getTimestamp(dt):
    return _getFormattedTimestamp(_getUTCTime(dt))

#def getCurrentTimestamp():
    #return getCorrectTimestamp(datetime.datetime.now())
