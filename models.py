
from google.appengine.ext import ndb

class Game(ndb.Model):
	title: ndb.StringProperty(required=True)