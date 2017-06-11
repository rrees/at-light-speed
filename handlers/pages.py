import os

import webapp2
import jinja2

from templates import templates

class FrontPage(webapp2.RequestHandler):
	def get(self):

		template_values = {}

		template = templates.get_template('index.html')
		self.response.write(template.render(template_values))