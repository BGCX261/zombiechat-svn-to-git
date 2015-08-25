import logging

from google.appengine.ext import db

import models

class CollectionOfRooms(object):
  """A collection of rooms selected somehow.

  members:
    rooms: a list of RoomResult's
  """
  def __init__(self, room_query):
    self.rooms = [RoomResult(r) for r in room_query.fetch(1000)]

  def Write(self, writer):
    writer.Start("rooms")
    for r in self.rooms:
      r.Write(writer)
    writer.End("rooms")


def AllRooms():
  """All the rooms."""
  return CollectionOfRooms(db.Query(models.Room))


def UserRooms(user):
  """All of the rooms that a User is in."""
  return CollectionOfRooms(db.Query(models.Room).filter('members =', user.key()))


# This needs to be in this module so that RoomResult can use it
def GenerateDescription(room):
  """Generate a user-understandable description for a room.

  Args:
    room: models.Room, the room

  Returns:
    str: the user-understandable picture of the froom
  """
  if room.name:
    return room.name

  # TODO(dbentley): something like "Chat between Foo and Bar"
  return 'Room %s' % repr(room.key().id_or_name())


class RoomResult(object):
  """Wraps a models.Room and has direct access to the various info that is spread
  around the database.

  self.room: models.Room object this wraps
  self.members:  set of ZombieUserResult's
  self.messages:  list of MessageResult's
  """
  def __init__(self, room):
    # TODO(dbentley): make these load lazily
    self.room = room
    self.description = GenerateDescription(room)

    self.members = set([ZombieUserResult(u) for u in db.get(room.members)])
    messages_query = db.Query(models.Message).filter('room =', room).order('-sent')

    self.messages = [MessageResult(m) for m in reversed(messages_query.fetch(100))]

  def Write(self, writer):
    writer.Start("room")
    writer.Content("roomkey", str(self.room.key))
    if self.room.name:
      writer.Content("name", self.room.name)
    writer.Content("description", self.description)

    writer.Start("members")

    member_index_map = {}
    member_index = 0
    for member in self.members:
      member.Write(writer)
      member_index_map[member.user_obj.phone_number] = member_index
      member_index = member_index + 1

    writer.End("members")

    writer.Start("messages")
    for message in self.messages:
      message.Write(writer, member_index_map)
    writer.End("messages")
    writer.End("room")


class ZombieUserResult(object):
  """Wraps a models.ZombieUser"""
  def __init__(self, user_obj):
    self.user_obj = user_obj
    # TODO(dbentley): support more than this when we transmit contact info
    self.display_name = user_obj.phone_number

  def Write(self, writer):
    writer.Start("member")
    writer.Content("phone", self.user_obj.phone_number)
    writer.End("member")


class MessageResult(object):
  """Wraps a models.Message"""
  def __init__(self, msg_obj):
    self.msg_obj = msg_obj
    self.user = ZombieUserResult(msg_obj.user)

  def Write(self, writer, member_index_map):
    writer.Start("message")
    writer.Content("sender", str(member_index_map[self.msg_obj.user.phone_number]))
    writer.Content("timestamp", str(self.msg_obj.sent))
    writer.Content("content", self.msg_obj.text)
    writer.End("message")
