#!/usr/bin/python
# -*- coding: utf-8 -*-


# Library to extract data from SY website.
import urllib2
import logging
import json  


class image(object):

    @staticmethod
    def getImageList(search, userIP, referer = "capitulizer.appspot.com"):
        """Do a image search"""
        search = search.replace(" ", "+") 
        logging.debug( "searching images for...")
        logging.debug(search)
        # BEWARE maybe we should escape this before hitting google

        # The request also includes the userip parameter which provides the end
        # user's IP address. Doing so will help distinguish this legitimate 
        # server-side traffic from traffic which doesn't come from an end-user.
        url = ('https://ajax.googleapis.com/ajax/services/search/images'
                      '?v=1.0&q={0}&userip={1}'.format(search, userIP)  )
        logging.debug( "received")

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
        # pick just one
        return listOfThem[3]



# retorna = getImageList("true blood temporada 5 capitulo 4", '91.142.222.222')
#logging.debug( dir( retorna["responseData"]["results"][0]["url"] ))
#logging.debug( "****")
