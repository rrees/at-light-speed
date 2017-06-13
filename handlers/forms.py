import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

import models
from templates import templates


class NewGame(webapp2.RequestHandler):
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