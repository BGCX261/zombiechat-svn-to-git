import handler
import models
import util

class InviteUser(handler.ZombieHandler):
  def HandleAction(self):
    inviting_user = util.GetUserFromRequest(self.request)
    if not inviting_user:
      raise util.ZombieException('No inviting user')
    invited_users = util.GetUsersFromRequest(self.request, user_prefix='invited_')
    if not invited_users:
      raise util.ZombieException('no invited user')
    room = util.GetRoomFromRequest(self.request)
    if not room:
      raise util.ZombieException('no such room')

    for invited_user in invited_users:
      util.AddUserToRoomIfNecessary(invited_user, room)


