#***************************************************************************
#
#  File: metadata.py (sapphire.managers)
#  Date created: 05/26/2018
#  Date edited: 05/27/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Contains class that handles master collection of metadata
#
#***************************************************************************

import uuid
import json
import csv
import os
import pandas as pd

import sapphire.utility
from sapphire.article import Article


class MetadataManager:

    IDENTIFIER = "Metadata Manager"

    def __init__(self):
        self.store_filename = sapphire.utility.metadata_store
        self.queue_dir = sapphire.utility.metadata_queue_dir
        self.store = None # will contain the dataframe

    def loadStore(self):
        self.log("Loading metadata store...")

        if not os.path.exists(self.store_filename):
            self.log("Metadata store file doesn't exist, creating '" + self.store_filename + "'...", "WARNING")
            with open(self.store_filename, 'a') as csv_file:
                headers = ["UUID"]
                headers.extend(list(Article().getMetadataDictionary().keys()))
                writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n',fieldnames=headers)
                writer.writeheader()
            
        
        self.store = pd.read_csv(self.store_filename)
        self.log("Metadata store loaded")

    def saveStore(self):
        self.log("Saving metadata store...")
        self.store.to_csv(self.store_filename, index=False)
        self.log("Saved!")
        

    # NOTE: consumption of 0 means consume all
    def consumeQueue(self, maximumConsumption=0):
        numberText = "all"
        if maximumConsumption > 0: numberText = str(maximumConsumption)
        self.log("Consuming " + numberText + " items from the queue...")
        
        # get directory listing
        files = os.listdir(self.queue_dir)
        for file in files:
            if file == "ph.txt": # TODO: remove this for final thing, cause placeholders unnecessary
                continue

            articlesJSON = None

            filename = self.queue_dir + file
            self.log("Opening '" + filename + "' in the queue...")

            with open(filename, 'r') as queue_file:
                articlesJSON = json.load(queue_file)
                self.log("Converting JSON into dataframe...")
                new_frame = pd.io.json.json_normalize(articlesJSON)
                self.storeFrame(new_frame)

    def generateUUID(self, row):
        row['UUID'] = uuid.uuid4().hex
        return row

    def storeFrame(self, frame):
        # make sure the store is loaded
        if self.store is None: self.loadStore()
        
        # add UUIDs to it
        self.log("Generating UUIDs...")
        frame['UUID'] = ''
        frame.apply(self.generateUUID, axis=1)

        # store
        self.sendFrameToStore(frame)
        self.sendFrameToDB(frame)
    
    def sendFrameToStore(self, frame):
        self.log("Adding new entries to local store...")
        self.store = pd.concat([self.store, frame])
        self.log("Dropping duplicates...")
        self.store = self.store.drop_duplicates(['title'])
        self.saveStore()

    def sendFrameToDB(self, frame):
        pass
        
    
        
    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.IDENTIFIER)
