# -*- coding: utf-8 *-*

import unittest
from google.appengine.ext import testbed
from google.appengine.ext import db


class DbTestCase(unittest.TestCase):

#    def __init__(self):
#        super(MailTestCase, self).__init__()

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        #self.testbed.init_mail_stub()
        #self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        self.testbed.init_datastore_v3_stub()
        

    def tearDown(self):
        self.testbed.deactivate()

    def test_db_saves_normally(self):
        episode().put()
        self.assertEqual(1, len(episode.all().fetch(2)))
        pass

    def test_db_saves_incomplete_object(self):
        pass

    def test_db_needs_required_fields(self):
        pass

    def test_db_loads_incomplete_object(self):
        pass



unittest.main()
