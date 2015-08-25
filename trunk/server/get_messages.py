import handler

class GetMessages(handler.ZombieHandler):
  """Get all the messages for all the rooms a user is in.
  """
  def HandleRequest(self):
    self.GetMessages()
