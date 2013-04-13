#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import episode
import logging

import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from nose.tools import *

@nottest
def loadFixt(filename):
    """Loads a fixture from a file, usually an HTML document and returns its
    content."""
    path = "./test/fixtures/" + filename
    fh = open(path, "r")
    c = fh.read()
    return c.decode('utf-8')


@nottest
def loadData(file):
    """load data from a file, using pickle"""
    fh = open("./test/fixtures/" + file, "rb")
    data = pickle.load(fh)
    return data


class test_episode_setter_methods():
    """testing episode's methods"""

    def setUp(self):
        """ - """
        linkEp = "http://seriesyonis.com/capitulo/mock"
        self.episode = episode.episode(link=linkEp)

    def test_A_dictionary_of_details_is_correctly_added_to_the_episode(self):
        """The details dict is saved"""
        dictionary = {"season": 5,
                      "tvshow": "Chicho Terremoto",
                      "fullTitle": "mi chica es preciosa" }
        logging.error(self.episode)
        self.episode.addDetails(dictionary)
        expect = dictionary
        result = self.episode.getDetails()
        print "expect: ", expect
        print "result", result
        assert expect == result

    def test_An_empty_dic_does_not_break_anything(self):
        self.episode.addDetails({})
        eq_({}, self.episode.getDetails())

##############################
#   Test related to datastore, no placed in
#   test-datastore.py
##############################
