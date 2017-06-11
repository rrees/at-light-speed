from __future__ import absolute_import

import os

import webapp2
import jinja2

import handlers

routes = [webapp2.Route(path, handler=handler) for path, handler in [(r'/', handlers.pages.FrontPage)]]

app = webapp2.WSGIApplication(routes, debug=True)