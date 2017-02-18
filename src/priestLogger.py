# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep
import string

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
    
    def log(self, message):
        self.logHandler.acquire()
        channelName = message.channel.name if not message.channel.is_private else 'PM'
        self.logger.info(channelName + ' - ' + message.author.name+': ' + ''.join(filter(lambda x: x in self.printable, message.content)))
        self.logHandler.release()
      
            