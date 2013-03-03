#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
# Date: 2012 10 24
###########################################

import webapp2

# Import the application scripts
import handlers.frontend_capitulizer as frontend_capitulizer
# import task_newEpisode
# import task_newVideo
import reloadImages


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
                            <a href="/reloading"> para recargar las imagenes</a>
                            <a href="/tasks/newPost"> Para crear un nuevo post</a>
                            </li>
                        </ul>
                        ''')

app = webapp2.WSGIApplication([
    ('/capitulizer', frontend_capitulizer.CapHandler),
    ('/blogger', frontend_capitulizer.BloggerHandler),
    ('/reloading', reloadImages.reloaderHandler),
    ('/', MainHandler)], debug=True)
