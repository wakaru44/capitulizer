# -*- coding: utf-8 *-*

# primeras pruebas conejas con el datastore. 

import unittest
from nose import tools
import tasks.newPost as nuPost

#from google.appengine.ext import testbed
#from google.appengine.ext import db
#import episode
#import extractSY


#class DbTestCase(unittest.TestCase):
#
##    def __init__(self):
##        super(MailTestCase, self).__init__()
#
#    def setUp(self):
#        self.testbed = testbed.Testbed()
#        self.testbed.activate()
#        #self.testbed.init_mail_stub()
#        #self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
#        self.testbed.init_datastore_v3_stub()
#        link="http://seriescoco.com/capitulo/mock"
#        self.episode= episode.episode(link=link)
#        #web = extractSY.openWebsite(link)
#        #details = extractSY.episodeDataFromEpisodeWeb(web)
#        #self.episode.addDetails(details)
#        
#
#    def tearDown(self):
#        self.testbed.deactivate()
#
#    def test_db_saves_normally(self):
#        self.episode.put()
#        tools.assert_equal(1, len(self.episode.all().fetch(2)))
#


def test_buildSubject():
    expect = "Ver Ej\xc3\xa9mpl\xc3\xb3 de show - 99 online #NewChapter"
    result = nuPost.buildSubject(u'Ejémpló de show', 99)
    print result
    tools.assert_equal(expect, result)

def test_buildTags():
    expect = "automagicoespialidoso,Ej\xc3\xa9mpl\xc3\xb3 de show,Temporada 99"
    result = nuPost.buildTags(u'Ejémpló de show', 99)
    tools.assert_equal(expect, result)


#unittest.main()