import logging

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import models
import util
import writeablemodel
from webapp import user

class ShowRoom(webapp.RequestHandler):
  def get(self, key):
    logging.getLogger().setLevel(logging.DEBUG)

    room = writeablemodel.RoomResult(db.get(key))

    template_values = {
      'room' : room,
      'user' : user.GetCurrentUser(self.request)
    }

    # TODO(dbentley): right now sending a message gets you to xml.
    # It should probably take you back here.

    path = util.GetTemplate('webapp/room.html')
    self.response.out.write(template.render(path, template_values))
