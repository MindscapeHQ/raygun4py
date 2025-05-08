import logging

from raygun4py import raygunprovider

API_KEY = "paste_your_api_key_here"

# Initialize a RaygunHandler from an existing RaygunSender
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
logging_handler_from_sender = raygunprovider.RaygunHandler.from_sender(
    sender, level=logging.INFO
)

# Initialize a RaygunHandler using an api_key
logging_handler_from_key = raygunprovider.RaygunHandler(API_KEY, level=logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging_handler_from_sender)
logger.addHandler(logging_handler_from_key)


def demonstrate_logging():
    # Sending an INFO log (not recommended)
    logger.info("Test INFO log sent from raygun4py")

    # Sending an ERROR log with exc_info=True
    try:
        raise ValueError("This is a test ValueError")
    except ValueError:
        logger.error(
            "Test ERROR log with exc_info=True sent from raygun4py", exc_info=True
        )

    # Sending an ERROR log without exc_info
    logger.error("Test ERROR log sent from raygun4py")

    # Using logger.exception which automatically includes exc_info
    try:
        raise RuntimeError("This is a test RuntimeError")
    except RuntimeError:
        logger.exception("Test logger.exception log sent from raygun4py")


if __name__ == "__main__":
    demonstrate_logging()
