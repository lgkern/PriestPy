# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep
import string
import sqlite3
from discord import TextChannel
from os import path

class PriestLogger:

    def __init__(self):
        self.logHandler = TimedRotatingFileHandler('~\\logs\\HowToPriest',when='midnight',backupCount=365)
        self.logFormatter = logging.Formatter('%(asctime)s - %(message)s')
        self.logHandler.setFormatter( self.logFormatter )
        self.logger = logging.getLogger( 'H2PLogger' )
        self.logger.addHandler( self.logHandler )
        self.logger.setLevel( logging.INFO )
        self.logHandler.createLock()
        self.printable = set(string.printable)
        self.dbFile = 'priestPy.sqlite'
        self.conn = None
        self.c = None
        
    # SQLite options   
     #   if not path.exists(self.dbFile):
       #     self.createDb()
        
    def log(self, message):
        self.logHandler.acquire()
        print(type(message.channel))
        channelName = message.channel.name if isinstance(message.channel, TextChannel) else 'PM'
        self.logger.info(channelName + ' - ' + message.author.name+'('+str(message.author.id)+') : (' + str(message.id) + ') '+ ''.join(filter(lambda x: x in self.printable, message.content)))
        self.logHandler.release()
      
    def createDb(self):
        c = self.cursor()
        c.execute("CREATE TABLE messages ('id' INTEGER PRIMARY KEY)")
        c.execute("ALTER TABLE messages ADD COLUMN 'timestamp' INTEGER NOT NULL DEFAULT 0")
        c.execute("ALTER TABLE messages ADD COLUMN 'channel_id' INTEGER NOT NULL DEFAULT 0")
        c.execute("ALTER TABLE messages ADD COLUMN 'channel_name' TEXT NOT NULL DEFAULT ''")
        c.execute("ALTER TABLE messages ADD COLUMN 'author_id' INTEGER NOT NULL DEFAULT 0")
        c.execute("ALTER TABLE messages ADD COLUMN 'author_tag' TEXT NOT NULL DEFAULT 0")
        c.execute("ALTER TABLE messages ADD COLUMN 'author_alias' TEXT NOT NULL DEFAULT ''")
        c.execute("ALTER TABLE messages ADD COLUMN 'message' TEXT NOT NULL DEFAULT ''")
        self.commit()
    
    def cursor(self):
        if not self.c:
            self.conn = sqlite3.connect(self.dbFile)
            self.c = self.conn.cursor()
        return self.c
     
    def commit(self):
        self.conn.commit()