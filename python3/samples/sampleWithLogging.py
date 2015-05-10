import sys, logging, os
from raygun4py import raygunprovider

# Hook the Raygun logging handler up:

logger = logging.getLogger("mylogger")
rgHandler = raygunprovider.RaygunHandler("paste_your_api_key_here")
logger.addHandler(rgHandler)

def log_exception(exc_type, exc_value, exc_traceback):
    logger.error("A python error occurred", exc_info=(exc_type, exc_value, exc_traceback))
    print("Logging: %s" % exc_value)

sys.excepthook = log_exception

## Example exception:

def buggyMethod():
    raise Exception("Test exception sent via built-in handler")

buggyMethod()