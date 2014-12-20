import os
import logging

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
		user = users.get_current_user()

		if not game_key:
			webapp2.abort(404, 'Game not found')

		game = game_key.get()

		characters = models.Character.query(ancestor=game_key).fetch(limit=100)

		player_characters = [c for c in characters if c.player == user]
		other_characters = [c for c in characters if not c.player == user]

		player_character = None

		if player_characters:
			player_character = player_characters[0]

		game_owner = user in game.admins

		template_values = {
			"game": game,
			"your_character": player_character,
			"game_owner": game_owner,
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