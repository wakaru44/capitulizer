# -*- coding: utf-8 *-*

#import unittest
#import sys
#print sys.path
#from google.appengine.ext import testbed
#from google.appengine.api import taskqueue
#
#import tasks.newEpisode as taskNewEpisode
#
#
##class MailTestCase(unittest.TestCase):
##
###    def __init__(self):
###        super(MailTestCase, self).__init__()
##
##    def setUp(self):
##        self.testbed = testbed.Testbed()
##        self.testbed.activate()
##        self.testbed.init_mail_stub()
##        self.task_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
##        self.task_stub._ParseQueueYaml  ## Is it working?  
##
##    def tearDown(self):
##        self.testbed.deactivate()
##
##    def test_newPost_creates_a_task(self):
##        pass
##
##
##class OtherMethodsTestCase(unittest.TestCase):
##
##    def setUp(self):
##        self.testbed = testbed.Testbed()
##        self.testbed.activate()
##        self.taskHandler = taskNewEpisode.NewEpisodeHandler()
##
##    def tearDown(self):
##        self.testbed.deactivate()
#
#
#
#class OtherFunctionsTestCase(unittest.TestCase):
#
#    def setUp(self):
#        self.taskHandler = taskNewEpisode.NewEpisodeHandler()
#
#    def test_buildSearch_builds_a_nice_search(self):
#        details = { "fullTitle": "Capítulo 5",
#                    "tvshow": "True Blood"} 
#        expect = "Capítulo 5+True Blood"
#        result = self.taskHandler.buildSearch(self.taskHandler, details)
#        self.assertEqual(expect, result)
#
