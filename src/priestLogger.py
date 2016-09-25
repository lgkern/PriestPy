import logging
from logging.handlers import TimedRotatingFileHandler

class PriestLogger:

	def __init__(self):
		logHandler = TimedRotatingFileHandler("C:\\lucas\\PriestPy\\logs\\HowToPriest",when="midnight")
		logFormatter = logging.Formatter('%(asctime)s - %(message)s')
		logHandler.setFormatter( logFormatter )
		logger = logging.getLogger( 'H2PLogger' )
		logger.addHandler( logHandler )
		logger.setLevel( logging.INFO )
	
	def log(self, message):
		logger.info(message.channel.name + ' - ' + message.author.name+': ' + message.content)