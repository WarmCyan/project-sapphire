#***************************************************************************
#
#  File: database.py (sapphire.managers)
#  Date created: 05/29/2018
#  Date edited: 05/29/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: An interface for interacting with a mysql database
#
#***************************************************************************

import MySQLdb

import sapphire.utility

class DatabaseManager:

    IDENTIFIER = "Database"

    def __init__(self):
        self.connect()

    def __del__(self):
        try: self.db.close()
        except: pass

    def connect(self):
        self.log("Connecting to database...")
        self.db = MySQLdb.connect(host=sapphire.utility.db_host, user=sapphire.utility.db_user, passwd=sapphire.utility.db_password, db=sapphire.utility.db_db)
        self.cur = self.db.cursor()
        self.log("Connection established")

    def createTables(self):
        sql = '''CREATE TABLE Articles (
            UUID char(32) primary key,
            title varchar(256),
            description text,
            timestamp datetime,
            link varchar(256),
            source_name varchar(30),
            source_type varchar(10),
            source_sub varchar(30),
            source_explicit varchar(256),
            meta_scrape_time datetime,
            meta_scrape_identifier varchar(40),
            content text,
            content_scrape_time datetime,
            content_scrape_identifier varchar(40)
        );'''
        
        self.cur.execute(sql)

        
    
    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.IDENTIFIER)
