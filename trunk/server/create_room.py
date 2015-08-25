import handler
import models
import util

class CreateRoom(handler.ZombieHandler):
  """
  Handler to create a room.
  """
  def HandleAction(self):
    invited_users = util.GetUsersFromRequest(
        self.request, user_prefix='invited_')
    # You can't create a chat without yourself
    invited_users.append(util.GetUserFromRequest(self.request))

    topic = self.request.get('topic', default_value=None)
    room = models.Room(topic=topic)
    room.put()

    for invited_user in invited_users:
      util.AddUserToRoomIfNecessary(invited_user, room)
