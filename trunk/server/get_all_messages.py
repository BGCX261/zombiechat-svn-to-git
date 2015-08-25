import handler

class GetAllMessages(handler.ZombieHandler):
  """Get all the messages for all the rooms a user is in.
  """
  def HandleRequest(self):
    result = writeablemodel.AllRooms()
    result.Write(xmlwriter.XmlWriter(self.response))
