import os

import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

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
		game_key = ndb.Key(urlsafe=key)

		if not game_key:
			webapp2.abort(404, 'Game not found')

		player_character = models.Character.query(ancestor=game_key).get()

		template_values = {
			"game" : game_key.get(),
			"your_character" : player_character,
		}
		template = templates.get_template('game.html')
		self.response.write(template.render(template_values))

class CharacterHandler(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()

		# TODO check the passed parameters are valid
		# TODO limit the player to single character

		urlsafe_key = self.request.POST['game_key']
		game_key = ndb.Key(urlsafe=urlsafe_key)
		game = game_key.get()

		name = self.request.POST['name']
		description = self.request.POST['description']

		new_character = models.Character(parent=game_key, player=user, name=name)

		if description and len(description) > 0:
			new_character.description = description

		new_character.put()

		return webapp2.redirect('/game/' + urlsafe_key)

app = webapp2.WSGIApplication([
	webapp2.Route(r'/home', handler=HomePage),
	webapp2.Route(r'/game/new', handler=NewGameHandler),
	webapp2.Route(r'/game/character', handler=CharacterHandler),
	webapp2.Route(r'/game/<key>', handler=GameHandler),
	], debug=True)