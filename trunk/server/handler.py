import logging
import util
import xmlwriter

from google.appengine.ext import webapp

import writeablemodel

class ZombieHandler(webapp.RequestHandler):
  """Common handler base class.

  Subclasses should implement HandleRequest (invoked in the case of either
  GET or POST requests).

  TODOs:
  - Universal response should probably go here
  - Authenticate users
  - Action tokens for state-change requests
  """
  def post(self):
    logging.getLogger().setLevel(logging.DEBUG)
    self.response.headers['Content-Type'] = 'text/xml'
    self.HandleAction()
    self.GetMessages()

  def get(self):
    logging.getLogger().setLevel(logging.DEBUG)
    self.response.headers['Content-Type'] = 'text/xml'
    self.HandleRequest()

  def GetMessages(self):
    user = util.GetUserFromRequest(self.request)
    result = writeablemodel.UserRooms(user)
    result.Write(xmlwriter.XmlWriter(self.response))


