
from google.appengine.ext import ndb

class Game(ndb.Model):
	title = ndb.StringProperty(required=True)
	description = ndb.TextProperty(required=True)
	creator = ndb.UserProperty(required=True)
	created = ndb.DateTimeProperty(auto_now_add=True)
	players = ndb.UserProperty(repeated=True)

class Character(ndb.Model):
	name = ndb.StringProperty(required=True)
	description = ndb.TextProperty()

class Message(ndb.Model):
	dt_sent = ndb.DateTimeProperty(required=True)
	dt_receive = ndb.DateTimeProperty(required=True)
	message = ndb.TextProperty(required=True)