import logging
from logging.handlers import TimedRotatingFileHandler

class PriestLogger:

	def __init__(self):
		logHandler = TimedRotatingFileHandler("C:\\lucas\\PriestPy\\logs\\HowToPriest",when="midnight",backupCount=365)
		logFormatter = logging.Formatter('%(asctime)s - %(message)s')
		logHandler.setFormatter( logFormatter )
		self.logger = logging.getLogger( 'H2PLogger' )
		self.logger.addHandler( logHandler )
		self.logger.setLevel( logging.INFO )
	
	def log(self, message):
		self.logger.info(message.channel.name + ' - ' + message.author.name+': ' + message.content)