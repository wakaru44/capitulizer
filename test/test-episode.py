#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import episode
import logging

import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed

#
#
#
## Helper Function. NOT A TEST


def loadFixt(filename):
    """Loads a fixture from a file, usually an HTML document and returns its
    content."""
    path = "./test/fixtures/" + filename
    fh = open(path, "r")
    c = fh.read()
    return c.decode('utf-8')


def loadData(file):
    """load data from a file, using pickle"""
    fh = open("./test/fixtures/" + file, "rb")
    data = pickle.load(fh)
    return data

### y aqui empezamos a probar


class test_episode_setter_methods():
    """testing episode's methods"""

    def setUp(self):
        """ - """
        linkEp = "http://seriesyonis.com/capitulo/mock"
        self.episode = episode.episode(link=linkEp)

    def test_A_dictionary_of_details_is_correctly_added_to_the_episode(self):
        """The details dict is saved"""
        #TODO: This is all wrong, Its just a note to write the real test
        dictionary = {"season": 5,
                      "tvshow": "Chicho Terremoto",
                      "fullTitle": "mi chica es preciosa" }
        logging.error(self.episode)
        self.episode.addDetails(dictionary)
        expect = dictionary
        result = self.episode.getDetails()
        # TODO check that is saved
        print "expect: ", expect
        print "result", result
        assert expect == result

    def test_An_empty_dic_does_not_break_anything(self):
        self.episode.addDetails({})
        assertEqual({}, self.episode.getDetails())




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
        assertEqual(1, len(episode.episode.all().fetch(2)))

    def test_an_empty_episode_does_not_break_anything(self):
        epi2 = episode.episode(link="")
        epi2.addDetails({})
        epi2.put()
        assertEqual(2, len(episode.episode.all().fetch(2)))
