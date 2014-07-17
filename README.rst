raygun4py
=========

Official Raygun provider for **Python 2.6/2.7** and **Python 3+**

This V2 release now contains code for both main Python versions, and should build automatically using your Python environment.


Installation
============

The easiest way to install this is as a pip package, as it is available from PyPI. From your command line, run::

  pip install raygun4py

Usage
=====

Run python[2 or 3]/sample.py to see a basic sample. You'll need to replace the API key with one of your own.

In your code, after importing the module with::


    from raygun4py import raygunprovider


you'll want to provide a callback function to sys.excepthook. This will pick up all uncaught exceptions that your program throws. It needs three parameters: the type, value and traceback. In the function, create a new raygunprovider.RaygunSender, then call send() on that object, passing in the parameters.

You can also attach the logging handler in raygunprovider.RaygunHandler then calling a logging method in a function that is provided to sys.except hook. This requires much less setup than the above alternative. **See sampleWithLogging.py**.

* If you are in a web server environment and have HTTP request details available, you can pass these and the headers through in a dictionary (as in sample.py).

Documentation
=============

API
---

*class* raygunprovider.**send**(exc_type, exc_value, exc_traceback, [className[, tags[, userCustomData[, httpRequest]]]])

This method performs the actual sending of exception data to Raygun. The first three parameters are required and can be accessed using sys.exc_info()::


    try:
       # LOC which raises an exception
    except:
       exc_type, exc_value, exc_traceback = sys.exc_info()
       client.send(exc_type, exc_value, exc_traceback)


The remaining parameters are optional:

* className is the name of the class
* tags is a list of tags relating to the current context which you can define
* userCustomData is a dict containing custom key-values also of your choosing.
* httpRequest is HTTP Request data - see sample.py for the expected format of the object.

Version tracking
----------------

Call `client.set_version("x.x.x.x")` to attach an app version to each message that is sent. This will be visible on the dashboard and can be used for filtering.

Unique User Tracking
--------------------

New in 2.1: More user data can now be passed in which will be displayed in the Raygun web app. Call `set_user` with the following::

  client.set_user({
      'firstName': 'Foo',
      'fullName': 'Foo Bar',
      'email': 'foo@bar.com',
      'isAnonymous': False,
      'identifier': 'foo@bar.com'
    })

`identifier` should be whatever unique key you use to identify users, for instance an email address. This will be used to create the count of unique affected users. If you wish to anonymize it, you can generate and store a UUID or hash one or more of their unique login data fields, if available.

Troubleshooting
===============

To see the HTTP response code from sending the message to raygun, `print client.send()` (as in line 27 of test.py). It will be 403 if an invalid API key was entered, and 202 if successful.

Create a thread in the official support forums at http://raygun.io/forums, and we'll help you out.

Changelog
=========

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
