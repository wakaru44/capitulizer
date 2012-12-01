#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import episode

#
#
#
## Helper Function. NOT A TEST


def loadFixt(filename):
    """Loads a fixture from a file, usually an HTML document and returns its
    content."""
    path = "./tests/fixtures/" + filename
    fh = open(path, "r")
    c = fh.read()
    return c.decode('utf-8')


def loadData(file):
    """load data from a file, using pickle"""
    fh = open("./tests/fixtures/" + file, "rb")
    data = pickle.load(fh)
    return data

### y aqui empezamos a probar

class test_episodeObject():
    """testing episode's methods"""

    def setUp(self):
        """ - """
        link = "http://seriesyonis.com/capitulo/mock"
        self.episode = episode.episode(link)

    def test_A_dictionary_of_details_is_correctly_saved(self):
        """a normal website says we are not robots"""
        expect = None
        dictionary = {}
        link = "http://seriesyonis.com/capitulo/mock"
        result = self.episode(dictionary)
        print "expect: ", expect                                
        print "result", result                          
        assert expect == result  

