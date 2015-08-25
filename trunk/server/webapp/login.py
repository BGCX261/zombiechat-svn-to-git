import base64
import Cookie
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import util
from webapp import user

COOKIE_OFFSET = 12 # To strip off "Set-Cookie: "

class Login(webapp.RequestHandler):
  def post(self):
    logging.getLogger().setLevel(logging.DEBUG)
    # TODO(dbentley): secure this
    # Get the new user param from the request
    new_user = None
    try:
      # Specifically, don't get it from the cookies, because the point is to
      # get rid of what's in the cookies
      new_user = util.GetUserFromRequest(self.request)
    except util.ZombieException:
      pass

    # Set the cookie
    if new_user:
      cookie = Cookie.SimpleCookie()
      cookie[user.COOKIE_NAME] = str(base64.b64encode(new_user.phone_number))
      this_cookie = cookie[user.COOKIE_NAME]
      this_cookie['expires'] = 86400 # 1 day
      this_cookie['path'] = '/'
      this_cookie['domain'] = '' # TODO(dbentley): what should this be?
      this_cookie['secure'] = '' # Also, this?

      header_str = cookie.output()[COOKIE_OFFSET:]
      self.response.headers.add_header('Set-Cookie', header_str)
      self.redirect('/w/')

    template_values = {}

    template_values['user'] = new_user

    if new_user:
      path = util.GetTemplate('webapp/logged_in.html')
    else:
      path = util.GetTemplate('webapp/no_user.html')
    self.response.out.write(template.render(path, template_values))

