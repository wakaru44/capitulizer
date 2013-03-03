#!/usr/bin/python
# -*- coding: utf-8 -*-

# General application to receive email. It is listening in all the addresses,
# and just logs the message to the app log.
#
# https://developers.google.com/appengine/docs/python/mail/receivingmail

import logging

import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import taskqueue

import extract
import episode
import auxtools


class CapHandler(InboundMailHandler):
    """Receive emails with links to episodes"""

    def receive(self, mail_message):
        try:
            self.doReceive(mail_message)
        except extract.NoExtractorFoundError:
            logging.error('Error, Could not extract a shit')
            logging.error(mail_message)
            auxtools.send_email_to_admin(extract.NoExtractorFoundError, mail_message)
        except extract.NoEpisodesFoundError:
            logging.error('Error, No episodes found bro!')
            logging.error(mail_message)
            auxtools.send_email_to_admin(NoEpisodesFoundError, mail_message)

    def doReceive(self, mail_message):
        """receives an email and log it"""
        logging.info("We have received someting new")
        # log the entry .DEBUG
        logging.debug(mail_message.subject)
        #logging.debug(self.getBody(mail_message)) #  too many output

        # extract the links to episodes in the email received
        episodeLinks = extract.linksToEpisodes(
                                self.getBody(mail_message))  # Links list

        # for each one, we will create an task
        for ep in episodeLinks:
            logging.debug("creating a task for the episode found")
            logging.debug(ep)
            try:
                # Create a queue
                queue = taskqueue.Queue('newEpisode')
                # Conform a task
                task = taskqueue.Task(url='/tasks/newEpisode',
                              params={'episodeLink': ep,
                              'submitter': mail_message.sender,})
                # Add the task to the queue.
                queue.add(task)
            except TypeError as err:
                logging.error("Error")
                logging.error(err)
                logging.error(mail_message)

        #return 0


    def getBody(self, mail_message):
        """Get the best body available. It can be the html or the text part"""
        bodies = mail_message.bodies()
        for content_type, body in bodies:
            return body.decode().encode("utf-8")


#######################################

# Entry point for the general receiving app
app = webapp2.WSGIApplication(
    [CapHandler.mapping()]
)
