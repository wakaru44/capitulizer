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

import episode  # it's actually used, but not declared explicitly.

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../templates"))
logging.debug("The path for templates is")
logging.debug(os.path.dirname(__file__) + "../templates")


class AdminHandler(webapp2.RequestHandler):

    def renderAndWrite(self, values, template="error.html"):
        """render the values in the template.
            by default it goes to the index page"""
        template = jinja_environment.get_template(template)
        self.response.out.write(template.render(values))

    def get(self):
        """Just print a list of all episodes"""
        theQuery = self.request.get('q')
        logging.info("The sent query is:")
        logging.info(theQuery)
        if theQuery == None or theQuery == "":
            theQuery = "SELECT * from episode "

        queriedEpisodes = self.do_query(theQuery)
        output = {'myQuery' : theQuery,
                  'episodeObjs': queriedEpisodes}
        self.renderAndWrite(output, "admin.html")

    def post(self):
        """Does the magic...
        - show selected episodes
        - check for dupes
        - etc
        """
        theQuery = self.request.get("myQuery")
        renderAndWrite(do_query(theQuery),"admin.html")
        #- we should find out wich button was presssed

        #- take the parameters with the request

        #- and send to the corresponding action

        #- the action will render.



    def do_query(self, query = "SELECT * FROM episode "):
        """Do a query to the db and return the list of results"""
        queriedEpisodes = db.GqlQuery(query)
        episodeObjs = []
        for q in queriedEpisodes:
            q.deserializeDetails()
            episodeObjs.append(q.link)
        # link mode
        # return episodeObjs
        # raw objects
        return queriedEpisodes
        
    def is_dupe(self, newEpisode):
        """Checks if the episode is already in db"""
        fails = newEpisode.all().filter('link =',
                                        newEpisode.link).fetch(limit=100)
        return len(fails)

