raygun4py
=========

Official Raygun provider for Python 2.6-2.7

Installation
------------

The easiest way to install this is as a pip package, as it is available from PyPI. From your command line, run::

  pip install raygun4py

Usage
-----
Run raygun4py-sample/test.py to see a basic sample. You'll need to replace the API key with one of your own.

In general, after importing the module with::


    from raygun4py import raygunprovider


you'll want to provide a callback function to sys.excepthook. This will pick up all uncaught exceptions that your program throws. It needs three parameters: the type, value and traceback. In the function, create a new raygunprovider.RaygunSender, then call send() on that object, passing in the parameters.

You can also attach the logging handler in raygunprovider.RaygunHandler then calling a logging method in a function that is provided to sys.except hook. This requires much less setup than the above alternative. **See testWithLogging.py**.

* If you are in a web server environment and have HTTP request details available, you can pass these and the headers through in a dictionary (as in test.py).

Troubleshooting
---------------

To see the HTTP response code from sending the message to raygun, `print client.send()` (as in line 27 of test.py). It will be 403 if an invalid API key was entered, and 202 if successful.

Create a thread in the official support forums at http://raygun.io/forums, and we'll help you out.

Changelog
---------

1.0.0

- **Breaking change:** changed module name to raygun4py. Now use *from raygun4py import raygunprovider*

- Added ability to send HTTP request data

0.1.2

- PyPi package
- RST file

0.1

- Initial release; basic message creation and transport functionality