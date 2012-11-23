#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm

import webapp2
from google.appengine.api import taskqueue
from google.appengine.api import mail


class NewEmailHandler(webapp2.RequestHandler):

    def post(self):
        """In this task, we should watch an episode entity
            and check the task queue for the new completed
            episode. then, create a new task to send the email. """



        keyEpisode = self.request.get('keyEpisode')
        # get the episode from the database

        # check if this episode has videos. (Trick for the earliest version)

        # check if all this episode videos have been added or failed 
        # (second version)
        queue = taskqueue.Queue() # newVideos
        #queueStats = taskqueue.QueueStats(queue, ['newVideo'], 2)
        # new way
        queueStats = queue.fetch_statistics()  # returns QueueStatistics

        if queueStats.OldestETA == 0:
            logging.debug("There are no pending video tasks")
            # so send an email

            sender = "Capitulizer Mighty Bot <botman@capitulizer.appspotmail.com>"
            to = "wakaru44@gmail.com"  # By now, send them to the admin TODO
            cc = "finesasturiano@gmail.com"  # and send a copy to someone TODO
            subject = "New Episode Available to Watch"
            body  = """<html><h1>This shoul be like the /blogger template.</h1>
            http://capitulizer.appspot.com/blogger</html>"""


            # Old version, sending the mail from here.
            # mail.send_mail(sender, to, subject, body)
            # New version, creating a new task
            # QUESTION: could this way be more maintenable and powerful?
            # QUESTION: Will we reach the size limit for task parameters??
            queue = taskqueue.Queue('sendEmail')
            task = taskqueue.Task(url='/tasks/sendEmail', 
                                  params={'sender': sender,
                                          'subject': subject,
                                          'body': body,
                                          'cc': cc,
                                          'to': to})
            queue.add(task)


        else:
            logging.debug("There are still some video tasks to complete")
            # so retry
            raise Exception("Still new videos waiting. Maybe next time...")


        return 0 

    def get(self):
        self.response.out.write("Welcome")
