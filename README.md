raygun4py
=========

![travisbadge]

![coverallsbadge]

Official Raygun provider for **Python 2.7**, **Python 3+** and **PyPy**

Installation
============

The easiest way to install this is as a pip package, as it is available
from PyPI. From your command line, run:

    $ pip install raygun4py

Then import and instantiate the module:

    from raygun4py import raygunprovider

    client = raygunprovider.RaygunSender('your_apikey')

Test the installation
---------------------

From the command line, run:

    $ raygun4py test your_apikey

Replace `your_apikey` with the one listed on your Raygun dashboard. This
will cause a test exception to be generated and sent.

Usage
=====

Automatically send the current exception like this:

    try:
        raise Exception("foo")
    except:
        client.send_exception()

See [sending functions] for more ways to send.

Uncaught exception handler
--------------------------

To automatically pick up unhandled exceptions with custom logic, you can
provide a callback function to sys.excepthook:

    def handle_exception(exc_type, exc_value, exc_traceback):
        sender = raygunprovider.RaygunSender("your_apikey")
        sender.send_exception(exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

Logging
-------

You can also send exceptions using a logger:

    logger = logging.getLogger("mylogger")
    rgHandler = raygunprovider.RaygunHandler("your_apikey")
    logger.addHandler(rgHandler)

    def log_exception(exc_type, exc_value, exc_traceback):
        logger.error("An exception occurred", exc_info = (exc_type, exc_value, exc_traceback))

    sys.excepthook = log_exception

This uses the built-in `RaygunHandler`. You can provide your own handler
implementation based on that class if you need custom sending behavior.

Web frameworks
--------------

Raygun4py includes dedicated middleware implementations for Django and
Flask, as well as generic WSGI frameworks (Tornado, Bottle, Ginkgo etc).
These are available for both Python 2.6/2.7 and Python 3+.

### Django

To configure Django to automatically send all exceptions that are raised
in views to Raygun:

settings.py

    MIDDLEWARE_CLASSES = (
        'raygun4py.middleware.django.Provider'
    )

    RAYGUN4PY_CONFIG = {
        'api_key': 'paste_your_api_key_here'
    }

The above configuration is the minimal required setup. The full set of
options supported by the provider can be declared in the same way:

    RAYGUN4PY_CONFIG = {
        'api_key': 'paste_your_api_key_here',
        'http_timeout': 10.0,
        'proxy': None,
        'before_send_callback': None,
        'gr

  [travisbadge]: https://travis-ci.org/MindscapeHQ/raygun4py.svg?branch=master
  [coverallsbadge]: https://coveralls.io/repos/MindscapeHQ/raygun4py/badge.svg?branch=master
