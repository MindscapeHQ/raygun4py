import sys, os
import traceback
from provider import raygunprovider

def handle_exception(exc_type, exc_value, exc_traceback):    
    cl = raygunprovider.RaygunSender("onPbQXtZKqJX38IuN4AQKA==")
    cl.set_version("1.2")
    print cl.send(exc_type, exc_value, exc_traceback, "myclass", ["tag1", "tag2"], {"key1": 1111, "key2": 2222})

def methodone():
    methodtwo()

def methodtwo():
    raise Exception("My exception")

sys.excepthook = handle_exception

methodone()
