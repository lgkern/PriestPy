import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep

class PriestLogger:

	def __init__(self):
		self.logHandler = TimedRotatingFileHandler('C:\\lucas\\PriestPy\\Dropbox\\logs\\HowToPriest',when='midnight',backupCount=365)
		self.logFormatter = logging.Formatter('%(asctime)s - %(message)s')
		self.logHandler.setFormatter( self.logFormatter )
		self.logger = logging.getLogger( 'H2PLogger' )
		self.logger.addHandler( self.logHandler )
		self.logger.setLevel( logging.INFO )
		self.logHandler.createLock()
	
	def log(self, message):
		self.logHandler.acquire()
		try:
			self.logger.info(message.channel.name + ' - ' + message.author.name+': ' + message.content)
			self.logHandler.release()
		except:
			self.logHandler.release()
		
			