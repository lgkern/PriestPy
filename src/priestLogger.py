import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep

class PriestLogger:

	def __init__(self):
		logHandler = TimedRotatingFileHandler('C:\\lucas\\PriestPy\\Dropbox\\logs\\HowToPriest',when='midnight',backupCount=365)
		logFormatter = logging.Formatter('%(asctime)s - %(message)s')
		logHandler.setFormatter( logFormatter )
		self.logger = logging.getLogger( 'H2PLogger' )
		self.logger.addHandler( logHandler )
		self.logger.setLevel( logging.INFO )
		logHandler.createLock()
	
	def log(self, message):
		logHandler.acquire()
		try:
			self.logger.info(message.channel.name + ' - ' + message.author.name+': ' + message.content)
			logHandler.release()
		except:
			logHandler.release()
		
			