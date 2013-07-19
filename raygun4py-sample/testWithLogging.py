import sys, logging, os
from provider import raygunprovider

logger = logging.getLogger("mylogger")

rgHandler = raygunprovider.RaygunHandler("{{Place your API key here}}")
ch = logging.StreamHandler()

handler = logger.addHandler(rgHandler)
logger.addHandler(ch)

def log_exception(exc_type, exc_value, exc_traceback):
    logger.error("A python error occurred", exc_info = (exc_type, exc_value, exc_traceback))

sys.excepthook = log_exception

def firstMethod():
	secondMethod()

def secondMethod():
	raise StandardError("A test exception")	

firstMethod()