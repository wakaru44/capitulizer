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

TRIGGER_TAG="#NewChapter"

def getEpisodeFromBD(keyEpisode):
    """This method should retrieve an episode object from bd safely"""
    return db.get(keyEpisode)


def buildTags(epObj):
    tags = "automagicoespialidoso, {0},{1}".format(
                                epObj.getDetails()["tvshow"],
                                "Temporada " + str(epObj.getDetails()["season"])
            )
    return tags


def buildSubject(epObj):
    show = epObj.getDetails()["tvshow"].encode("utf-8")
    subject = 'Ver {0} - {1} online {2}'.format(show,
                           str( epObj.getDetails()["season"] ),
                           TRIGGER_TAG)
    return subject


def buildBody(epObj):
    queriedEpisode = [epObj]
    logging.debug("queriedEpisode")
    logging.debug(epObj.title)
    output = {'title': epObj.title,
              'episodeObjs': queriedEpisode}

    template = jinja_environment.get_template("blogger.html")
    return  template.render(output)


class NewPostHandler(webapp2.RequestHandler):
    
    def post(self):
        """In this task, we should get an episode from bd, and elaborate
            a blog post. Then send it to IFTTT (or the admin
            while in development"""

        # TODO 1: in the first run, we shoul defer it for later, because if
        # there were no task pending, it will be instantly trigguered :(
        # below there are some code about how to check the queue

        logging.debug("NewPostHandler Entered")
        keyEpisode = self.request.get('keyEpisode')
        try:
            # - get the episode from the database
            epObj = getEpisodeFromBD(keyEpisode)
            # QUESTION: how should i encapsulate this??
            # answer: how about putting all the stuff about
            # building the message, and leave here only the sending?
            # answer2: and how about creating the params dictionary in
            # one function, and passing it to the task in another one?

            # - check if this episode has videos.
            if len(epObj.videos) > 0:
                logging.debug("has videos")

                # - start building the email body
                body = buildBody(epObj)
                #logging.debug("body")  # noisy
                #logging.debug(body)  # noisy

                # - build other parts of the message

                # - The subject will be the sentence of the title in the post
                # - TRIGGER_TAG is the tag that will action the IFTTT trigger
                # - and create the post
                subject = buildSubject(epObj)
                # - We send it to IFTTT to create the post
                to = "trigger@ifttt.com"
                # - send a copy to the mail account - try to post by email also
                cc = "capitulizer.mail@gmail.com, capitulizer.mail.icanhazpozt@blogger.com"
                # - The body tags are the boy of the message, that we use to send
                # - the tags of the episode
                bodyTags = buildTags(epObj)
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


