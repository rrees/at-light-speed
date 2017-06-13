import os

import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

import models
from templates import templates

class FrontPage(webapp2.RequestHandler):
	def get(self):

		template_values = {
			"title": "Play",
		}

		template = templates.get_template('index.html')
		self.response.write(template.render(template_values))


class HomePage(webapp2.RequestHandler):
	def get(self):

		user = users.get_current_user()

		template_values = {
			"title": "Home",
			"user": user,
			"games_created": [ g for g in models.Game.query(models.Game.creator == user)],
			"games_playing": [ g for g in models.Game.query(models.Game.players.IN([user]))],
			"games_invited": [g for g in models.Game.query(models.Game.invited_emails.IN([user.email()]))],
		}

		template = templates.get_template('home.html')
		self.response.write(template.render(template_values))

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
			"title": game.title,
			"game": game,
			"your_character": player_character,
			"game_owner": game_owner,
			"other_characters": other_characters,
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

class Invitation(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()

		# TODO check the passed parameters are valid
		# TODO limit the player to single character

		urlsafe_key = self.request.POST['game_key']
		game_key = ndb.Key(urlsafe=urlsafe_key)
		game = game_key.get()

		email = self.request.POST['email']

		game.invited_emails.append(email)
		game.put()

		return webapp2.redirect('/game/' + urlsafe_key)
