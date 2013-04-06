# -*- coding: utf-8 *-*

import unittest
from nose.tools import *
#import sys
#print sys.path
from google.appengine.ext import testbed
from google.appengine.api import taskqueue

import tasks.newEpisode as taskNewEpisode
import episode
#
#
##class MailTestCase(unittest.TestCase):
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

class BaseTestCase(unittest.TestCase):
    pass

###
# get_params  #request
###

###
# create_object  #epOjb
###
class test_create_object(BaseTestCase):

    def setUp(self):
        self.link = ""
        self.submitter = ""

    @raises
    def test_empty_link_raise(self):
        episode.episode(link=self.link)

    def test_normal_link_accepts(self):
        link = "http://www.seriesyonkis.com/pruebas"

        epObj = episode.episode(link=link)
        eq_(epObj.link, link)

###
# get_episode_data #extract #WONT TEST
###

class test_get_episode_data(BaseTestCase):
    def setUp(self):
        import extract


###
# get_episode_picture # searcher #WONT TEST
###

###
# populate_episode_object # epObj
###

class test_populate_episode_object(BaseTestCase):
    def setUp(self):
        # empty values
        self.details_empty = {}
        self.picture_empty = ""
        # filled values
        self.details_filled = {"fullTitle": "capitulo 3",
                   "description": "no recuerdo como era la descripcion"}
        self.picture_filled = "http://blogspot.com/imagen.png"
        # object
        self.epObj = episode.episode(link="http://test-example.com")
        self.tne = taskNewEpisode.NewEpisodeHandler()

    @raises
    def test_raise_if_details_empty(self):
        assert_raises(Exception,
                      self.tne.populate_episode_object,
                      self.epObj, self.details_empty, self.picture_filled)

    @raises
    def test_raise_if_picture_empty(self):
        assert_raises(Exception,
                      self.tne.populate_episode_object,
                      self.details_filled, self.picture_empty)

    def test_filles_it_normally(self):
        epObj1 = self.tne.populate_episode_object(
                                        self.details_filled,
                                        self.picture_filled)
        eq_(eObj1.details, self.details_filled)
        eq_(eObj1.picture, self.picture_filled)


###
# putEpisode # epObj, db stub
###
class test_put_episode(BaseTestCase):
    def setUp(self):
        self.epObj = episode.episode(link="http://seriesyonkis.com/")

    def test_saves_an_episode(self):
        pass
        #datastore test, using db stubs 
        #TODO: write datastore test


###
# is_dupe #db test #TODO: datastore tests
###
class test_is_dupe(BaseTestCase):
    def setUp(self):
        self.tne = taskNewEpisode.NewEpisodeHandler()
        self.link = ""

    def test_returns_true_if_duplicated(self):
        link = "http://link-the-prueba/"
        #- save it once
        epOb = episode.episode(link=link)
        epOb.put()
        #- check it  again
        eq_(self.tne.is_dupe(link), True)

    def test_returns_false_if_not_dupe(self):
        #epOb = episode.episode(link="http://notdupe")
        eq_(self.tne.is_dupe("http://undupe"), False)


###
# deserves_to_be_saved # epObj #FUTURE TESTS
###

###
# create_watch_task #taskqueue stubs
###

###
# create_videos_tasks  #taskqueue stubs
###

###
# check_and_save #db test TODO
###

###
# post # WONT TEST
###

