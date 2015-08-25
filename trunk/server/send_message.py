import logging

import handler
import models
import util

class SendMessage(handler.ZombieHandler):
  """
  Send a message.
  """
  def HandleAction(self):
    user = util.GetUserFromRequest(self.request)
    message_text = self.request.get('message_text')
    room = util.GetRoomFromRequest(self.request)
    util.AddUserToRoomIfNecessary(user, room)
    msg = models.Message(user=user, room=room, text=message_text)
    logging.debug('"%s" says "%s" in "%s"' % (user.phone_number, repr(message_text), room.key()))
    msg.put()


