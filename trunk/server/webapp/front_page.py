import logging

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import models
import util
from webapp import user
import writeablemodel

class FrontPage(webapp.RequestHandler):
  def get(self):
    logging.getLogger().setLevel(logging.DEBUG)

    current_user = user.GetCurrentUser(self.request)

    template_values = {
      'user' : current_user
    }
    
    if current_user:
      template_values['rooms'] = writeablemodel.UserRooms(current_user).rooms

    path = util.GetTemplate('webapp/front_page.html')
    self.response.out.write(template.render(path, template_values))

