3.1.4

- Fix runtime bugs involving the WSGI pipeline, a local variable accessor edge case, and a pickling old-style classes exception

3.1.3

- Guard against environment variable access exceptions as seen in Google App Engine, gevent and Jython 2.6 

3.1.2

- Guard against jsonpickle failing to serialize local/global variables

3.1.1

- Global variables are now populated from the final stacktrace frame instead of globals() as seen by the provider
- Fix log statements in referring to module-level field instead of instance-level for Py2

3.1.0

- Add on_grouping_key for custom grouping logic
- Add Django, Flask and WSGI middleware for Python 3
- Allow Django settings.py config override
- Surface more environment data (versions, interpreter location etc) for Python itself and Django/Flask
- Fix WSGI close() implementation when an exception is raised while handling a prior one (match spec)

3.0.3

- Add 'httpTimeout' option to config
- Much improved unicode handling for local variables for both py2 and py3
- Fix Django >1.8 raw_post_data bug
- Internal: upgrade from httplib to requests (urllib3); provider errors are now output to loggers instead of stdout/stderr; CI now runs on Travis in container-mode

3.0.2

- Fix UnicodeDecodeError being thrown when sending payload due to jsonpickle not pickling large binary values correctly (such as local variable bytestrings or high-codepoint unicode characters)
- Guard added for tracebacks with null method names (such as exceptions from C-wrapper libraries)

3.0.1

- Updated bdist egg to include middleware package
- Fix WSGI logging message

3.0.0

- Added functions: ignore_exceptions, filter_keys, set_proxy, on_before_send
- Added support for local variables, global variables, and environment variables
- Added CLI for testing provider
- Py2: Added web middleware (Django, Flask and WSGI)
- Py2: Added send_exception function (see below)
- send() deprecated in favor of send_exception(); see the Sending Functions in the readme for the available options



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
