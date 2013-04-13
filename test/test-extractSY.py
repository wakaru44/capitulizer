#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import extract

import unittest
from nose.tools import raises, assert_equal

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
#
#
#def loadData(file):
#    """load data from a file, using pickle"""
#    fh = open("./test/fixtures/" + file, "rb")
#    data = pickle.load(fh)
#    return data
#
#### y aqui empezamos a probar
#
#
##class test_openWebsite():
##
##    def test_A_local_webtest(self):
##        """checks the function with a local resource"""
##        url = "http://localhost:8080/capitulizer"
##        expect = loadFixt("local-test-output.html")
##        result = extract.openWebsite(url)
##        print expect
##        print result
##        assert expect == False
#
#
#class test_buildLink():
#    """the builLink is important to compose the final url's we'll be using 
#        when accessing SY content."""
#
#    def test_A_complete_link_gets_no_extra_output(self):
#        link = "http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
#        expect = "http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
#        result = extract.buildLink(link)
#        print expect
#        print result
#        assert expect == result
#
#
#    def test_A_incomplete_link_gets_the_domain(self):
#        # TODO
#        link = "/capitulo/the-big-bang-theory/capitulo-8/224754"
#        expect = "http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
#        result = extract.buildLink(link)
#        print expect
#        print result
#        assert expect == result
#
#    def test_A_wrong_link_gets_an_error(self):
#        # TODO
#        pass
#
#    def test_A_link_with_seriesyonkis_domain_gets_no_extra_output(self):
#        link = "http://www.seriesyonkis.com/capitulo/the-big-bang-theory/capitulo-8/224754"
#        expect = "http://www.seriesyonkis.com/capitulo/the-big-bang-theory/capitulo-8/224754"
#        result = extract.buildLink(link)
#        print expect
#        print result
#        assert expect == result
#
#    def test_A_link_with_domain_only_gets_no_extra_output(self):
#        # TODO
#        pass
#
#    def test_A_unicode_link_with_domain_only_gets_no_extra_output(self):
#        link = u"/capitulo/the-big-bang-theory/capitulo-8/224754"
#        expect = u"http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
#        result = extract.buildLink(link)
#        print expect
#        print result
#        assert expect == result
#
#    def test_A_malformed_link_returns_a_correct_one(self):
#        link = u"http://capitulo/the-big-bang-theory/capitulo-8/224754"
#        expect = u"http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
#        result = extract.buildLink(link)
#        print expect
#        print result
#        assert expect == result
#
#
#
#
#class test_extractEpisodesFromMail():
#    """ Test the function that gets the list of links from the mail"""
#
#    def test_Extract_a_single_bad_link_from_a_msg(self):
#        """Test the extraction of a
#            good single link to SY  BAD LOCATION from a mail"""
#        msg = loadFixt("extractEpisodes-badSingle.html")
#        expect = [
#    u'http://www.seriesyonkis.com/capitulo/the-walking-dead/capitulo-2/222051']
#        result = extract.linksToEpisodes(msg)
#
#        print "expect", expect
#        print "result", result
#        assert expect == result
#
#    def test_Extract_a_single_good_link_from_a_msg(self):
#        """Test the extraction of a
#            good single link to SY episode from a mail"""
#        msg = loadFixt("extractEpisodes-goodSingle.html")
#        expect = [
#    u'http://www.seriesyonkis.com/capitulo/the-walking-dead/capitulo-2/222045']
#        result = extract.linksToEpisodes(msg)
#        print "expect", expect
#        print "result", result
#        assert expect == result
#
#    def test_Extract_many_links_from_a_msg(self):
#        """ test the extracion of many links to SY in a mail"""
#        msg = loadFixt("extractEpisodes-goodMulti.html")
#        expect = [
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-14/217220',
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-15/217214',
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-16/217213',
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-17/217212',
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-18/217215',
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-19/217216',
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-20/217219',
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-21/217218',
#        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-22/217217'
#        ]
#        result = extract.linksToEpisodes(msg)
#
#        print "expect", expect
#        print "result", result
#        assert expect == result
#
#    def test_Parse_this_page_without_failing(self):
#        """ this is a page known to cause error. we added it to out tests"""
#        msg = loadFixt("extractSY-linksToEpisodes-iTFails.html")
#        expect = 97
#        result = len(extract.linksToEpisodes(msg))
#
#        print "expect", expect
#        print "result", result
#        assert expect == result
#
#
#class test_InterLinkks():
#    """ Getting the SY intermedium link
#        from a seriesyonkis/seriescoco link"""
#
#    def test_A_web_gives_a_link(self):
#        """ Test a good page, with one link"""
#        episodeWeb = loadFixt("getSYInterLink-goodSingle-input.html")
#        expect = [u'http://www.seriescoco.com/s/ngo/3/9/1/7/353']
#        result = extract.interLinks(episodeWeb)
#
#        print "expect", expect
#        print "result", result
#        assert expect == result
#
#    def test_A_lost_web_does_not_break(self):
#        """ Test a good page, with one link"""
#        episodeWeb = loadFixt("extractSY-badLost.html")
#        expect = None
#        result = extract.interLinks(episodeWeb)
#
#        print "expect", expect
#        print "result", result
#        assert expect == result
#
#    def test_A_web_that_has_two_links(self):
#        """ Test with a link to a good page, with two links"""
#
#        episodeWeb = loadFixt("getSYInterLink-goodMulti-input.html")
#        expect = [u'http://www.seriescoco.com/s/ngo/2/9/6/5/849',
#                 u'http://www.seriescoco.com/s/ngo/3/9/1/7/202']
#        result = extract.interLinks(episodeWeb)
#        print "expect", expect
#        print "result", result
#        assert len(result) == len(expect)
#
#    def test_A_web_that_has_many_links(self):
#        """ Test with a link to a good page, with many links"""
#
#        episodeWeb = loadFixt("getSYInterLink-goodSuperMulti-input.html")
#        expect = loadData("getSYInterLink-goodSuperMulti-output.txt")
#        result = extract.interLinks(episodeWeb)
#        print "expect", len(expect)
#        print "result", len(result)
#        # if i only compare the number, i get a more stable response.
#        assert len(expect) == len(result)
#
#    def test_a_broken_page_returns_none(self):
#        """ Test with a link to a broken page, with no episode."""
#        episodeWeb = loadFixt("getSYInterLink-bad-noLinks.html")
#        expect = None
#        result = extract.interLinks(episodeWeb)
#
#        print "expect", expect
#        print "result", result
#        assert expect == result
#
#
#class test_extractlinkToVideoSYandProvider():
#
#    def test_A_bad_link_doesn_not_break_anything(self):
#        """test that no links are found, and we died gracefully"""
#        expect = None
#        web = loadFixt("extractSY-badLost.html")
#        result = extract.linkToVideoSY(web)
#        print "expect: ", expect
#        print "result", result
#        assert expect == result
#
#    def test_A_good_link_returns_a_good_link(self):
#        """test that a good link is found, and only one"""
#        expect = u'http://www.seriescoco.com/s/y/4091459/0/s/136'
#        web = loadFixt("extractSYlinkToVideoSY-good-input.html")
#        result = extract.linkToVideoSY(web)
#        print "expect: ", expect
#        print "result", result
#        assert expect == result
#
#    def test_A_good_link_returns_a_provider(self):
#        """test that a good link is found, and only one"""
#        expect = u'magnovideo'
#        web = loadFixt("extractSYlinkToVideoSY-good-input.html")
#        result = extract.providerFromInterWeb(web)
#        print "expect: ", expect
#        print "result", result
#        assert expect == result
#
#
#class test_extractlinkToVideoInProv:
#
#    def test_A_bad_link_returns_none(self):
#        """test that a bad page gives no output"""
#        expect = None
#        web = "http://www.seriescoco.com/s/y/4093444437/0/s/136"
#        result = extract.linkToVideoSY(web)
#        print "expect: ", expect
#        print "result", result
#        assert expect == result
#
#    def test_A_bad_page_of_shit_returns_none(self):
#        """test that a bad page gives no output"""
#        expect = None
#        web = loadFixt("extractSY-badLost.html")
#        result = extract.linkToVideoSY(web)
#        print "expect: ", expect
#        print "result", result
#        assert expect == result
#
#    def test_A_good_link_returns_a_good_link(self):
#        """a good link will give you a good video link in the provider"""
#        expect = u'http://allmyvideos.net/4wia9zjfm2it'
#        link = "http://www.seriescoco.com/s/y/4093037/0/s/136"
#        result = extract.linkToVideoInProv(link)
#        print "expect: ", expect
#        print "result", result
#        assert expect == result
#
#    def test_A_good_incomplete_link_returns_a_good_link(self):
#        """a good link whit no domain will give you a
#            good video link in the provider"""
#        expect = u'http://allmyvideos.net/4wia9zjfm2it'
#        link = "/s/y/4093037/0/s/136"
#        result = extract.linkToVideoInProv(link)
#        print "expect: ", expect
#        print "result", result
#        assert expect == result
#
#    def test_A_good_link_can_be_given_in_unicode(self):
#        """a good link will give you a good video link in the provider"""
#        expect = u'http://allmyvideos.net/4wia9zjfm2it'
#        link = u'http://www.seriescoco.com/s/y/4093037/0/s/136'
#        result = extract.linkToVideoInProv(link)
#        print "expect: ", expect
#        print "result", result
#        assert expect == result
#
#class test_episodeDataFromEpisodeWeb():
#    """testing the funcion episodeDataFromInterWeb"""
#
#    def test_A_website_with_spanish_chars_in_title_and_desc(self):
#        """test with a known error prone html, that it returns without
#            breaking anything"""
#        # plain text version
#        #expect1 = u' Capítulo 6 8x6 ' # title
#        expect1 = u'Cap\xedtulo 6 <span> 8x6</span>' # title
#        # Plain Text version
#        #expect2 = u' Cómo conocí a vuestra madre Título original: Capítulo 6 Temporada: 8 Capítulo: 6 ' # desc
#        # HTML version
#        expect2 = u'<h2> C\xf3mo conoc\xed a vuestra madre</h2> <p><strong>  T\xedtulo original: </strong> Cap\xedtulo 6</p><p> <strong>  Temporada: </strong> 8</p> <p> <strong>  Cap\xedtulo: </strong> 6</p>'
#        web = loadFixt("episodeDataFromEpisodeWeb-GoodUnicode-input.html")
#        result1, result2, resultDic = extract.episodeDataFromEpisodeWeb(web)
#        print "expect 1 = ", repr(expect1  )
#        print "Result 1 = ", repr(result1)
#        print "expect 2 = ", repr(expect2)
#        print "Result 2 = ", repr(result2)
#        print "Details  = ", repr(resultDic)
#        assert expect1 == result1
#        assert expect2 == result2
#
#
#    def test_A_website_with_a_captcha(self):
#        """test that nothing breaks if we are detected, and that
#            we are gracefully noticed"""
#        expect = True
#        web = loadFixt("extractSY-captchaWeb.html")
#        result = extract.amIARobot(web)
#        print "expect: ", expect                                
#        print "result", result                          
#        assert expect == result  
#
#class test_amIARobot():
#    """testing that we can check if a website has been blocked with captchas."""
#
#    def test_A_normal_website_returns_false(self):
#        """a normal website says we are not robots"""
#        expect = False
#        web = loadFixt("episodeDataFromEpisodeWeb-GoodUnicode-input.html")
#        result = extract.amIARobot(web)
#        print "expect: ", expect                                
#        print "result", result                          
#        assert expect == result  
#
#
#    def test_A_captcha_block_web_returns_true(self):
#        """a captcha_block_web_returns_true """
#        expect = True
#        web = loadFixt("extractSY-captchaWeb.html")
#        result = extract.amIARobot(web)
#        print "expect: ", expect                                
#        print "result", result                          
#        assert expect == result  
#
#
#    def DEACTIVATED_A_normal_web_with_wrong_words_doesnt_give_fake_positive(self):
#        expect = False
#        web = loadFixt("extractSY-amIARobot-faux-input.html")
#        result = extract.amIARobot(web)
#        print "expect: ", expect                                
#        print "result", result                          
#        assert expect == result  

#    def test_An_unrelated_web_doesnt_give_exceptions(self):
#        expect = False
#        web = loadFixt("_-__-__-__-__-__-__-__-__-__-_")
#        result = " _-__-__-__-__-__-__-__-__-_  "
#        print "expect: ", expect                                
#        print "result", result                          
#        assert expect == result  






################################################

@raises(extract.LinkExtractionError)
def test_with_no_extractors_die_and_cry():
    extract.linksToEpisodes("",{})
    
class FakeException(Exception):
    pass

@raises(FakeException)
def test_with_a_failing_extractor_die_and_cry():
    def fake_extractor(msg):
        raise FakeException

    extract.linksToEpisodes("foo", {"foo": fake_extractor})

def test_matching_extractors_are_executed():
    def fake_extractor1(msg):
        print "nice"
        return ["nice"]

    def fake_extractor2(msg):
        print "beautiful"
        return ["beautiful"]

    def fake_extractor3(msg):
        print "ugly"
        return ["ugly"]

    extractors = {
           "foo": fake_extractor1,
           "gaita": fake_extractor2,
           "ochourizo": fake_extractor3
           }

    result = extract.linksToEpisodes("foo gaita", extractors)
    expect = ["beautiful","nice"]
    assert_equal(result, expect)


class BaseTest(unittest.TestCase):
    """base class to test extractions"""

    mappings = {
        "episodeWeb": "episodeDataFromEpisodeWeb-GoodUnicode-input.html",
        "interWeb": "extractSYlinkToVideoSY-good-input.html",
        "captcha": "extractSY-captchaWeb.html",
        "lostEpisode": "extractSY-badLost.html",
        "email": "email-example.txt"
    }
    
    def load_html(self, type="episodeWeb"):
        """load an html in a bs4 element"""
        web = self.mappings[type]
        return loadFixt(web)

    def setUp(self):
        self.fixt = self.load_html()

class test_extraction_of_episodeData_from_episodeWeb(BaseTest):
    
    def test_extraction_of_title(self):
        """TODO"""
        pass

    def test_extraction_of_(self):
        """TODO: write test for each field"""
        pass

    #- desde pagina de episodio
    @raises(extract.LinkExtractionError)
    def test_interLinks_raise_with_bad_html(self):
        """raises exception if no links found"""
        extract.interLinks("<html><head></head><body></body></html>")

    def test_interLinks_with_good_episode_web(self):
        """Returns a list of links"""
        expect0 = 74  # number of links expected
        expect1 = '/s/ngo/4/2/1/5/222'  #example of link

        result = extract.interLinks(self.fixt)
        print result
        self.assertEqual(len(result), expect0)  # number of results
        self.assertEqual(result[0], expect1)  # results are good


class test_extraction_from_interweb(BaseTest):

    def setUp(self):
        self.fixt = self.load_html("interWeb")

    # desde pagina intermedia
    def test_linkToVideoSY(self):
        """ES_ comprueba que al pasarle un html de web intermedia, extrae el
        link al video en el shortener de SY"""
        expect = "http://www.seriescoco.com/s/y/4091459/0/s/136"  # a link to the video in shortener
        result = extract.linkToVideoSY(self.fixt)
        self.assertEqual(expect, result)

    def test_providerFromInterWeb_returns_provider(self):
        pass  #TODO



class test_extraction_from_SY_email(BaseTest):

    def setUp(self):
        self.fixt=self.load_html("email")

    # desde el email
    def test_linksToEpisodes(self):
        # Already tested in test_sy_url_extraction.py
        pass

    # desde el email
    def test_linksToEpisodesSY(self):
        """ES_ comprueba que al pasarle un email extrae los enlaces al episodio
        que hay en el email"""
        expect = [u"http://www.seriesyonkis.com/capitulo/once-upon-a-time/capitulo-18/236053"]
        result = extract.linksToEpisodesSY(self.fixt.encode("UTF-8"))
        self.assertEqual(expect, result)


class test_extraction_from_links(BaseTest):
    # desde link de episodio
    def test_linkToVideoInProvFromEpisodeLink(self):
        """ES_ comprueba que la extraccion directamente desde enlace del
        episodio da una lista de videos"""
        #- TODO: ES_ comprobar si esta funcion se esta realmente usando.... 


    # desde enlace a interweb
    def test_linkToVideoAndProvFromInterLink(self):
    # esta func. llama a las que reciben la web.
        """ES_ pruebas de que la extraccion conjunta funciona igual de bien que
        la separada"""
        expectVid = "http://www.seriescoco.com/s/y/4091459/0/s/136"  # a link to the video in shortener
        expectProv = "moevideos"
        # Deactivated. requires conection
        #    resultVid, resultProv = extract.linkToVideoAndProvFromInterLink(self.fixt)
        #    print resultVid, "--", resultProv
        #    self.assertEqual(expectVid, resultVid)
        #    self.assertEqual(expectProv, resultProv)


    # desde enlace shortener
    def test_linkToVideoInProv(self):
        """ES_ prueba que la extraccion del video en el proveedor desde un
        enlace al shortener es correcta"""
        pass


