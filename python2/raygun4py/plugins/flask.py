from __future__ import absolute_import

from flask.signals import got_request_exception

from raygun4py import raygunprovider

class Provider(object):

	def __init__(self, flaskApp, apiKey):
		self.flaskApp = flaskApp
		self.apiKey = apiKey
		self.flaskApp = flaskApp

		got_request_exception.connect(self.send_exception, sender=flaskApp)

		flaskApp.extensions['raygun'] = self

	def attach(self):
		if not hasattr(self.flaskApp, 'extensions'):
			self.flaskApp.extensions = {}

		self.sender = raygunprovider.RaygunSender(self.apiKey)

	def send_exception(self, *args, **kwargs):
		if not self.sender:
			print >> sys.stderr, ("Raygun-Flask: Cannot send as provider not attached")

		self.sender.send_exception()
