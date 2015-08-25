import logging
import os
from xml.sax import saxutils

from google.appengine.ext import db

import models
import writeablemodel

class ZombieException(Exception):
  """A base class for Zombie exceptions."""
  pass


def AddUserToRoomIfNecessary(invited_user, room):
  # TODO(dbentley): make room membership unique
  # TODO(dbentley): generate system message saying user now exists
  logging.debug("Put %s in %s" % (invited_user.phone_number, str(room.key())))
  # TODO(dbentley): make this a transaction
  user_key = invited_user.key()
  if user_key not in room.members:
    room.members.append(user_key)
    room.put()

def GetUsersFromRequest(request, user_prefix=''):
  """Get user objects out of this request.

  params:
    request:  Request object.  The request object should have a parameter
      'userphone'.  Eventually we want other ways to identify a user.
      Like a user that only logs in via xmpp.  Or, y'know, to also have
      authentication.
    user_prefix:  for requests that involve multiple users, users are
      disambiguated by a string the identifies.  Thus, if user_prefix is
      'inviting_', the request object should have a parameter called
      'inviting_userphone'

  returns:
    a list of models.ZombieUser that were extracted for this request.
    If the user(s) are new, this will be a new user.

  raises:
    ZombieException if we can't find/create
  """

  users = []

  userphones = request.get(user_prefix + 'userphone', allow_multiple=True)
  if not userphones:
    raise ZombieException("Can't get user without phone number")
  for userphone in userphones:
    # Ignore empty parameter values
    if not userphone: continue
    user = GetOrCreateUserForPhoneNumber(userphone)
    users.append(user)

  return users

def GetUserFromRequest(request, user_prefix=''):
  """Variant of GetUsersFromRequest that only extracts a single user"""
  return GetUsersFromRequest(request, user_prefix)[0]


def GetOrCreateUserForPhoneNumber(phone_number):
  """Return a (possibly new) User object for phone number 'phone_number'.

  params:
    phone_number: str, the user's phone number.

  returns:
    a models.ZombieUser
  """
  user = (db.Query(models.ZombieUser).filter('phone_number =', phone_number)
          .get())
  if not user:
    logging.debug("Creating User for " + phone_number)
    user = models.ZombieUser()
    user.phone_number = phone_number
    user.put()
  return user


def GetRoomFromRequest(request):
  """
  Get the models.Room object associated with a request.

  params:
    request: a Request object with parameter 'roomkey'

  returns:
    a models.Room()
  """
  roomkey = request.get('roomkey')
  if not roomkey:
    raise ZombieException("No room specified in request.")
  room = db.get(roomkey)
  return room

def UserId(user):
  """Return a nice way to print a user.

  Eventually, use a nickname instead of a phone number. """
  return user.phone_number


def RoomId(room):
  """Return a nice way to print a room.

  Eventually use the room's topic instead of its key.
  """
  return room.key()


def GetMessagesForRoom(room):
  """
  Get the recent messages for a room.

  Params:
    room:  models.Room

  Returns:
    an iterable result set of models.Message
  """

  return q


def GetTemplate(template_name):
  """Return the path to a zombie template.

  Templates for ZombieChat are stored in the templates/ subdirectory.

  Locating that subdirectory can be a pain because python doesn't believe in
  'roots', so this function finds it relative to its directory.

  If you refactor this function into a file in a different directory, it
  will break.  That sucks.

  Returns:
    str, the path to the template file for template_name
  """
  return os.path.join(os.path.dirname(__file__),
                      'templates',
                      template_name)
