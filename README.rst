raygun4py
=========

Official Raygun provider for **Python 2.6/2.7** and **Python 3+**

This V2 release now contains code for both main Python versions, and should build automatically using your Python environment.


Installation
============

The easiest way to install this is as a pip package, as it is available from PyPI. From your command line, run::

    $ pip install raygun4py

Then import and instantiate the module::

    from raygun4py import raygunprovider

    client = raygunprovider.RaygunSender('your_apikey')

Usage
=====

Run python[2or3]/sample.py to see a basic implementation. You'll need to replace the API key with one of your own.

Logging
-------

You can also attach the logging handler in raygunprovider.RaygunHandler then calling a logging method in a function that is provided to sys.except hook. This requires much less setup than the above alternative.

**See sampleWithLogging.py** for an example implementation.

Uncaught exception handler
--------------------------

To automatically pick up unhandled exceptions with custom logic, you can provide a callback function to sys.excepthook. This will send uncaught exceptions that your program throws. The function should take three parameters: the type, value and traceback. In the function, create a new raygunprovider.RaygunSender, then call send() on that object, passing in the parameters.

**See sample.py for an example implementation**.

Manual sending
--------------

**Python 3**

Python 3 code can now use the new send_exception method, which simply takes an Exception object and sends it::

    try:
        raise Exception("foo")
    except Exception as e:
        client.send_exception(e)

**Python 2**

You can manually send the current exception in Python 2 by calling sys.exc_info first, and pass through the three values through to send()::

    try:
        raise StandardError("Raygun4py manual sending test")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        client.send(exc_type, exc_value, exc_traceback)

Web frameworks
--------------

If you are in a web server environment and have HTTP request details available, you can pass these and the headers through in a dictionary (as in sample.py).

Code running on Google App Engine should now be supported - you can test this locally, and has been reported working once deployed (the latter currently requires a paid account due to needed SSL support).

Documentation
=============

API
---

*class* raygunprovider.**send_exception**(exception, [className[, tags[, userCustomData[, httpRequest]]]])

This is the preferred method for manually sending from Python 3 code. The first parameter, _exception_, should be an object that inherits from Exception.

*class* raygunprovider.**send**(exc_type, exc_value, exc_traceback, [className[, tags[, userCustomData[, httpRequest]]]])

This method performs the actual sending of exception data to Raygun. This overload is available for both Python 2 and 3, but should be considered deprecated for Py3. The first three parameters are required and can be accessed using sys.exc_info (see the example under Manual Sending above).

The remaining parameters are optional:

* tags is a list of tags relating to the current context which you can define
* userCustomData is a dict containing custom key-values also of your choosing.
* httpRequest is HTTP Request data - see sample.py for the expected format of the object.

* className was used prior to v2.2.0, but is now **deprecated** and can be removed from your code. This parameter may be deleted in a future release.

Version tracking
----------------

Call `client.set_version("x.x.x.x")` to attach an app version to each message that is sent. This will be visible on the dashboard and can be used for filtering.

Affected User Tracking
--------------------

User data can be passed in which will be displayed in the Raygun web app. Call `set_user` with the following::

  client.set_user({
      'firstName': 'Foo',
      'fullName': 'Foo Bar',
      'email': 'foo@bar.com',
      'isAnonymous': False,
      'identifier': 'foo@bar.com'
    })

`identifier` should be whatever unique key you use to identify users, for instance an email address. This will be used to create the count of unique affected users. If you wish to anonymize it, you can generate and store a UUID or hash one or more of their unique login data fields, if available.

Chained exceptions
------------------

For Python 3, chained exceptions are now supported and automatically sent along with their traceback.

This occurs when an exception is raised while handling another exception - see tests_functional.py for an example.

Troubleshooting
===============

To see the HTTP response code from sending the message to raygun, `print client.send()` (as in line 27 of test.py). It will be 403 if an invalid API key was entered, and 202 if successful.

Create a thread in the official support forums at http://raygun.io/forums, and we'll help you out.

Changelog
=========

2.2.0

- Added new send_exception() method for Py3
- Added support for chained exceptions for Py3
- Automatically detect class name - this no longer needs to be provided on send() and as such this parameter is deprecated.
- Support Google App Engine by disabling multiprocessing module if not available

2.0.1

- Fix bug when exceptions received from C++ libraries

2.0.0

- Added port of library to Python 3
- Minor bugfix where OS version wasn't correctly transmitted (Environment tab in Dashboard)

1.1.3

- Fixed bug when logging with RaygunHandler attached but not passing exception data crashes program

1.1.2

- Fixed a bug where the IP address had invalid casing resulting in it being unable to be read by the API
- Fixed a bug if set_user wasn't called leading to a error
- Renamed samples and moved them to a more appropriate folder
- Added unit tests

1.1.1

- Fixed a critical bug in 1.1.0; the previous version is not recommended - use this instead.

1.1.0

- Added set_user function for unique user tracking; internal refactor to make module more pythonic

1.0.0

- **Breaking change:** changed module name to raygun4py. Now use *from raygun4py import raygunprovider*

- Added ability to send HTTP request data

0.1.2

- PyPi package
- RST file

0.1

- Initial release; basic message creation and transport functionality
