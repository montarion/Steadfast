#! /usr/bin/python3.5

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/code/fileshare/')
from test import app as application
application.secret_key = 'anything you wish'
