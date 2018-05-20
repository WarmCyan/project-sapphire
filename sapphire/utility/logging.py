#***************************************************************************
#
#  File: logging.py
#  Date created: 05/20/2018
#  Date edited: 05/20/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Logging classes and functions to abstract logging process
#
#***************************************************************************

import datetime

registeredLoggers = []

# NOTE: call this one externally!
def log(msg, channel="", source=None):
    global registeredLoggers
    now = datetime.datetime.now()
    logMessage = LogMessage(msg, now, channel, source)
    for logger in registeredLoggers:
        logger.log(logMessage)

def registerLogger(logger):
    global registeredLoggers
    registeredLoggers.append(logger)

def deregisterLogger(logger):
    global registeredLoggers
    registeredLoggers.remove(logger)

# NOTE: this is what all loggers expect passed to them in log()
class LogMessage:

    def __init__(self, msg, dt, channel, source):
        self.msg = msg
        self.dt = dt
        self.channel = channel
        self.source = source

class ConsoleLogger:

    def __init__(self, channelAssociations={}, sourceAssociations={}):
        self.channelAssociations = channelAssociations
        self.sourceAssociations = sourceAssociations

    def log(self, msg):
        localAssociations = self.channelAssociations
        if msg.source in self.sourceAssociations:
            localAssociations = self.sourceAssociations[msg.source]

        messageSettings = None
        if msg.channel in localAssociations:
            messageSettings = localAssociations[msg.channel]
        elif "[ALL]" in localAssociations:
            messageSettings = localAssociations["[ALL]"]

        if messageSettings != None:
            # TODO: add color and prepend settings handler
            timeStr = msg.dt.strftime("%Y-%m-%d::%H:%M:%S:%f")
            messageString = "[" + timeStr + "]:: " + msg.msg
            print(messageString)
