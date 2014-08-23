import os

import webapp2
import jinja2

from google.appengine.api import users

import models

templates = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomePage(webapp2.RequestHandler):
	def get(self):

		user = users.get_current_user()

		template_values = {
			"user" : user,
			"games_created" : models.Game.query(models.Game.creator == user),
			"games_playing" : models.Game.query(models.Game.players.IN([user])),
		}

		template = templates.get_template('home.html')
		self.response.write(template.render(template_values))

class NewGameHandler(webapp2.RequestHandler):
	def post(self):
		for key in ['title', 'description']:
			if not key in self.request.POST.keys():
				webapp2.abort(400, 'Missing key {key}'.format(key=key))

		user = users.get_current_user()

		title = self.request.POST['title']
		description = self.request.POST['description']

		new_game = models.Game(title=title, description=description, creator=user, admins=[user], players=[user])
		new_game.put()


		return webapp2.redirect('/home')

class GameHandler(webapp2.RequestHandler):
	def get(self, key):
		template_values = {}
		template = templates.get_template('game.html')
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
	webapp2.Route(r'/home', handler=HomePage),
	webapp2.Route(r'/game/new', handler=NewGameHandler),
	webapp2.Route(r'/game/<key>', handler=GameHandler),
	], debug=True)