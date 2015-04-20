from raygun4py import raygunprovider

class Provider(object):

	def __init__(self, app, apiKey):
		self.app = app
		self.sender = raygunprovider.RaygunSender(apiKey)

	def __call__(self, environ, start_response):
		if not self.sender:
			print >> sys.stderr, ("Raygun-Flask: Cannot send as provider not attached")

		try:
			iterable = self.app(environ, start_response)
		except Exception as e:
			self.sender.send_exception(exception=e) # TODO pass in request

			raise

		try:
			for event in iterable:
				yield event
		except Exception as e:
			self.sender.send_exception(exception=e)

			raise
		finally:
			if iterable and hasattr(iterable, 'close') and callable(iterable.close):
                try:
                    iterable.close()
                except Exception as e:
                    self.send_exception(exception=e)
