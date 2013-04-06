# -*- coding: utf-8 *-*

# primeras pruebas conejas con el datastore. 

import unittest
from nose import tools
import tasks.newPost as nuPost

from google.appengine.ext import testbed
from google.appengine.ext import db
import episode
import extract


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
        #web = extract.openWebsite(link)
        #details = extract.episodeDataFromEpisodeWeb(web)
        #self.episode.addDetails(details)
        

    def tearDown(self):
        self.testbed.deactivate()

    def test_db_saves_normally(self):
        self.episode.put()
        tools.assert_equal(1, len(self.episode.all().fetch(2)))



def test_buildPostTitle():
    expect = "Ver Ejemplo de show - Temp. 9 -  Capitulo molon de turno online #NewChapter"
    result = nuPost.buildPostTitle({ "tvshow": u'Ejémpló de show',
                                    "season": u'9',
                                    "fullTitle": u' Capitulo molon de turno',
                                    "episodeNumber": 99})
    print result
    tools.assert_equal(expect, result)

def buildTags_with_unicode():  # Deactivated
    expect = "automagicoespialidoso,Ej\xc3\xa9mpl\xc3\xb3 de show,Temporada 99"
    result = nuPost.buildTags(u'Ejémpló de show', u'99')
    tools.assert_equal(expect, result)


def test_buildTags_no_unicode():
    expect = "Ejemplo de show,Temporada 99"
    result = nuPost.buildTags(u'Ejemplo de show', u'99')
    tools.assert_equal(expect, result)



#unittest.main()
