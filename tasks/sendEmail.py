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
        cc = self.request.get('cc')
        bcc = self.request.get('bcc')
        to = self.request.get('to')

        try:

            logging.debug("We are about to send an email")
            # - first create the message
            # QUESTION I think that some of this should be in a function to test it
            # better
            if sender == "":
                sender = "Capitulizer Mighty Poster Bot <capitulizer@capitulizer.appspotmail.com>"
            message = mail.EmailMessage(sender=sender,
                              subject=subject)
            if to != "":
                message.to = to
            else:
                message.to = "wakaru44@gmail.com"
                logging.error("No TO address. Sending one to the admin")
            if cc != "":
                message.cc = cc
            if bcc != "":
                message.bcc = bcc
            else:
                # logging.error("No Black Carbon Copy. Sending one to the admin")
                # message.bcc = "wakaru44@gmail.com"
                # bcc = "wakaru44@gmail.com"
                pass

            message.html = bodyContent
            # - NOTE: we use the body to make the tags of the article
            message.body = bodyTags


            # noisy group:
            logging.debug("sender")
            logging.debug(repr(sender))
            #logging.debug("body HTML")
            #logging.debug(repr(bodyContent))
            #logging.debug("mail")
            #logging.debug(repr(mail))

            # - then send an email
            message.send()
            logging.debug("And finally, mail sent")
            logging.debug("bcc")
            logging.debug(bcc)
            logging.debug("to")
            logging.debug(repr(to))
            logging.debug("cc")
            logging.debug(repr(cc))
            logging.debug("subject")
            logging.debug(repr(subject))
            logging.debug("text Body or BodyTags")
            logging.debug(repr(bodyTags))


        except:
            logging.error("We could not send an email.")
            # TODO: add here a notification of some other kind?
            # this seems like a critical failure...
            # but i dont know how to handle it.
            raise



        #return 0

    def get(self):
        self.response.out.write("Welcome")
