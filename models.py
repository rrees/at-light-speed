
from google.appengine.ext import ndb

class Game(ndb.Model):
	title = ndb.StringProperty(required=True)
	description = ndb.TextProperty()

class Character(ndb.Model):
	name = ndb.StringProperty(required=True)
	description = ndb.TextProperty()

class Message(ndb.Model):
	dt_sent = ndb.DateTimeProperty(required=True)
	dt_receive = ndb.DateTimeProperty(required=True)
	message = ndb.TextProperty(required=True)