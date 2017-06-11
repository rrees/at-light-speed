from __future__ import absolute_import

import os

import webapp2
import jinja2

import handlers

routes = [webapp2.Route(path, handler=handler) for path, handler in [(r'/', handlers.pages.FrontPage)]]

templates = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


app = webapp2.WSGIApplication(routes, debug=True)