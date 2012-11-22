#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####################################
# Date: 2012 10 24
###########################################
#    Frontend of capitulizer application
###########################################
import webapp2
from google.appengine.ext import db

import jinja2
import os

import episode  # it's actually used, but not declared explicitly.

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))


class CapHandler(webapp2.RequestHandler):

    def render(self, values, template="error.html"):
        """render the values in the template.
            by default it goes to the index page"""
        template = jinja_environment.get_template(template)
        self.response.out.write(template.render(values))

    def get(self):

        queriedEpisodes = db.GqlQuery("SELECT * FROM episode ")
        episodeObjs = []
        for q in queriedEpisodes:
            q.addLista()
            episodeObjs.append(q.link)

        output = {'title': "Maquinavajo!",
                  'episodeObjs': queriedEpisodes}

        # And output the thing out
        self.render(output, "capitulizer.html")

    def post(self):
        pass


class BloggerHandler(webapp2.RequestHandler):
    # TODO: this is just a clone. There are better ways to change just a layout.

    def render(self, values, template="error.html"):
        """render the values in the template.
            by default it goes to the index page"""
        template = jinja_environment.get_template(template)
        self.response.out.write(template.render(values))

    def get(self):

        queriedEpisodes = db.GqlQuery("SELECT * FROM episode ")
        episodeObjs = []
        for q in queriedEpisodes:
            q.addLista()
            episodeObjs.append(q.link)

        output = {'title': "Maquinavajo!",
                  'episodeObjs': queriedEpisodes}

        # And output the thing out
        self.render(output, "blogger.html")

    def post(self):
        pass
