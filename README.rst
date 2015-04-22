raygun4py
=========

.. image:: https://travis-ci.org/MindscapeHQ/raygun4py.svg?branch=vnext
  :target: https://travis-ci.org/MindscapeHQ/raygun4py?branch=vnext

.. image:: https://coveralls.io/repos/MindscapeHQ/raygun4py/badge.svg?branch=vnext
  :target: https://coveralls.io/r/MindscapeHQ/raygun4py?branch=vnext


Official Raygun provider for **Python 2.6/2.7**, **Python 3+** and **PyPy**


Installation
============

The easiest way to install this is as a pip package, as it is available from PyPI. From your command line, run::

    $ pip install raygun4py

Then import and instantiate the module::

    from raygun4py import raygunprovider

    client = raygunprovider.RaygunSender('your_apikey')

Usage
=====

Automatically send the current exception like this::

    try:
        raise Exception("foo")
    except:
        client.send_exception()

See `sending functions`_ for more ways to send.



Uncaught exception handler
--------------------------

To automatically pick up unhandled exceptions with custom logic, you can provide a callback function to sys.excepthook::

  def handle_exception(exc_type, exc_value, exc_traceback):
      sender = raygunprovider.RaygunSender("your_apikey")
      sender.send_exception(exc_info=(exc_type, exc_value, exc_traceback))

  sys.excepthook = handle_exception

Logging
-------

You can also attach the logging handler in raygunprovider.RaygunHandler then calling a logging method in a function that is provided to sys.except hook. See :code:`sampleWithLogging.py` for an example implementation.


Web frameworks
--------------

If you are in a web server environment and have HTTP request details available, you can pass these and the headers through in a dictionary (as in sample.py).
l
Code running on Google App Engine should now be supported - you can test this locally, and has been reported working once deployed (the latter currently requires a paid account due to needed SSL support).

Documentation
=============

Sending functions
-----------------

+----------------+---------------+--------------------+
| Function       | Arguments     | Type               |
+================+===============+====================+
| send_exception | exception     | Exception          |
+                +---------------+--------------------+
|                | exc_info      | 3-tuple            |
+                +---------------+--------------------+
|                | tags          | List               |
+                +---------------+--------------------+
|                | userCustomData| Dict               |
+                +---------------+--------------------+
|                | httpRequest   | Dict               |
+----------------+---------------+--------------------+

This is the preferred method for sending exceptions. Call this function from within a catch block to send the current exception to Raygun::

  # Automatically gets the current exception
  httpResult = client.send_exception()

  # Uses the supplied sys.exc_info() tuple
  httpResult = client.send_exception(exc_info=sys.exc_info())

  # Uses a supplied Exception object
  httpResult = client.send_exception(exception=exception)

  # Send tags, custom data and an HTTP request object
  httpResult = client.send_exception(tags=[], userCustomData={}, request={})

All the arguments in the above table are optional:

* :code:`exception` should be a subclass of type Exception. Pass this in if you want to manually transmit an exception object to Raygun.
* :code:`exc_info` should be the 3-tuple returned from :code:`sys.exc_info()`. Pass this tuple in if you wish to use it in other code aside from send_exception().

send_exception also supports the following extra data parameters:

* :code:`tags` is a list of tags relating to the current context which you can define.
* :code:`userCustomData` is a dict containing custom key-values also of your choosing.
* :code:`httpRequest` is HTTP Request data - see `sample.py` for the expected format of the object.

Data functions
--------------

+----------------+---------------+--------------------+
| Function       | Arguments     | Type               |
+================+===============+====================+
| set_version    | version       | String             |
+----------------+---------------+--------------------+

Call this to attach a SemVer version to each message that is sent. This will be visible on the dashboard and can be used to filter exceptions to a particular version, deployment tracking etc.

+----------------+---------------+--------------------+
| Function       | Arguments     | Type               |
+================+===============+====================+
| set_user       | user_info     | Dict               |
+----------------+---------------+--------------------+

User data can be passed in which will be displayed in the Raygun web app. The dict you pass in should look this this::

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

`View the release history here <CHANGELOG.rst>`_