import Cookie
import base64
import logging

import util

COOKIE_NAME = 'ZombieUser'

def GetCurrentUser(request):
  """Get the current user for the webapp.

  This is the same as for the API, except that the User can also be
    in a cookie.

  Eventually, we intend to support use of the webapp through the Users module
    that App Engine supplies.
  """
  user = None
  try:
    user = util.GetUserFromRequest(request)
  except util.ZombieException:
    # Look in the cookies
    user_cookie_text = request.cookies.get(COOKIE_NAME)
    if user_cookie_text != None:
      user_phone_number = str(base64.b64decode(user_cookie_text))
      user = util.GetOrCreateUserForPhoneNumber(user_phone_number)

  return user
