#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####################################
# Date: 2012 10 24
###########################################
#    Frontend of capitulizer application
###########################################
import os
import webapp2
from google.appengine.ext import db

import jinja2
import logging


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../templates"))
logging.debug("The path for templates is")
logging.debug(os.path.dirname(__file__) + "../templates")


class CamsHandler(webapp2.RequestHandler):
    # TODO: this is just a clone of a handler. There are better ways to change just a layout.

    def renderAndWrite(self, values, template="error.html"):
        """render the values in the template.
            by default it goes to the index page"""
        template = jinja_environment.get_template(template)
        self.response.out.write(template.render(values))

    def get(self):

        queriedEpisodes = db.GqlQuery("SELECT * FROM episode ")
        episodeObjs = []
        for q in queriedEpisodes:
            q.deserializeDetails()
            logging.debug(q.detailsDict)
            episodeObjs.append(q)




        output = {'title': "Maquinavajo!",
                  'episodeObjs': episodeObjs }

        # And output the thing out
        self.renderAndWrite(output, "cams.html")

    def post(self):
        pass
