import handler
import models
import util

class SetTopic(handler.ZombieHandler):
  """
  Handler to set the topic for a room.
  """
  def HandleAction(self):
    topic = self.request.get('topic')
    
    room = util.GetRoomFromRequest(self.request)
    room.topic = topic
    room.put()   
    
    
  