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
                logging.debug("-- has videos --")
                # - start building the email body
                queriedEpisode = [epObj]
                logging.debug("queriedEpisode")
                logging.debug(epObj.title)
                logging.debug(repr(queriedEpisode))
                output = {'title': epObj.title,
                          'episodeObjs': queriedEpisode}

                body = self.renderBody(output, "blogger.html")
                #logging.debug("body")  # noisy
                #logging.debug(body)  # noisy

                # - build the rest of the message
                sender = "Capitulizer Mighty Poster Bot <capitulizer@capitulizer.appspotmail.com>"
                subject = "watch %s online" % epObj.title
                to = "capitulizer.mail@gmail.com"
                cc = "trigger@ifttt.com, wakaru44@gmail.com, capitulizer.mail.icanhazpozt@blogger.com"
                # send a copy to the admin; try to post by email also
                bodyTags = "automagicoespialidoso, %s" % "SERIE AUTOMATIc",epObj.getDetails()["tvshow"]
                logging.debug("subject")
                logging.debug(repr(subject))
                logging.debug(epObj.getDetails()["tvshow"])

                # QUESTION: could this way be more maintenable and powerful?
                # QUESTION: Will we reach the size limit for task parameters??
                logging.debug("Creating a sendEmail Task with a new Post")
                queue = taskqueue.Queue('sendEmail')
                task = taskqueue.Task(url='/tasks/sendEmail',
                                      params={'sender': sender,
                                              'subject': subject,
                                              'to': to,
                                              'cc': cc,
                                              'bodyTags': bodyTags,
                                              'body': body})
                queue.add(task)
            else:
                logging.error("no videos in the database yet. Retrying")
                raise Exception




                # ............................................................
                # TODO 1: .........write over the dotted line ..........

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


    def renderBody(self, values, template="error.html"):
        """render the values in the template.
            by default it goes to the index page"""
        template = jinja_environment.get_template(template)
        return template.render(values)

