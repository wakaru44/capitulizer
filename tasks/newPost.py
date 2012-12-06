#!/usr/bin/python
# -*- coding: utf-8 -*-

# 25-nov-2012 juanantoniofm

import webapp2
import logging
import unicodedata
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


def buildTags(show, season):
    """gets the episode details in unicode and converts them
        to tags for the episode in blogger"""
    # The tags are not decoded to unicode throug IFTTT
    # and you can not send them in unicode, because
    # appengine encodes them in base64, and IFTTT doesn't
    # undestand that

    # UNICODE Version. just testing how it works
    #tags = u'automagicoespialidoso,{0},{1}'.format(
    #                            show,
    #                            u'Temporada ' + unicode(season))

    # ASCII Version. It works, but the letters dissapear
    #tags = "automagicoespialidoso,{0},{1}".format(
    #                            show.encode("utf-8"),
    #                            "Temporada " + str(season))

    # The ideal case, is to find a function that converts from 
    # unicode to ascii, nicely
    showstr = unicodedata.normalize('NFKD', show).encode('ascii', 'ignore')
    tags = "automagicoespialidoso,{0},{1}".format(
                                showstr,
                                "Temporada " + str(season))
    logging.debug
    logging.debug

    return tags


def buildSubject(show, season):
    """ gets the episode details, decode them and build
        a subject for the email, title of the post"""
    # El caso es que con el asunto, si que se re-codifica en unicode
    subject = 'Ver {0} - {1} online {2}'.format(
                        show.encode("utf-8"),
                        str(season),
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
                subject = self.buildSubject(epObj)
                # - We send it to IFTTT to create the post
                to = "trigger@ifttt.com"
                # - send a copy to the mail account - try to post by email also
                cc = "capitulizer.mail@gmail.com, capitulizer.mail.icanhazpozt@blogger.com"
                # - The body tags are the boy of the message, that we use to send
                # - the tags of the episode
                bodyTags = self.buildTags(epObj)
                logging.debug("subject")
                logging.debug(repr(subject))

                # WARN: we can reach the size limit for task parameters
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


    def buildTags(self, epObj):
        show = epObj.getDetails()["tvshow"]
        season = epObj.getDetails()["season"]
        tags = buildTags(show, season)
        return tags


    def buildSubject(self, epObj):
        """ gets the details in unicode and pass them to
            the function that really builds the subject"""
        show = epObj.getDetails()["tvshow"]
        season = epObj.getDetails()["season"]
        subject = buildSubject(show, season)
        return subject


