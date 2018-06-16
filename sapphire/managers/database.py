#***************************************************************************
#
#  File: database.py (sapphire.managers)
#  Date created: 05/29/2018
#  Date edited: 06/16/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: An interface for interacting with a mysql database
#
#***************************************************************************

import MySQLdb

import sapphire.utility
from sapphire.article import Article

class DatabaseManager:

    IDENTIFIER = "Database"

    def __init__(self):
        self.connect()
        tablesExist = self.tableCheck()
        if not tablesExist: self.createTables()

    def __del__(self):
        try: self.db.close()
        except: pass

    def connect(self):
        self.log("Connecting to database...")
        self.db = MySQLdb.connect(host=sapphire.utility.db_host, user=sapphire.utility.db_user, passwd=sapphire.utility.db_password, db=sapphire.utility.db_db)
        self.cur = self.db.cursor()
        self.log("Connection established")

    def tableCheck(self):
        self.log("Checking tables...")
        sql = '''SELECT 1 FROM Articles LIMIT 1;'''
        
        try: self.cur.execute(sql)
        except: 
            self.log("Database tables don't exist", "WARNING")
            return False
        return True

    def createTables(self):
        self.log("Creating tables...")
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
        
        result = self.tableCheck()
        if not result: self.log("Tables couldn't be created", "ERROR")
        else: self.log("Tables successfully created!")

    def storeMetadataFrame(self, frame):
        self.log("Storing metadata frame...")
        for index, row in frame.iterrows():
            
            # make sure article with this title doesn't exist yet
            checkQuery = '''SELECT COUNT(*) FROM Articles WHERE UUID = %s'''
            self.cur.execute(checkQuery, (row['UUID'],))
            if self.cur.fetchone()[0] > 0: continue 

            insertQuery = '''INSERT INTO Articles (UUID, title, description, timestamp, link, source_name, source_type, source_sub, source_explicit, meta_scrape_time, meta_scrape_identifier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            self.cur.execute(insertQuery, (row['UUID'], row['title'], row['description'], row['timestamp'], row['link'], row['source_name'], row['source_type'], row['source_sub'], row['source_explicit'], row['meta_scrape_time'], row['meta_scrape_identifier']))

        self.db.commit()
        self.log("All new metadata stored")
        self.log("Database now contains " + str(self.getArticleCount()) + " entries")

    def getArticleCount(self):
        self.cur.execute('''SELECT COUNT(*) FROM Articles''')
        return self.cur.fetchone()[0]

    def updateArticle(self, article):
        self.log("Updating article " + article.UUID + "...")
        updateQuery = '''UPDATE Articles SET 
            title = ?,
            description = ?,
            timestamp = ?,
            link = ?,
            source_name = ?,
            source_type = ?,
            source_sub = ?,
            source_explicit = ?,
            meta_scrape_time = ?,
            meta_scrape_identifier = ?,
            content = ?,
            content_scrape_time = ?,
            content_scrape_identifier = ?
            
            WHERE UUID = ?'''

        article.cur.execute(updateQuery, (article.title, article.description, article.timestamp, article.link, article.source_name, article.source_type, article.source_sub, article.source_explicit, article.meta_scrape_time, article.meta_scrape_identifier))
        self.db.commit()
        self.log("Article updated in database")

    # NOTE: returns first article without content
    def getFirstLackingArticle(self):
        findQuery = '''SELECT * FROM Articles WHERE content ''' 
    
    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.IDENTIFIER)
