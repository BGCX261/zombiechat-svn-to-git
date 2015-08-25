#!/usr/bin/env python
"""
Prints out an 'export PYTHONPATH' command to be run so that all of the
appengine imports resolve correctly.

This code was stolen from dev_appserver.py.
"""  

import os
import sys

appengine_root = os.getenv('APPENGINE_ROOT')
if not appengine_root and len(sys.argv) == 2:
  appengine_root = sys.argv[1]

if not appengine_root: 
  print """
Usage:
  print_pythonpath.py /path/to/appengine/root/

  export APPENGINE_ROOT=/path/to/appengine/root
  print_pythonpath.py

If both the environment variable and command-line argument are specified, the
command-line argument wins.
""" 
  sys.exit(1) 
DIR_PATH = os.path.abspath(os.path.realpath(appengine_root))

EXTRA_PATHS = [
  DIR_PATH,
  os.path.join(DIR_PATH, 'lib', 'django'),
  os.path.join(DIR_PATH, 'lib', 'webob'),
  os.path.join(DIR_PATH, 'lib', 'yaml', 'lib'),
]

if __name__ == '__main__':
  print "export PYTHONPATH=%s:$PYTHONPATH" % ':'.join(EXTRA_PATHS)
