#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import extractSY

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


#class test_openWebsite():
#
#    def test_A_local_webtest(self):
#        """checks the function with a local resource"""
#        url = "http://localhost:8080/capitulizer"
#        expect = loadFixt("local-test-output.html")
#        result = extractSY.openWebsite(url)
#        print expect
#        print result
#        assert expect == False


class test_buildLink():
    """the builLink is important to compose the final url's we'll be using 
        when accessing SY content."""

    def test_A_complete_link_gets_no_extra_output(self):
        link = "http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
        expect = "http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
        result = extractSY.buildLink(link)
        print expect
        print result
        assert expect == result


    def test_A_incomplete_link_gets_the_domain(self):
        # TODO
        link = "/capitulo/the-big-bang-theory/capitulo-8/224754"
        expect = "http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
        result = extractSY.buildLink(link)
        print expect
        print result
        assert expect == result

    def test_A_wrong_link_gets_an_error(self):
        # TODO
        pass

    def test_A_link_with_seriesyonkis_domain_gets_no_extra_output(self):
        link = "http://www.seriesyonkis.com/capitulo/the-big-bang-theory/capitulo-8/224754"
        expect = "http://www.seriesyonkis.com/capitulo/the-big-bang-theory/capitulo-8/224754"
        result = extractSY.buildLink(link)
        print expect
        print result
        assert expect == result

    def test_A_link_with_domain_only_gets_no_extra_output(self):
        # TODO
        pass

    def test_A_unicode_link_with_domain_only_gets_no_extra_output(self):
        link = u"/capitulo/the-big-bang-theory/capitulo-8/224754"
        expect = u"http://www.seriescoco.com/capitulo/the-big-bang-theory/capitulo-8/224754"
        result = extractSY.buildLink(link)
        print expect
        print result
        assert expect == result



class test_extractEpisodesFromMail():
    """ Test the function that gets the list of links from the mail"""

    def test_Extract_a_single_bad_link_from_a_msg(self):
        """Test the extraction of a
            good single link to SY  BAD LOCATION from a mail"""
        msg = loadFixt("extractEpisodes-badSingle.html")
        expect = [
    u'http://www.seriesyonkis.com/capitulo/the-walking-dead/capitulo-2/222051']
        result = extractSY.linksToEpisodes(msg)

        print "expect", expect
        print "result", result
        assert expect == result

    def test_Extract_a_single_good_link_from_a_msg(self):
        """Test the extraction of a
            good single link to SY episode from a mail"""
        msg = loadFixt("extractEpisodes-goodSingle.html")
        expect = [
    u'http://www.seriesyonkis.com/capitulo/the-walking-dead/capitulo-2/222045']
        result = extractSY.linksToEpisodes(msg)
        print "expect", expect
        print "result", result
        assert expect == result

    def test_Extract_many_links_from_a_msg(self):
        """ test the extracion of many links to SY in a mail"""
        msg = loadFixt("extractEpisodes-goodMulti.html")
        expect = [
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-14/217220',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-15/217214',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-16/217213',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-17/217212',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-18/217215',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-19/217216',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-20/217219',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-21/217218',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-22/217217'
        ]
        result = extractSY.linksToEpisodes(msg)

        print "expect", expect
        print "result", result
        assert expect == result


class test_InterLinkks():
    """ Getting the SY intermedium link
        from a seriesyonkis/seriescoco link"""

    def test_A_web_gives_a_link(self):
        """ Test a good page, with one link"""
        episodeWeb = loadFixt("getSYInterLink-goodSingle-input.html")
        expect = [u'http://www.seriescoco.com/s/ngo/3/9/1/7/353']
        result = extractSY.interLinks(episodeWeb)

        print "expect", expect
        print "result", result
        assert expect == result

    def test_A_lost_web_does_not_break(self):
        """ Test a good page, with one link"""
        episodeWeb = loadFixt("extractSY-badLost.html")
        expect = None
        result = extractSY.interLinks(episodeWeb)

        print "expect", expect
        print "result", result
        assert expect == result

    def test_A_web_that_has_two_links(self):
        """ Test with a link to a good page, with two links"""

        episodeWeb = loadFixt("getSYInterLink-goodMulti-input.html")
        expect = [u'http://www.seriescoco.com/s/ngo/2/9/6/5/849',
                 u'http://www.seriescoco.com/s/ngo/3/9/1/7/202']
        result = extractSY.interLinks(episodeWeb)
        print "expect", expect
        print "result", result
        assert len(result) == len(expect)

    def test_A_web_that_has_many_links(self):
        """ Test with a link to a good page, with many links"""

        episodeWeb = loadFixt("getSYInterLink-goodSuperMulti-input.html")
        expect = loadData("getSYInterLink-goodSuperMulti-output.txt")
        result = extractSY.interLinks(episodeWeb)
        print "expect", len(expect)
        print "result", len(result)
        # if i only compare the number, i get a more stable response.
        assert len(expect) == len(result)

    def test_A_link_to_a_broken_page_does_not_break(self):
        """ Test with a link to a broken page, with no episode."""
        expect = ""
        result = ""

        print "expect", expect
        print "result", result
        assert expect == result


class test_extractlinkToVideoSYandProvider():

    def test_A_bad_link_doesn_not_break_anything(self):
        """test that no links are found, and we died gracefully"""
        expect = None
        web = loadFixt("extractSY-badLost.html")
        result = extractSY.linkToVideoSY(web)
        print "expect: ", expect
        print "result", result
        assert expect == result

    def test_A_good_link_returns_a_good_link(self):
        """test that a good link is found, and only one"""
        expect = u'http://www.seriescoco.com/s/y/4091459/0/s/136'
        web = loadFixt("extractSYlinkToVideoSY-good-input.html")
        result = extractSY.linkToVideoSY(web)
        print "expect: ", expect
        print "result", result
        assert expect == result

    def test_A_good_link_returns_a_provider(self):
        """test that a good link is found, and only one"""
        expect = u'magnovideo'
        web = loadFixt("extractSYlinkToVideoSY-good-input.html")
        result = extractSY.providerFromInterWeb(web)
        print "expect: ", expect
        print "result", result
        assert expect == result


class test_extractlinkToVideoInProv:

    def test_A_bad_link_returns_none(self):
        """test that a bad page gives no output"""
        expect = None
        web = "http://www.seriescoco.com/s/y/4093444437/0/s/136"
        result = extractSY.linkToVideoSY(web)
        print "expect: ", expect
        print "result", result
        assert expect == result

    def test_A_bad_page_of_shit_returns_none(self):
        """test that a bad page gives no output"""
        expect = None
        web = loadFixt("extractSY-badLost.html")
        result = extractSY.linkToVideoSY(web)
        print "expect: ", expect
        print "result", result
        assert expect == result

    def test_A_good_link_returns_a_good_link(self):
        """a good link will give you a good video link in the provider"""
        expect = u'http://allmyvideos.net/4wia9zjfm2it'
        link = "http://www.seriescoco.com/s/y/4093037/0/s/136"
        result = extractSY.linkToVideoInProv(link)
        print "expect: ", expect
        print "result", result
        assert expect == result

    def test_A_good_incomplete_link_returns_a_good_link(self):
        """a good link whit no domain will give you a
            good video link in the provider"""
        expect = u'http://allmyvideos.net/4wia9zjfm2it'
        link = "/s/y/4093037/0/s/136"
        result = extractSY.linkToVideoInProv(link)
        print "expect: ", expect
        print "result", result
        assert expect == result

    def test_A_good_link_can_be_given_in_unicode(self):
        """a good link will give you a good video link in the provider"""
        expect = u'http://allmyvideos.net/4wia9zjfm2it'
        link = u'http://www.seriescoco.com/s/y/4093037/0/s/136'
        result = extractSY.linkToVideoInProv(link)
        print "expect: ", expect
        print "result", result
        assert expect == result

class test_episodeDataFromEpisodeWeb():
    """testing the funcion episodeDataFromInterWeb"""

    def test_A_website_with_spanish_chars_in_title_and_desc(self):
        """test with a known error prone html, that it returns without
            breaking anything"""
        # plain text version
        #expect1 = u' Capítulo 6 8x6 ' # title
        expect1 = u' Cap\xedtulo 6 <span>\n 8x6\n</span>\n ' # title
        # Plain Text version
        #expect2 = u' Cómo conocí a vuestra madre Título original: Capítulo 6 Temporada: 8 Capítulo: 6 ' # desc
        # HTML version
        expect2 = u' <h2>\n C\xf3mo conoc\xed a vuestra madre\n</h2>\n <p>\n<strong>\n  T\xedtulo original:\n </strong>\n Cap\xedtulo 6\n</p>\n<p>\n <strong>\n  Temporada:\n </strong>\n 8\n</p>\n <p>\n <strong>\n  Cap\xedtulo:\n </strong>\n 6\n</p>\n '
        web = loadFixt("episodeDataFromEpisodeWeb-GoodUnicode-input.html")
        result1, result2 = extractSY.episodeDataFromEpisodeWeb(web)
        print "expect 1 = ", repr(expect1  )
        print "Result 1 = ", repr(result1)
        print "expect 2 = ", repr(expect2)
        print "Result 2 = ", repr(result2)
        assert expect1 == result1
        assert expect2 == result2


    def test_A_website_with_a_captcha(self):
        """test that nothing breaks if we are detected, and that
            we are gracefully noticed"""
        expect = True
        web = loadFixt("extractSY-captchaWeb.html")
        result = extractSY.amIARobot(web)
        print "expect: ", expect                                
        print "result", result                          
        assert expect == result  

class test_amIARobot():
    """testing that we can check if a website has been blocked with captchas."""

    def test_A_normal_website_returns_false(self):
        """a normal website says we are not robots"""
        expect = False
        web = loadFixt("episodeDataFromEpisodeWeb-GoodUnicode-input.html")
        result = extractSY.amIARobot(web)
        print "expect: ", expect                                
        print "result", result                          
        assert expect == result  


    def test_A_captcha_block_web_returns_true(self):
        """a captcha_block_web_returns_true """
        expect = True
        web = loadFixt("extractSY-captchaWeb.html")
        result = extractSY.amIARobot(web)
        print "expect: ", expect                                
        print "result", result                          
        assert expect == result  


    def test_A_normal_web_with_wrong_words_doesnt_give_fake_positive(self):
        expect = False
        web = loadFixt("extractSY-amIARobot-faux-input.html")
        result = extractSY.amIARobot(web)
        print "expect: ", expect                                
        print "result", result                          
        assert expect == result  

#    def test_An_unrelated_web_doesnt_give_exceptions(self):
#        expect = False
#        web = loadFixt("_-__-__-__-__-__-__-__-__-__-_")
#        result = " _-__-__-__-__-__-__-__-__-_  "
#        print "expect: ", expect                                
#        print "result", result                          
#        assert expect == result  


