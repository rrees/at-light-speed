import webapp2

class FrontPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello world')

app = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=FrontPage),
	], debug=True)