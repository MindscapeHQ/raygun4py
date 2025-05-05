import sys

from raygun4py import raygunprovider

API_KEY = "paste_your_api_key_here"

sender = raygunprovider.RaygunSender(API_KEY)
sender.set_version("1.3")
sender.set_user(
    {
        "identifier": "example@email_or_user_id.com",
        "firstName": "John",
        "fullName": "John Smith",
        "email": "example@email_or_user_id.com",
    }
)


def handle_exception(exc_type, exc_value, exc_traceback):
    headers = {"referer": "localhost", "user-Agent": "Mozilla"}
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
    sender.send_exception(
        exc_info=(exc_type, exc_value, exc_traceback),
        tags=["tag1", "tag2"],
        userCustomData={"key1": 1111, "key2": 2222},
        request=request,
    )
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


def very_buggy_request():
    try:
        raise Exception("Test caught exception sent from raygun4py")
    except Exception:
        sender.send_exception()

    methodtwo()


def methodtwo():
    raise Exception("Test uncaught exception sent from raygun4py")


sys.excepthook = handle_exception

very_buggy_request()
