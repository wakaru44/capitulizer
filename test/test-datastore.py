#
#

#Join all the test related to the datastore, in a single file,
# for ease of testing.

import sys
sys.path.append("/usr/share/google_appengine")

import unittest
from nose.tools import *

from google.appengine.ext import testbed
from google.appengine.ext import db

import episode

import tasks.newEpisode as taskNewEpisode

class BaseDsTest(unittest.TestCase):
    def setUp(self):
        # - create the intance of testbed
        self.testbed = testbed.Testbed()
        # - Activate it 
        self.testbed.activate()
        # - declare the stubs
        self.testbed.init_datastore_v3_stub()
        #- create a example object
        #- used in put_episode or is_dupe i think
        self.epObj = episode.episode(link="http://seriesyonkis.com/")
        #- create other things for other tests (see bottom)
        #- used in is_dupe
        self.tne = taskNewEpisode.NewEpisodeHandler()
        self.link = ""


    def tearDown(self):
        self.testbed.deactivate()



#
#   From test-episode
#
class Test_episode_saving_in_datastore(unittest.TestCase):
    def setUp(self):
        # - create the intance of testbed
        self.testbed = testbed.Testbed()
        # - Activate it 
        self.testbed.activate()
        # - declare the stubs
        self.testbed.init_datastore_v3_stub()


    def tearDown(self):
        self.testbed.deactivate()

    def test_that_an_episode_is_saved_normally(self):
        epi = episode.episode(link="http://typing.io")
        epi.put()
        eq_(1, len(episode.episode.all().fetch(2)))

    @raises
    def test_an_empty_episode_is_not_saved(self):
        assert_raises(episode.episode(link=""), BadValueError)
        epi2 = episode.episode(link="")
        epi2.addDetails({})
        epi2.put()
        assertEqual(2, len(episode.episode.all().fetch(2)))


class test_all_the_same_by_link(BaseDsTest):
    """we should test that we find 2 objects already the same in duped, 1 if
    saved."""
    pass

##############################
#   from test-newEpisode.py
##############################

###
# check_and_save #db test TODO
###

###
# putEpisode # epObj, db stub
###

class test_put_episode(BaseDsTest):
    def test_returns_a_key_if_saved_correctly(self):
        key = self.tne.putEpisode(self.epObj)
        if key != None:
            eq_(1,1)
        else:
            raise Exception
        #TODO: write datastore test
        # nothing more than this should be necesary


###
# is_dupe #db test #TODO: datastore tests
###
# TODO: this should be in the episode object's method test
class test_is_dupe(BaseDsTest):
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



