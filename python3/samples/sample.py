import sys, os, urllib.request, urllib.error, urllib.parse
import traceback
from raygun4py import raygunprovider

def handle_exception(exc_type, exc_value, exc_traceback):
    cl = raygunprovider.RaygunSender("paste_your_api_key_here")
    cl.set_version("1.3")
    cl.set_user({
        'identifier': 'example@email_or_user_id.com',
        'firstName': 'John',
        'fullName': 'John Smith',
        'email': 'example@email_or_user_id.com'
    })

    # If we're handling a request in a web server environment, we can send the HTTP request data
    headers = {
        "referer": "localhost",
        "user-Agent": "Mozilla"
    }

    request = {
        "headers": headers,
        "hostName": "localhost",
        "url": "/resource",
        "httpMethod": "GET",
        "ipAddress": "127.0.0.1",
        "queryString": None,
        "form": None,
        "rawData": None,
    }

    print(cl.send_exception(exc_info=(exc_type, exc_value, exc_traceback), "myclass", ["tag1", "tag2"], {"key1": 1111, "key2": 2222}, request))

def very_buggy_request():
    methodtwo()

def methodtwo():
    raise Exception("Test exception sent from raygun4py")

sys.excepthook = handle_exception

very_buggy_request()
