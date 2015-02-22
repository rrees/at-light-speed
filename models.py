
from google.appengine.ext import ndb

class Game(ndb.Model):
	title = ndb.StringProperty(required=True)
	description = ndb.TextProperty(required=True)
	creator = ndb.UserProperty(required=True)
	created = ndb.DateTimeProperty(auto_now_add=True)
	admins = ndb.UserProperty(repeated=True)
	players = ndb.UserProperty(repeated=True)
	invited_emails = ndb.StringProperty(repeated=True)

class Character(ndb.Model):
	player = ndb.UserProperty(required=True)
	name = ndb.StringProperty(required=True)
	description = ndb.TextProperty()

class Message(ndb.Model):
	sent = ndb.DateTimeProperty(required=True)
	receive = ndb.DateTimeProperty(required=True)
	message = ndb.TextProperty(required=True)
	sender = ndb.KeyProperty(required=True)
	recipient = ndb.KeyProperty(required=True)