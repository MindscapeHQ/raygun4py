raygun4py
=========

.. image:: https://travis-ci.org/MindscapeHQ/raygun4py.svg?branch=master
  :target: https://travis-ci.org/MindscapeHQ/raygun4py?branch=master

.. image:: https://coveralls.io/repos/MindscapeHQ/raygun4py/badge.svg?branch=master
  :target: https://coveralls.io/r/MindscapeHQ/raygun4py?branch=master


Official Raygun provider for **Python 2.7**, **Python 3+** and **PyPy**


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

Raygun4py includes dedicated middleware implementations for Django and Flask, as well as generic WSGI frameworks (Tornado, Bottle, Ginkgo etc). These are available for both Python 2.6/2.7 and Python 3+.

Django
++++++

To configure Django to automatically send all exceptions that are raised in views to Raygun:

settings.py

.. code:: python

  MIDDLEWARE_CLASSES = (
      'raygun4py.middleware.django.Provider'
  )

  RAYGUN4PY_CONFIG = {
      'api_key': 'paste_your_api_key_here'
  }


The above configuration is the minimal required setup. The full set of options supported by the provider can be declared in the same way:

.. code:: python

  RAYGUN4PY_CONFIG = {
      'api_key': 'paste_your_api_key_here',
      'http_timeout': 10.0,
      'proxy': None,
      'before_send_callback': None,
      'grouping_key_callback': None,
      'filtered_keys': [],
      'ignored_exceptions': [],
      'transmit_global_variables': True,
      'transmit_local_variables': True,
      'transmit_environment_variables:': True,
      'userversion': "Not defined",
      'user': None
  }

Flask
+++++

.. code:: python

  from flask import Flask, current_app
  from raygun4py.middleware import flask

  app = Flask(__name__)

  flask.Provider(app, 'your_apikey').attach()

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
    raygun_wrapped_app = wsgi.Provider(wsgiapp, 'your_apikey')
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

:code:`RaygunSender` accepts a :code:`config` dict which is used to set options for the provider (the defaults are shown below):

.. code:: python

  from raygun4py import raygunprovider

  client = raygunprovider.RaygunSender('your_apikey', config={
      'http_timeout': 10.0,
      'proxy': None,
      'before_send_callback': None,
      'grouping_key_callback': None,
      'filtered_keys': [],
      'ignored_exceptions': [],
      'transmit_global_variables': True,
      'transmit_local_variables': True,
      'transmit_environment_variables:': True,
      'userversion': "Not defined",
      'user': None
  })

For the local/global/environment variables, if their options are set to False the corresponding variables will not be sent with exception payloads.

httpTimeout controls the maximum time the HTTP request can take when POSTing to the Raygun API, and is of type 'float'.

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
-------------------------

+--------------------+---------------+--------------------+
| Function           | Arguments     | Type               |
+====================+===============+====================+
| filter_keys        | keys          | List               |
+--------------------+---------------+--------------------+

If you want to filter sensitive data out of the payload that is sent to Raygun, pass in a list of keys here. Any matching keys on the top level Raygun message object, or within dictionaries on the top level Raygun message object (including dictionaries nested within dictionaries) will have their value replaced with :code:`<filtered>` - useful for passwords, credit card data etc. Supports * at the end of a key to indicate you want to filter any key that contains that key, ie foo_* will filter foo_bar, foo_qux, foo_baz etc

+------------------+---------------+--------------------+
| Function         | Arguments     | Type               |
+==================+===============+====================+
| ignore_exceptions| exceptions    | List               |
+------------------+---------------+--------------------+

Provide a list of exception types to ignore here. Any exceptions that are passed to send_exception that match a type in this list won't be sent.

+------------------+---------------+--------------------+
| Function         | Arguments     | Type               |
+==================+===============+====================+
| on_before_send   | callback      | Function           |
+------------------+---------------+--------------------+

You can mutate the candidate payload by passing in a function that accepts one parameter using this function. This allows you to completely customize what data is sent, immediately before it happens.

+------------------+---------------+--------------------+
| Function         | Arguments     | Type               |
+==================+===============+====================+
| on_grouping_key  | callback      | Function           |
+------------------+---------------+--------------------+

Pass a callback function to this method to configure custom grouping logic. The callback should take one parameter, an instance of RaygunMessage, and return a string between 1 and 100 characters in length (see 'Custom Grouping Logic' below for more details).

+----------------+---------------+--------------------+
| Function       | Arguments     | Type               |
+================+===============+====================+
| set_proxy      | host          | String             |
+                +---------------+--------------------+
|                | port          | Integer            |
+----------------+---------------+--------------------+

Call this function if your code is behind a proxy and want Raygun4py to make the HTTP request to the Raygun endpoint through it.

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

Customer data can be passed in which will be displayed in the Raygun web app. The dict you pass in should look this this:

.. code:: python

  client.set_user({
      'firstName': 'Foo',
      'fullName': 'Foo Bar',
      'email': 'foo@bar.com',
      'isAnonymous': False,
      'identifier': 'foo@bar.com'
    })

`identifier` should be whatever unique key you use to identify customers, for instance an email address. This will be used to create the count of affected customers. If you wish to anonymize it, you can generate and store a UUID or hash one or more of their unique login data fields, if available.

Custom grouping logic
---------------------

You can create custom exception grouping logic that overrides the automatic Raygun grouping by passing in a function that accepts one parameter using this function. The callback's one parameter is an instance of RaygunMessage (python[2/3]/raygunmsgs.py), and the callback should return a string.

The RaygunMessage instance contains all the error and state data that is about to be sent to the Raygun API. In your callback you can inspect this RaygunMessage, hash together the fields you want to group by, then return a string which is the grouping key.

This string needs to be between 1 and 100 characters long. If the callback is not set or the string isn't valid, the default automatic grouping will be used.

By example:

.. code:: python

    class MyClass(object):

        def my_callback(self, raygun_message):
            return raygun_message.get_error().message[:100] # Use naive message-based grouping only

        def create_raygun_and_bind_callback(self):
            sender = raygunprovider.RaygunSender('api_key')
            sender.on_grouping_key(self.my_callback)

The RaygunSender above will use the my_callback to execute custom grouping logic when an exception is raised. The above logic will use the exception message only - you'll want to use a more sophisticated approach, usually involving sanitizing or ignoring data.

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

`View the release history here <CHANGELOG.md>`_
