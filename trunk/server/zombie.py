import cgi
import logging
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


import models
import util

import create_room
import get_all_messages
import get_messages
import get_room
import invite_user
import send_message
import set_topic
from webapp import front_page
from webapp import login
from webapp import show_room

logging.getLogger().setLevel(logging.DEBUG)

class MainPage(webapp.RequestHandler):
  def get(self):
    logging.getLogger().setLevel(logging.DEBUG)

    rooms = db.GqlQuery("SELECT * FROM Room")
    users = db.GqlQuery("SELECT * FROM ZombieUser")
    template_values = {
      'rooms' : rooms,
      'users' : users }

    template_path = util.GetTemplate('admin.html')
    self.response.out.write(template.render(template_path, template_values))

def main():
  application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/create_room', create_room.CreateRoom),
     ('/invite_user', invite_user.InviteUser),
     ('/set_topic', set_topic.SetTopic),
     ('/send_message', send_message.SendMessage),
     ('/get_room', get_room.GetRoom),
     ('/get_messages.xml', get_messages.GetMessages),
     ('/get_all_messages', get_all_messages.GetAllMessages),
     ('/w[/]?', front_page.FrontPage),
     ('/w/login[/]?', login.Login),
     ('/w/room/(.*)[/]?', show_room.ShowRoom)
     ],
    debug=True)
  wsgiref.handlers.CGIHandler().run(application)



if __name__ == "__main__":
  main()

