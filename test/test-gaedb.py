# -*- coding: utf-8 *-*

# primeras pruebas conejas con el datastore.

import unittest
from nose import tools
from google.appengine.ext import testbed
from google.appengine.ext import db
import episode


class DbTestCase(unittest.TestCase):

#    def __init__(self):
#        super(MailTestCase, self).__init__()

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        #self.testbed.init_mail_stub()
        #self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        self.testbed.init_datastore_v3_stub()
        link="http://seriescoco.com/capitulo/mock"
        self.episode= episode.episode(link=link)
        self.episode2= episode.episode(link=link)
        

    def tearDown(self):
        self.testbed.deactivate()

    def test_db_saves_normally(self):
        self.episode.put()
        self.assertEqual(1, len(self.episode.all().fetch(2)))
        pass

    def test_db_does_not_save_duplicates(self):
        self.episode.put()
        self.assertEqual(1, len(self.episode.all().fetch(2)))
        tools.assert_equal(1, len(self.episode.all().fetch(2)))
        
        #tools.assert_raises(self.episode2.save(), "Exception")
        self.assertRaises(Exception, self.episode2.save)
        pass

    def test_db_saves_incomplete_object(self):
        pass

    def test_db_needs_required_fields(self):
        pass

    def test_db_loads_incomplete_object(self):
        pass



#unittest.main()
