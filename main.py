#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
# Date: 2012 10 24
###########################################

import webapp2

# Import the application scripts
import frontend_capitulizer
# import task_newEpisode
# import task_newEmail
# import task_newVideo


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('''<h1>Capitulizer Beta</h1>.\n
                        <ul>
                            <li>Envia un email a agregar at
                            capitulizer.appspotmail.com</li>
                            <li>Entra en 
                            <a href="http://capitulizer.appspot.com/capitulizer">
                                capitulizer
                            </a>
                            </li>
                        </ul>
                        ''')

app = webapp2.WSGIApplication([
    ('/capitulizer', frontend_capitulizer.CapHandler),
    ('/blogger', frontend_capitulizer.BloggerHandler),
    ('/', MainHandler)], debug=True)
