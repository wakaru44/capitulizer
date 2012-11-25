#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm

import webapp2
import logging
from google.appengine.api import taskqueue
from google.appengine.api import mail


class SendEmailHandler(webapp2.RequestHandler):

    def post(self):
        """This task, send an email. Just that"""

        # get the data from the request.
        # CAREFULL the body might be too big :(
        sender = self.request.get('sender')
        subject = self.request.get('subject')
        bodyContent = self.request.get('body')
        bodyTags = self.request.get('bodyTags')
        # TODO 1: we need to know the tvshow to put the fucking tag
        cc = self.request.get('cc')
        bcc = self.request.get('bcc')
        to = self.request.get('to')

        try:

            logging.debug("We are about to send an email")
            # - first create the message
            # QUESTION I think that this should be in a function to test it
            # better
            message = mail.EmailMessage(sender=sender,
                              subject=subject)
            if to != "":
                message.to = to
            else:
                message.to = "wakaru44@gmail.com"
            if cc != "":
                message.cc = cc 
            if bcc != "":
                message.bcc = "" # TODO : add bcc
            message.html = bodyContent
            # - NOTE: we use the body to make the tags of the article
            message.body = bodyTags


            #post(payload=body.as_string())
            # noisy group:
            #logging.debug("sender")
            #logging.debug(repr(sender))
            #logging.debug("to")
            #logging.debug(repr(to))
            #logging.debug("cc")
            #logging.debug(repr(cc))
            #logging.debug("subject")
            #logging.debug(repr(subject))
            #logging.debug("body HTML")
            #logging.debug(repr(bodyContent))
            #logging.debug("mail")
            #logging.debug(repr(mail))
            # OLD REMOVE
            #mail.send_mail(sender, to, cc, subject, body)
            #mail.send_mail(sender.encode(), 
            #               to.encode(), 
            #               cc.encode(),
            #               subject.encode(), 
            #               body)

            # - then send an email
            message.send()


        except:
            logging.error("We could not send an email.")
            # TODO: add here a notification of some other kind?
            # this seems like a critical failure...
            # but i dont know how to handle it.
            raise



        #return 0

    def get(self):
        self.response.out.write("Welcome")
