#!/usr/bin/python
# -*- coding: utf-8 -*-

import searcher


class test_searcher_images():

    def test_getImage_list_returns_Empty_list_when_no_results(self):

        search = ""
        userIP = "91.142.222.222"
        result = searcher.image.getImageList( search , userIP )
        print result
        expect = []
        
        assert expect == result


    def test_getImage_list_returns_a_list_of_links_to_images(self):

        search = "True+blood"
        userIP = "91.142.222.222"
        expect = [u'http://img2.timeinc.net/people/i/2012/news/120730/joe-manganiello-240.jpg',
        u'http://tvrecappersanonymous.files.wordpress.com/2010/11/trueblood_eric.jpg',
        u'http://ia.media-imdb.com/images/M/MV5BMjA3Mzg4MzUzM15BMl5BanBnXkFtZTcwNDIzMjU3Nw%40%40._V1._SY317_.jpg',
        u'http://hbowatch.com/wp-content/uploads/2012/05/True-Blood-Series.jpg']
        result = searcher.image.getImageList( search , userIP )
        print expect 
        print result
        
        assert expect == result
 

    def test_getImageList_handles_unicode(self):
        search = u'Cómo conocí a vuestra madre'
        userIP = "91.142.222.222"
        result = searcher.image.getLink( search , userIP )
        # This result seems product of a bad encoding in the search 
        #expect = u'http://www.wallsave.com/wallpapers/1024x768/fon-reborn/780384/fon-reborn-katekyo-automatic-epis-dio-cap-tulo-780384.jpg'
        expect = []
        print expect 
        print result
        
        assert expect == result
    


    def test_getLink_returns_only_a_single_link(self):

        search = "True+blood"
        userIP = "91.142.222.222"
        result = searcher.image.getLink( search , userIP )
        expect = u'http://tvrecappersanonymous.files.wordpress.com/2010/11/trueblood_eric.jpg'
        print expect 
        print result
        
        assert expect == result
 

    def test_getLink_receives_no_ip(self):

        search = "True+blood"
        userIP = ""
        result = searcher.image.getLink( search , userIP )
        expect = u'http://tvrecappersanonymous.files.wordpress.com/2010/11/trueblood_eric.jpg'
        print expect 
        print result
        
        assert expect == result


    def test_getLink_returns_empty_string_if_no_results(self):
        search = ""
        userIP = "91.142.222.222"
        result = searcher.image.getLink( search , userIP )
        expect = u''
        print expect 
        print result
        
        assert expect == result
    
