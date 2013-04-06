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
# Third party libraries path must be fixed before importing webapp2
import os, sys

from  wtforms import validators, Form, fields
from wtforms.ext.appengine.db import model_form

import episode  # it's actually used, but not declared explicitly.

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../templates"))
logging.debug("The path for templates is")
logging.debug(os.path.dirname(__file__) + "../templates")


class oldadminForm(Form):
    texto = fields.TextField('Username', [validators.Length(max=40)])

    addedDate = fields.DateField('%Y-%m-%d')
    updatedDate = fields.DateField('%Y-%m-%d')
    link = fields.TextField('Link')
    title = fields.TextField('Title')
    description = fields.TextField('Description')
    #videos = db.StringListProperty()  # a string list to save videos
    videos = fields.TextField('Videos')
    details = fields.TextField('Details')
    picture = fields.TextField('Picture')

    update_picture = fields.SubmitField("update_picture")

class adminForm(Form):
    episodes = []

    def __init__(self, query = "SELECT * FROM episode"):
        #- query the objects
        queried_episodes=db.GqlQuery(query)
        #- populate the form
        for ep in queried_episodes:
            self.episodes.append(model_form(episode.episode(link=ep.link))())
        #- so be it 

class AdminHandler(webapp2.RequestHandler):

    #metodo manual
    form = adminForm()
    # metodo con asistente de wtforms
    #form = model_form(episode.episode)()

    def renderAndWrite(self, values, template="error.html"):
        """render the values in the template.
            by default it goes to the index page"""
        template = jinja_environment.get_template(template)
        self.response.out.write(template.render(values))

    def classicView(self):
        """Just print a list of all episodes"""
        theQuery = self.request.get('q')
        logging.info("The sent query is:")
        logging.info(theQuery)
        if theQuery == None or theQuery == "":
            theQuery = "SELECT * from episode "

        queriedEpisodes = self.do_query(theQuery)
        output = {'myQuery' : theQuery,
                  'episodeObjs': queriedEpisodes}

    def get(self):
        """Print the list of queried objects using wtForms"""
        #- take query if any
        theQuery = self.request.get('q')
        logging.info("The sent query is:")
        logging.info(theQuery)

        #- First, just an example:
            #- inst a form, pass and render to jinja
        #self.renderAndWrite({ "form": self.form , "myQuery": theQuery }, "admin.html")
        #- Second. try to list all my episodes
        self.renderAndWrite({ "form": self.form }, "admin.html")
        
        

    def edit_profile_demo(self, request):
        form = self.form
        # episode = self.get_values(request)  # this shouldn't be necesary in future
        #if form.validate():
        #    epObj = episode.episode(link="http://foo.bar")
        #    #epObj = episode.episode(link=form.link.data)
        #    form.populate_obj(episode)
        #    epObj.save()
        #else:
        #    epObj = episode.episode(link="http://fooo")
        self.renderAndWrite({"megaform":self.form},
                            "admin.html")
        

    def post(self):
        """Does the magic...
        - show selected episodes
        - check for dupes
        - etc
        """
        #theQuery = self.request.get("myQuery")
        #self.renderAndWrite(self.do_query(theQuery),"admin.html")
        #- we should find out wich button was presssed

        #- take the parameters with the request

        #- and send to the corresponding action

        #- the action will render.

        ####################
        # edit profile demo
        self.edit_profile_demo(self.request)

        



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


