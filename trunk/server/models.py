from google.appengine.ext import db

class ZombieUser(db.Model):
  phone_number = db.StringProperty()
  phone_email_address = db.StringProperty()
  gmail_user = db.UserProperty()


QUICK_CHAT = 0


class Room(db.Model):
  members = db.ListProperty(db.Key)
  room_type = db.IntegerProperty(default=0)
  name = db.StringProperty()

class Message(db.Model):
  room = db.ReferenceProperty(Room, required=True)
  user = db.ReferenceProperty(ZombieUser, required=True)
  sent = db.DateTimeProperty(auto_now_add=True)
  text = db.StringProperty(required=True)
