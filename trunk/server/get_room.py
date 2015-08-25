import logging

from google.appengine.ext import db

import handler
import models
import util
import xmlwriter
import writeablemodel

class GetRoom(handler.ZombieHandler):
  """Display one room's info.

  Strictly speaking, our API doesn't need this.  But it's easier than
    get_messages, so is probably a good milestone to have for debugging.
  """
  def HandleRequest(self):
    room = util.GetRoomFromRequest(self.request)
    logging.debug('Fetching room %s' % room.key())
    room_result = writeablemodel.RoomResult(room)
    room_result.Write(xmlwriter.XmlWriter(self.response))


