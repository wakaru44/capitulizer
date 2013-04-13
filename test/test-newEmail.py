
import unittest
from nose.tools import * 

import sys
sys.path.append("/usr/share/google_appengine")

from google.appengine.ext import testbed
from google.appengine.ext import db
import episode


class test_new_email_handler(unittest.TestCase):
    def setUp(self):
        pass


###
# retrieve_episode_object  #db
###

###
# episode_has_videos  #db
###

###
# video_queue_empty  #taskqueue
###

###
# send_mail_to_admin  #email #TODO: getthisout
###

###
# episode_videos_added  #WONT TEST - NOT IMPLEMENTED
###

