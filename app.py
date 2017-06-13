import os
import logging

import webapp2
import jinja2

import handlers


routes = [webapp2.Route(path, handler=handler) for path, handler in [
	(r'/home', handlers.pages.HomePage),
	(r'/game/new', handlers.forms.NewGame),
	(r'/game/character', handlers.pages.CharacterHandler),
	(r'/game/invite/player', handlers.pages.Invitation),
	(r'/game/<key>', handlers.pages.GameHandler),
	]]

app = webapp2.WSGIApplication(routes, debug=True)