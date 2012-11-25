#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm

import webapp2
import logging
from google.appengine.api import taskqueue
from google.appengine.api import mail


class WatchNotifyHandler(webapp2.RequestHandler):

    def post(self):
        """In this task, we should watch an episode entity
            and check the task queue for the new completed
            episode. then, create a new task to send the email. """

        # TODO 1: in the first run, we shoul defer it for later, because if
        # there were no task pending, it will be instantly trigguered :(

        keyEpisode = self.request.get('keyEpisode')
        submitter = self.request.get('submitter')
        # get the episode from the database

        # check if this episode has videos. (Trick for the earliest version)

        # check if all this episode videos have been added or failed 
        # (second version)
        queue = taskqueue.Queue() # newVideos
        #queueStats = taskqueue.QueueStats(queue, ['newVideo'], 2)
        # new way
        queueStats = queue.fetch_statistics()  # returns QueueStatistics

        if queueStats.tasks == 0:
            logging.debug("There are no pending video tasks")
            # so send an email

            sender = "Capitulizer Mighty Bot <botman@capitulizer.appspotmail.com>"
            to = submitter  # send them to the submitter TODO
            cc = ""  # by now, empty string so sending doesnt fail
            bcc = "wakaru44@gmail.com"  # and send a copy to the admin 
            subject = "New Episode Available to Watch"
            # TODO 1: create the notification body 
            body  = """<html><h1>Notification Email Body</h1>
            http://capitulizer.appspot.com/</html>"""


            # Old version, sending the mail from here.
            # mail.send_mail(sender, to, subject, body)
            # New version, creating a new task
            # QUESTION: could this way be more maintenable and powerful?
            # QUESTION: Will we reach the size limit for task parameters??
            logging.debug("Creating task sendEmail")
            queue = taskqueue.Queue('sendEmail')
            task = taskqueue.Task(url='/tasks/sendEmail', 
                                  params={'sender': sender,
                                          'subject': subject,
                                          'body': body,
                                          'cc': cc,
                                          'bcc': bcc,
                                          'to': to})
            queue.add(task)

            logging.debug("Creating task newPost")
            queue = taskqueue.Queue('newPost')
            task = taskqueue.Task(url='/tasks/newPost', 
                                  params={'keyEpisode': keyEpisode
                                          })
            queue.add(task)


        else:
            logging.debug("There are still some video tasks to complete")
            # so retry
            raise Exception("Still new videos waiting. Maybe next time...")


        #return 0 

    def get(self):
        self.response.out.write("Welcome")
