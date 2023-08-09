import logging

from raygun4py import raygunprovider

sender = raygunprovider.RaygunSender("fbbUf14bTUapOz1YAvURw")
sender.set_version("1.3")
sender.set_user({
    'identifier': 'example@email_or_user_id.com',
    'firstName': 'John',
    'fullName': 'John Smith',
    'email': 'example@email_or_user_id.com'
})
logging_handler = raygunprovider.RaygunHandler.from_sender(
    sender, level=logging.INFO)

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(logging_handler)


def very_buggy_request():
    logging.info("Test error log sent from raygun4py")


def methodtwo():
    raise Exception("Test exception sent from raygun4py")


very_buggy_request()
