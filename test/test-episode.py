#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import episode
import logging

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

class test_episodeObject():
    """testing episode's methods"""

    def setUp(self):
        """ - """
        linkEp = "http://seriesyonis.com/capitulo/mock"
        self.episode = episode.episode(link = linkEp)

    def test_A_dictionary_of_details_is_correctly_added_to_the_episode(self):
        """The details dict is saved"""
        #TODO: This is all wrong, Its just a note to write the real test
        dictionary = {
                      "season": 5,
                      "tvshow": "Chicho Terremoto",
                      "fullTitle": "mi chica es preciosa"
                     }
        logging.error(self.episode)
        self.episode.addDetails(dictionary)
        self.episode.put()
        expect = dictionary
        result = self.episode.getDetails()
        # TODO check that is saved
        print "expect: ", expect                                
        print "result", result                          
        assert expect == result  

