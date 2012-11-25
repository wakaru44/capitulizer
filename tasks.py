#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
# Date: 2012 10 24
###########################################

import webapp2

# Import the application scripts
import task_newEpisode
import task_newEmail
import task_newVideo
import task_watchNotify
import task_sendEmail
import task_newPost


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('''<h1>Capitulizer Beta :: Tasks List</h1>.\n
                        <ul>
                            <li>agregate tasks through email</li>
                        </ul>
                        ''')

app = webapp2.WSGIApplication([
    ('/tasks/newEpisode', task_newEpisode.NewEpisodeHandler),
    ('/tasks/newEmail', task_newEmail.NewEmailHandler),
    ('/tasks/newVideo', task_newVideo.NewVideoHandler),
    ('/tasks/watchNotify', task_watchNotify.WatchNotifyHandler),
    ('/tasks/sendEmail', task_sendEmail.SendEmailHandler),
    ('/tasks/newPost', task_newPost.NewPostHandler),
    ('/tasks/', MainHandler),
    ('/tasks', MainHandler)
], debug=True)
