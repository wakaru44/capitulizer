#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
# Date: 2012 10 24
###########################################

import webapp2

# Import the application scripts
import tasks.newEpisode
import tasks.newVideo
import tasks.watchNotify
import tasks.sendEmail
import tasks.newPost


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('''<h1>Capitulizer Beta :: Tasks List</h1>.\n
                        <ul>
                            <li>agregate tasks through email</li>
                        </ul>
                        ''')

app = webapp2.WSGIApplication([
    ('/tasks/newEpisode', tasks.newEpisode.NewEpisodeHandler),
    ('/tasks/newVideo', tasks.newVideo.NewVideoHandler),
    ('/tasks/watchNotify', tasks.watchNotify.WatchNotifyHandler),
    ('/tasks/sendEmail', tasks.sendEmail.SendEmailHandler),
    ('/tasks/newPost', tasks.newPost.NewPostHandler),
    ('/tasks/', MainHandler),
    ('/tasks', MainHandler)
], debug=True)
