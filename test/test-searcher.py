#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import searcher
import nose


class test_searcher_images(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.normalDetails = { "tvshow": "True+blood",
                    "season": 8}


    def getImage_list_returns_Empty_list_when_no_results(self):

        search = { "tvshow": ""}
        userIP = "91.142.222.222"
        result = searcher.image.getImageList( search , userIP )
        print len(result)
        expect = []
        
        assert len(expect) == len(result)


    def test_getImage_list_returns_a_list_of_links_to_images(self):

        search = self.normalDetails
        userIP = "91.142.222.222"
        # this is the result of a search with episode title and tvshow
        #expect = [u'http://img2.timeinc.net/people/i/2012/news/120730/joe-manganiello-240.jpg',
        #u'http://tvrecappersanonymous.files.wordpress.com/2010/11/trueblood_eric.jpg',
        #u'http://ia.media-imdb.com/images/M/MV5BMjA3Mzg4MzUzM15BMl5BanBnXkFtZTcwNDIzMjU3Nw%40%40._V1._SY317_.jpg',
        #u'http://hbowatch.com/wp-content/uploads/2012/05/True-Blood-Series.jpg']
        # this is the result of search with only the tv show.
        expect = [u'http://img2.timeinc.net/people/i/2012/news/120730/joe-manganiello-240.jpg',
                 u'http://truebloodgirl.com/wp-content/uploads/2011/06/True-Blood.jpg',
                 u'http://tvrecappersanonymous.files.wordpress.com/2010/11/trueblood_eric.jpg',
                 u'http://ia.media-imdb.com/images/M/MV5BMjA3Mzg4MzUzM15BMl5BanBnXkFtZTcwNDIzMjU3Nw%40%40._V1._SY317_.jpg']

        result = searcher.image.getImageList( search , userIP )
        print len(result)
        
        assert len(result) >= 1

    def test_getLink_handles_unicode(self):
        search = { "tvshow": u'Cómo conocí a vuestra madre'}
        userIP = "91.142.222.222"
        result = searcher.image.getLink( search , userIP )
        # This result seems product of a bad encoding in the search 
        #expect = u'http://www.wallsave.com/wallpapers/1024x768/fon-reborn/780384/fon-reborn-katekyo-automatic-epis-dio-cap-tulo-780384.jpg'
        #expect = [u'http://3.bp.blogspot.com/_smzP2YZmS8s/S8QtXQGDL2I/AAAAAAAAAQA/ouoWWIjMYx0/s1600/comoconoci.jpg']
        expect = u'http://1.bp.blogspot.com/-Z_hA5kz4-ck/TnpR509lz_I/AAAAAAAABC8/bFjWGDMlDf0/s1600/HIMYM.jpg'
        print type(result)
        
        assert type(expect) == type(result)
        assert len(expect) > 1
    


    def test_getLink_returns_only_a_single_link(self):

        userIP = "91.142.222.222"
        result = searcher.image.getLink( self.normalDetails , userIP )
        expect = u'http://truebloodgirl.com/wp-content/uploads/2011/06/True-Blood.jpg'
        print result
        
        ##assert len(expect) == len(result)
        assert type(expect) == type(result)
 

    def test_getLink_receives_no_ip(self):

        userIP = ""
        result = searcher.image.getLink( self.normalDetails, userIP )
        expect = u'http://truebloodgirl.com/wp-content/uploads/2011/06/True-Blood.jpg'
        print result
        
        assert type(expect) == type(result)


    def getLink_returns_empty_string_if_no_results(self):
        details = {"tvshow": ""}
        userIP = "91.142.222.222"
        result = searcher.image.getLink( details , userIP )
        expect = u''
        print result
        
        assert expect == result
    

if __name__ == "__main__":
    unittest.main()
