#***************************************************************************
#
#  File: rss.py (sapphire.managers)
#  Date created: 05/24/2018
#  Date edited: 05/24/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Handles running all of the various rss scrapers
#
#***************************************************************************

import time

import sapphire.utility

from sapphire.scrapers import reuters_v1


class RSSManager:

    IDENTIFIER = "RSS Manager"

    reuters_ver = "v1"

    sources_list = {"reuters": None} # should be filled with the requiste RSS Scraper class

    def __init__(self):
        self.sources_list["reuters"] = reuters_v1.RSSScraper()

    # NOTE: scrapes ALL subfeeds
    def scrapeSource(self, source):
        self.log("Initiating scraper for source '" + source + "'...")
        
        scraper = self.sources_list[source]
        subfeeds = scraper.getSubfeeds()
        self.log("Scraper identifier: '" + scraper.getIdentifier() + "'")
        
        articles = []
        
        for subfeed in subfeeds:
            self.log("Running " + source + " scraper on subfeed '" + subfeed + "'...")
            newarticles = scraper.run(subfeed)
            articles.extend(newarticles)
            time.sleep(1)

        self.log("All " + source + " RSS subfeeds scraped")

        return articles


    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.IDENTIFIER)
        
        
