#!/usr/bin/python
# -*- coding: utf-8 -*-


# Library to extract data from SY website.
import urllib2
import logging
#import random 
import json  
import re, urlparse


def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
    part.encode('idna') if parti==1 else
    urlEncodeNonAscii(part.encode('utf-8'))
    for parti, part in enumerate(parts)
    )


class image(object):

    @staticmethod
    def getImageList(search, userIP, referer = "capitulizer.appspot.com"):
        """Do a image search"""
        search = search.replace(u' ', u'+') 
        logging.debug( "searching images for...")
        #search = iriToUri( urlEncodeNonAscii(search) )
        search = iriToUri(search)
        
        # TODO: i know that you can do search in unicode ¿HOW?
        logging.debug(repr(search))
        # BEWARE maybe we should escape this before hitting google

        # The request also includes the userip parameter which provides the end
        # user's IP address. Doing so will help distinguish this legitimate 
        # server-side traffic from traffic which doesn't come from an end-user.
        url = ('https://ajax.googleapis.com/ajax/services/search/images'
                      '?v=1.0&q={0}&userip={1}'.format(search, userIP)  )
        # QUESTION: encode in utf-8? really?
        logging.debug("received")

        request = urllib2.Request(
                url, None, {'Referer': referer})
        response = urllib2.urlopen(request)
        searchData = json.load(response)
        # Process the JSON string.
        listOfLinks = []
        resultset = searchData["responseData"]["results"]
        for result in resultset:
            listOfLinks.append(result["url"])
            #pretty printin
            #logging.debug( json.dumps(retorna ,sort_keys=True,indent=4, separators=(',', ': ') )
            logging.debug(result["url"])

        return listOfLinks

    @staticmethod
    def getLink(search, userIP):
        """return just one link to an image"""
        logging.debug("getting link to an image")
        listOfThem = image.getImageList(search, userIP)
        if len(listOfThem) > 0:
            # pick just one
            # TODO: Enable this
            # I change this to a static choose to test it easier
            #selec = random.randint(0,len(listOfThem))
            selec = 1
            chosenLink = listOfThem[selec]
            return chosenLink
        else:
            return u''





# retorna = getImageList("true blood temporada 5 capitulo 4", '91.142.222.222')
#logging.debug( dir( retorna["responseData"]["results"][0]["url"] ))
#logging.debug( "****")
