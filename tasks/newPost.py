#!/usr/bin/python
# -*- coding: utf-8 -*-

# 25-nov-2012 juanantoniofm

import webapp2
import logging
import jinja2
import os
from google.appengine.api import taskqueue
from google.appengine.ext import db

import episode  # it's actually used, but not declared explicitly.

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../templates"))


class NewPostHandler(webapp2.RequestHandler):
    

    TRIGGER_TAG="#NewChapter"

    def post(self):
        """In this task, we should get an episode from bd, and elaborate
            a blog post. Then send it to IFTTT (or the admin
            while in development"""

        # TODO 1: in the first run, we shoul defer it for later, because if
        # there were no task pending, it will be instantly trigguered :(

        logging.debug("NewPostHandler Entered")
        keyEpisode = self.request.get('keyEpisode')
        try:
            # - get the episode from the database
            epObj = self.getEpisodeFromBD(keyEpisode)
            # QUESTION: how should i encapsulate this??
            # answer: how about putting all the stuff about
            # building the message, and leave here only the sending?
            # answer2: and how about creating the params dictionary in
            # one function, and passing it to the task in another one?

            # - check if this episode has videos.
            if len(epObj.videos) > 0:
                logging.debug("has videos")

                # - start building the email body
                body = self.buildBody(epObj)
                #logging.debug("body")  # noisy
                #logging.debug(body)  # noisy

                # - build other parts of the message

                # - The subject will be the sentence of the title in the post
                # - TRIGGER_TAG is the tag that will action the IFTTT trigger
                # - and create the post
                subject = self.buildSubject(epObj)
                # - We send it to IFTTT to create the post
                to = "trigger@ifttt.com"
                # - send a copy to the mail account - try to post by email also
                cc = "capitulizer.mail@gmail.com, capitulizer.mail.icanhazpozt@blogger.com"
                # - The body tags are the boy of the message, that we use to send
                # - the tags of the episode
                bodyTags = self.buildTags
                logging.debug("subject")
                logging.debug(repr(subject))

                # QUESTION: could this way be more maintenable and powerful?
                # QUESTION: Will we reach the size limit for task parameters??
                logging.debug("Creating a sendEmail Task with a new Post")
                queue = taskqueue.Queue('sendEmail')
                task = taskqueue.Task(url='/tasks/sendEmail',
                                      params={
                                              'subject': subject,
                                              'to': to,
                                              'cc': cc,
                                              'bodyTags': bodyTags,
                                              'body': body})
                queue.add(task)
            else:
                logging.error("no videos in the database yet. Retrying")
                raise Exception


        except TypeError:
            logging.error("No episode object?")
            raise
        except:
            raise


        ############################################################
        # # check if all this episode videos have been added or failed
        # # (second version)
        # queue = taskqueue.Queue() # newVideos
        # #queueStats = taskqueue.QueueStats(queue, ['newVideo'], 2)
        # # new way
        # queueStats = queue.fetch_statistics()  # returns QueueStatistics

        # if queueStats.tasks == 0:
        #     logging.debug("There are no pending video tasks")
        #     # so send an email

        #     sender = "Capitulizer Mighty Bot <capitulizer@capitulizer.appspotmail.com>"
        #     to = submitter  # send them to the submitter TODO
        #     cc = "wakaru44@gmail.com"  # and send a copy to the admin
        #     subject = "New Episode Available to Watch"
        #     body  = """<html><h1>This shoul be like the /blogger template.</h1>
        #     http://capitulizer.appspot.com/blogger</html>"""


        #     # Old version, sending the mail from here.
        #     # mail.send_mail(sender, to, subject, body)
        #     # New version, creating a new task
        #     # QUESTION: could this way be more maintenable and powerful?
        #     # QUESTION: Will we reach the size limit for task parameters??
        #     logging.debug("Creating a sendEmail Task")
        #     queue = taskqueue.Queue('sendEmail')
        #     task = taskqueue.Task(url='/tasks/sendEmail',
        #                           params={'sender': sender,
        #                                   'subject': subject,
        #                                   'body': body,
        #                                   'cc': cc,
        #                                   'to': to})
        #     queue.add(task)


        # else:
        #     logging.debug("There are still some video tasks to complete")
        #     # so retry
        #     raise Exception("Still new videos waiting. Maybe next time...")
        ############################################################

        #return 0  # big mistake! REMOVE

    def getEpisodeFromBD(self, keyEpisode):
        """This method should retrieve an episode object from bd safely"""
        return db.get(keyEpisode)


    def get(self):
        HTML="""
        <body>

            <form name="input" action="/tasks/newPost"
            method="post">
            Episode key <input type="text" name="keyEpisode" value="a1a1a1a1a1a1a"><br>
            <input type="submit" value="Submit">
            </form>

        </body>
        """
        self.response.out.write(HTML)


    def buildBody(self, epObj):
        queriedEpisode = [epObj]
        logging.debug("queriedEpisode")
        logging.debug(epObj.title)
        output = {'title': epObj.title,
                  'episodeObjs': queriedEpisode}

        template = jinja_environment.get_template("blogger.html")
        return  template.render(output)


    def buildSubject(self, epObj):
        subject = u'Ver {0} - {1} online {2}'.format(epObj.getDetails()["tvshow"],
                               str( epObj.getDetails()["season"] ),
                               self.TRIGGER_TAG)
        return subject

    def buildTags(self, epObj):
        tags = "automagicoespialidoso, {0},{1}".format(
                                        epObj.getDetails()["tvshow"],
                                        "Temporada " + str(epObj.getDetails()["season"])
                )
        return tags


