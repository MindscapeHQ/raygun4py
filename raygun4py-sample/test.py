import sys, os, urllib2
import traceback
from provider import raygunprovider

def handle_exception(exc_type, exc_value, exc_traceback):
    cl = raygunprovider.RaygunSender("onPbQXtZKqJX38IuN4AQKA==") # Place your API key here
    cl.set_version("1.2")

    # If we're handling a request in a web server environment, we can send the HTTP request data 
    request = {}
    request['hostName'] = "localhost"
    request['url'] = "/resource"
    request['httpMethod'] = "GET"
    request['ipAddress'] = "127.0.0.1"
    request['queryString'] = None
    request['form'] = None
    request['rawData'] = None

    headers = {}

    headers['referer'] = "Me"
    headers['user-Agent'] = "Mozilla bleg"

    request['headers'] = headers


    print cl.send(exc_type, exc_value, exc_traceback, "myclass", ["tag1", "tag2"], {"key1": 1111, "key2": 2222}, request)

def very_buggy_request():
    methodtwo()

def methodtwo():
    urllib2.urlopen("gopher://test.edu/resource").read()

sys.excepthook = handle_exception

very_buggy_request()
