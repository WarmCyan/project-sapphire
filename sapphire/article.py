#***************************************************************************
#
#  File: article.py
#  Date created: 05/22/2018
#  Date edited: 05/22/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Contains the class for representing an article, and all 
#    its associated data
#
#***************************************************************************

# TODO: should store "version" of scrapers used?

class Article:

    def __init__(self):
        self.title = None
        self.description = None
        self.timestamp = None               # make sure it's in UTC
        self.link = None
        self.source_name = None             # name to refer to source, ex: 'reuters'
        self.source_type = None             # 'rss', 'twitter', etc. NOTE: this may not actually be used at any point
        self.source_sub = None              # sub category name of the source, in case a source has multiple
        self.source_explicit = None         # the link used to scrape
        self.content = None         
        self.meta_scrape_time = None        # UTC
        self.content_scrape_time = None     # UTC

    def populateMetadata(self, title, description, timestamp, link, source_name, source_type, source_sub, source_explicit, scrape_time):
        self.title = title
        self.description = description
        self.timestamp = utctimestamp
        self.link = link
        self.source_name = source_name
        self.source_type = source_type
        self.source_sub = source_sub
        self.source_explicit = source_explicit
        self.meta_scrape_time = scrape_time
        
    def populateContent(self, content, scrape_time):
        self.content = content
        self.content_scrape_time = scrape_time
