#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm

import webapp2
from google.appengine.api import taskqueue
from google.appengine.api import mail


class SendEmailHandler(webapp2.RequestHandler):

    def post(self):
        """This task, send an email. Just that"""

        # get the data from the request.
        # CAREFULL the body might be too big :(
        sender = self.request.get('sender')
        subject = self.request.get('subject')
        body = self.request.get('body')
        cc = self.request.get('cc')
        to = self.request.get('to')

        try:

            logging.debug("We are about to send an email")
            # so send an email
            mail.send_mail(sender, to, subject, body) # TODO 1: add the cc

        except:
            logging.error("We could not send an email.")
            # TODO: add here a notification of some other kind?
            # this seems like a critical failure... 
            # but i dont know how to handle it. 
            raise 



        return 0 

    def get(self):
        self.response.out.write("Welcome")
