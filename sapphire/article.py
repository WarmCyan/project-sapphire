#***************************************************************************
#
#  File: article.py (sapphire)
#  Date created: 05/22/2018
#  Date edited: 06/16/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Contains the class for representing an article, and all 
#    its associated data
#
#***************************************************************************

# TODO: should store "version" of scrapers used?

import sapphire.utility

class Article:

    def __init__(self):
        # metadata
        self.UUID = ""
        self.title = None
        self.description = None
        self.timestamp = None               # make sure it's in UTC
        self.link = None
        self.source_name = None             # name to refer to source, ex: 'reuters'
        self.source_type = None             # 'rss', 'twitter', etc. NOTE: this may not actually be used at any point
        self.source_sub = None              # subfeed
        self.source_explicit = None         # the link used to scrape
        self.meta_scrape_time = None        # UTC
        self.meta_scrape_identifier = None

        # content
        self.content = None         
        self.content_scrape_time = None     # UTC
        self.content_scrape_identifier = None

    def populateMetadata(self, title, description, timestamp, link, source_name, source_type, source_sub, source_explicit, scrape_time, scrape_identifier):
        self.title = title
        self.description = description
        self.timestamp = utctimestamp
        self.link = link
        self.source_name = source_name
        self.source_type = source_type
        self.source_sub = source_sub
        self.source_explicit = source_explicit
        self.meta_scrape_time = scrape_time
        self.meta_scrape_identifier = scrape_identifier
        
    def populateContent(self, content, scrape_time, scrape_identifier):
        self.content = content
        self.content_scrape_time = scrape_time
        self.content_scrape_identifier = scrape_identifier

    def populateFromRow(self, row):
        self.UUID = row[0]
        self.title = row[1]
        self.description = row[2]
        self.timestamp = row[3]
        self.link = row[4]
        self.source_name = row[5]
        self.source_type = row[6]
        self.source_sub = row[7]
        self.source_explicit = row[8]
        #self.meta_scrape_time = sapphire.utility.getDT(row[9])
        self.meta_scrape_time = row[9]
        self.meta_scrape_identifier = row[10]
        self.content = row[11]
        #self.content_scrape_time = sapphire.utility.getDT(row[12])
        self.content_scrape_time = row[12]
        self.content_scrape_identifier = row[13]

    def getMetadataDictionary(self):
        dictionary = {
                "UUID": self.UUID,
                "title": self.title,
                "description": self.description,
                "timestamp": self.timestamp,
                "link": self.link,
                "source_name": self.source_name,
                "source_type": self.source_type,
                "source_sub": self.source_sub,
                "source_explicit": self.source_explicit,
                "meta_scrape_time": self.meta_scrape_time,
                "meta_scrape_identifier": self.meta_scrape_identifier
                }
        return dictionary
