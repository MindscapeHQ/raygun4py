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

Then import and instantiate the module:

.. code:: python

    from raygun4py import raygunprovider

    client = raygunprovider.RaygunSender('your_apikey')

Test the installation
------------------------

From the command line, run::

  $ raygun4py test your_apikey

Replace :code:`your_apikey` with the one listed on your Raygun dashboard. This will cause a test exception to be generated and sent.

Usage
=====

Automatically send the current exception like this:

.. code:: python

    try:
        raise Exception("foo")
    except:
        client.send_exception()

See `sending functions`_ for more ways to send.


Uncaught exception handler
--------------------------

To automatically pick up unhandled exceptions with custom logic, you can provide a callback function to sys.excepthook:

.. code:: python

  def handle_exception(exc_type, exc_value, exc_traceback):
      sender = raygunprovider.RaygunSender("your_apikey")
      sender.send_exception(exc_info=(exc_type, exc_value, exc_traceback))

  sys.excepthook = handle_exception

Logging
-------

You can also send exceptions using a logger:

.. code:: python

  logger = logging.getLogger("mylogger")
  rgHandler = raygunprovider.RaygunHandler("your_apikey")
  logger.addHandler(rgHandler)

  def log_exception(exc_type, exc_value, exc_traceback):
      logger.error("An exception occurred", exc_info = (exc_type, exc_value, exc_traceback))

  sys.excepthook = log_exception

This uses the built-in :code:`RaygunHandler`. You can provide your own handler implementation based on that class if you need custom sending behavior.


Web frameworks
--------------

Python 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raygun4py in Python 2.x includes several middleware implementations for various frameworks to enable reporting out of the box:

Django
++++++

settings.py

.. code:: python

  MIDDLEWARE_CLASSES = (
      'raygun4py.middleware.django.Provider'
  )

  RAYGUN4PY_API_KEY = 'your_apikey'
  RAYGUN4PY_CONFIG = {'ignoredExceptions': ['CustomException']}

Exceptions that occur in views will be automatically sent to Raygun.


Flask
+++++

.. code:: python

  from flask import Flask, current_app
  from raygun4py.middleware import flask

  app = Flask(__name__)

  flask.Provider(app, 'your_apikey', {'ignoredExceptions': ['CustomException']}).attach()

WSGI
++++

An example using **Tornado**, which will pick up exceptions that occur in the WSGI pipeline:

.. code:: python

  from raygun4py.middleware import wsgi

  class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
        raise Exception('init')

  def main():
    settings = {
        'default_handler_class': MainHandler
    }

    application = tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)

    wsgiapp = tornado.wsgi.WSGIAdapter(application)
    raygun_wrapped_app = wsgi.Provider(wsgiapp, 'your_apikey'. {'ignoredException': ['CustomException']})
    server = wsgiref.simple_server.make_server('', 8888, raygun_wrapped_app)
    server.serve_forever()

Note that many frameworks (tornado, pryramid, gevent et al) will swallow exceptions that occur within their domain.

Let us know if we're missing middleware for your framework, or feel free to submit a pull request.

Attaching raw HTTP request data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are in a web server environment and have HTTP request details available, you can pass these and the headers through in a dictionary (see :code:`sample.py`).

Code running on Google App Engine should now be supported - you can test this locally, and has been reported working once deployed (the latter currently requires a paid account due to needed SSL support).

Documentation
=============

Initialization options
----------------------

:code:`RaygunSender` accepts a :code:`config` dict which is used to set options for the provider:

.. code:: python

  from raygun4py import raygunprovider

  client = raygunprovider.RaygunSender('your_apikey', config={
    'transmitLocalVariables': True,
    'transmitGlobalVariables': True
  })

If either of these are set to False, the corresponding variables will not be sent with exception payloads. Both default to True.

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

**All parameters are optional.**

Call this function from within a catch block to send the current exception to Raygun:

.. code:: python

  # Automatically gets the current exception
  httpResult = client.send_exception()

  # Uses the supplied sys.exc_info() tuple
  httpResult = client.send_exception(exc_info=sys.exc_info())

  # Uses a supplied Exception object
  httpResult = client.send_exception(exception=exception)

  # Send tags, custom data and an HTTP request object
  httpResult = client.send_exception(tags=[], userCustomData={}, request={})

You can pass in **either** of these two exception params:

* :code:`exception` should be a subclass of type Exception. Pass this in if you want to manually transmit an exception object to Raygun.
* :code:`exc_info` should be the 3-tuple returned from :code:`sys.exc_info()`. Pass this tuple in if you wish to use it in other code aside from send_exception().

send_exception also supports the following extra data parameters:

* :code:`tags` is a list of tags relating to the current context which you can define.
* :code:`userCustomData` is a dict containing custom key-values also of your choosing.
* :code:`httpRequest` is HTTP Request data - see `sample.py` for the expected format of the object.

Config and data functions
--------------

Raygun supports passing a dictionary of variables that can be later used to customize RaygunSender. It's very handful if you are using one of our built-in middlewares.

+------------------+---------------+--------------------+-----------------------------+
| Function         | Arguments     | Type               | Configuration variable name |
+==================+===============+====================+=============================+
| filter_keys      | keys          | List               | filteredKeys                |
+------------------+---------------+--------------------+-----------------------------+

If you want to filter sensitive data out of the payload that is sent to Raygun, pass in a list of keys here. Any matching keys in the payload will have their value replaced with :code:`<filtered>` - useful for passwords, credit card data etc.

+------------------+---------------+--------------------+-----------------------------+
| Function         | Arguments     | Type               | Configuration variable name |
+==================+===============+====================+=============================+
| ignore_exceptions| exceptions    | List               | ignoredExceptions           |
+------------------+---------------+--------------------+-----------------------------+

Provide a list of exception types to ignore here. Any exceptions that are passed to send_exception that match a type in this list won't be sent.

+------------------+---------------+--------------------+-----------------------------+
| Function         | Arguments     | Type               | Configuration variable name |
+==================+===============+====================+=============================+
| on_before_send   | callback      | Function           | beforeSendCallback          |
+------------------+---------------+--------------------+-----------------------------+

You can mutate the candidate payload by passing in a function that accepts one parameter using this function. This allows you to completely customize what data is sent, immediately before it happens.
Raygun4py passes details of the message. Example usage:

.. code:: python

  import os

  def add_environment_detail(message):
      '''Hook ads information about machine type 
      message.update({
        'NodeType': os.environ.get('NodeType')
      })
      return message

  client = raygunprovider.RaygunSender('your_apikey', {'beforeSendCallback': add_environment_detail})

+----------------+---------------+--------------------+-----------------------------+
| Function       | Arguments     | Type               | Configuration variable name |
+================+===============+====================+=============================+
| set_proxy      | host          | String             | proxy                       |
+                +---------------+--------------------+                             +
|                | port          | Integer            |                             |
+----------------+---------------+--------------------+-----------------------------+

Call this function if your code is behind a proxy and want Raygun4py to make the HTTP request to the Raygun endpoint through it.

+----------------+---------------+--------------------+-----------------------------+
| Function       | Arguments     | Type               | Configuration variable name |
+================+===============+====================+=============================+
| set_version    | version       | String             | filteredKeys                |
+----------------+---------------+--------------------+-----------------------------+

Call this to attach a SemVer version to each message that is sent. This will be visible on the dashboard and can be used to filter exceptions to a particular version, deployment tracking etc.

+----------------+---------------+--------------------+
| Function       | Arguments     | Type               |
+================+===============+====================+
| set_user       | user_info     | Dict               |
+----------------+---------------+--------------------+

User data can be passed in which will be displayed in the Raygun web app. The dict you pass in should look this this:

.. code:: python

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

For Python 3, chained exceptions are supported and automatically sent along with their traceback.

This occurs when an exception is raised while handling another exception - see tests_functional.py for an example.

Troubleshooting
===============

To see the HTTP response code from sending the message to raygun, `print client.send()` (as in line 27 of test.py). It will be 403 if an invalid API key was entered, and 202 if successful.

Create a thread in the official support forums at http://raygun.io/forums, and we'll help you out.

Changelog
=========

`View the release history here <CHANGELOG.rst>`_