#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm

import webapp2
from google.appengine.api import taskqueue
from google.appengine.api import mail


class NewEmailHandler(webapp2.RequestHandler):

    def retrieve_episode_object(self, key):
        pass # TODO

    def episode_has_videos(self, keyEpisode = None):
        pass

    def video_queue_empty(self):
        """check that the queue of newVideo is empty"""
        queue = taskqueue.Queue() # newVideos
        #queueStats = taskqueue.QueueStats(queue, ['newVideo'], 2)
        # new way
        queueStats = queue.fetch_statistics()  # returns QueueStatistics
        if queueStats.OldestETA == 0:
            return True
        else:
            return False

    def send_mail_to_admin(self): 
        try:
            sender = "Capitulizer Mighty Bot <botman@capitulizer.appspotmail.com>"
            to = "wakaru44@gmail.com"  # By now, send them to the admin TODO
            subject = "New Episode Available to Watch"
            body  = """<html><h1>This shoul be like the /blogger template.</h1>
            http://capitulizer.appspot.com/blogger</html>"""
        except:
            logging.error("CRITICAL - could not send email")


    def episode_videos_added(self):
        pass
        # TODO: implement this

    def post(self):
        """In this task, we should watch an episode entity
            and maybe check the task queue for the new completed
            episode. and then send an email to the submitter"""

        keyEpisode = self.request.get('keyEpisode')
        # get the episode from the database
        episode_object = self.retrieve_episode(keyEpisode)

        # check if this episode has videos
        self.episode_has_videos(keyEpisode)

        # check if all this episode videos have been added or failed
        self.episode_videos_all_added() # Not Implemented
        if self.video_queue_empty():
            logging.debug("There are no pending video tasks")
            # so send an email
            self.send_mail_to_admin()
        else:
            logging.debug("There are still some video tasks to complete")
            # so retry
            raise Exception("Still new videos waiting. Maybe next time...")


        #return 0

    def get(self):
        self.response.out.write("Welcome")
