=========
raygun4py
=========

Official Raygun provider for Python 2.6-2.7

== Installation

The easiest way to install this is as a pip package, as it is available from PyPI. From your command line, run:

```
pip install raygun4py
```

== Usage

Run raygun4py-sample/test.py to see a basic sample. You'll need to replace the API key with one of your own.

In general, after importing the module with

```python
from provider import raygunprovider
```

you'll want to provide a callback function to sys.excepthook. This will pick up all uncaught exceptions that your program throws. It needs three parameters: the type, value and traceback. In the function, create a new raygunprovider.RaygunSender, then call send() on that object, passing in the parameters.

== Troubleshooting

[Create a thread in the official support forums](http://raygun.io/forums), and we'll help you out.