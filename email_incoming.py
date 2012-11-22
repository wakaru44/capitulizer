#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################
# Date: 2012 10 24
###########################################
# General application to receive email. It is listening in all the addresses,
# and just logs the message to the app log.
#
# https://developers.google.com/appengine/docs/python/mail/receivingmail
###########################################

import logging

#import urllib2
#import time
#from bs4 import BeautifulSoup

import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


class LogSenderHandler(InboundMailHandler):
    """General class to recived messages.
       by now, it just records them in the log"""

    def receive(self, mail_message):
        """receives an email and log it"""
        logging.info("Received a message from: " +
            mail_message.sender)
        logging.info(self.getBody(mail_message))
        ## TODO finish this

    def getBody(self, mail_message):
        """Return the html body of a message. """
        # TODO: it would be nice to return the text body if html is not
        # availabe
        html_bodies = mail_message.bodies('text/html')
        for content_type, body in html_bodies:
            decoded_html = body.decode()
            # return the first htmlbody found in unicode format.
            # i think that should be a way to avoid this for loop, but...
            return decoded_html

# Entry point for the general receiving app
app = webapp2.WSGIApplication(
    [LogSenderHandler.mapping()]
)
