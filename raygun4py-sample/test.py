import sys, os
import traceback
from provider import raygunprovider

def handle_exception(exc_type, exc_value, exc_traceback):    
    cl = raygunprovider.RaygunSender("onPbQXtZKqJX38IuN4AQKA==")
    cl.set_version("1.2")
    print cl.send(exc_type, exc_value, exc_traceback)

def methodone():
    methodtwo()

def methodtwo():
    raise Exception("My exception")

sys.excepthook = handle_exception

methodone()
