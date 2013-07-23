import sys, logging, os
from raygun4py import raygunprovider

logger = logging.getLogger("mylogger")

rgHandler = raygunprovider.RaygunHandler("{{Place your API key here}}")

logger.addHandler(rgHandler)

def log_exception(exc_type, exc_value, exc_traceback):
    print "Logging: %s" % exc_value
    logger.error("A python error occurred", exc_info = (exc_type, exc_value, exc_traceback))

sys.excepthook = log_exception

def firstMethod():
	secondMethod()

def secondMethod():
	raise StandardError("A test exception")	

firstMethod()