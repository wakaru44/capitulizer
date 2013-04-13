# -*- coding: utf-8 *-*

import unittest
from nose.tools import *
#import sys
#print sys.path
from google.appengine.ext import testbed
from google.appengine.api import taskqueue

import tasks.newEpisode as taskNewEpisode
import episode


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
        # QUESTION: ES_ no se porque, pero declare como declare este
        # diccionario, cuando es convertido a traves del metodo populate episode
        # object, cambia las comillas a comillas simples, y me jode la asercion.
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
        # TODO: broken test. 
        # the method changes the quotation marks for single quotes, invalidating
        # the test... aisss
        epObj1 = self.tne.populate_episode_object(
                                        self.epObj,
                                        self.details_filled,
                                        self.picture_filled)
        #- test the internal dictionary
        eq_(repr(epObj1.detailsDict), repr(self.details_filled))
        #- check the json string that will be saved
        import json
        eq_(repr(epObj1.details), repr(json.dumps(self.details_filled)))
        #- check the picture
        eq_(epObj1.picture, self.picture_filled)


###
# putEpisode # epObj, db stub
###

##############################
#   Test related to datastore, no placed in
#   test-datastore.py
##############################

###
# is_dupe #db test 
###

##############################
#   Test related to datastore, no placed in
#   test-datastore.py
##############################

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
# post # WONT TEST
###

