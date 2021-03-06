#!/usr/bin/python
# -*- coding: utf-8 -*-
# Definition of the episode object

import logging
import json
#import datetime
from google.appengine.ext import db


class episode(db.Model):
    """An episode represents the concept of a tv show episode.
        It can have many links to many videos in different providers,
        For now, it can only be listed in SeriesYonkis.com or SeriesCoco.com,
        In the future, we plan to add more websites """

    def __str__(self):
        return self.link

    addedDate = db.DateProperty(auto_now_add=True)
    updatedDate = db.DateProperty(auto_now=True)
    link = db.LinkProperty(required=True)
    title = db.StringProperty()
    description = db.StringProperty()
    videos = db.StringListProperty()  # a string list to save videos
    details = db.StringProperty()  # a json string of a dictionary
    picture = db.StringProperty()  # the url to an image

    ## Future interesting data
    submitter = db.EmailProperty  # save the submitter email for future alerts
    objeto = db.ReferenceProperty  # here we can save the links to the videos?
    detailsDict = {}

    def addVideo(self, link, provider="Video Online"):
        """add a link to a video to the list"""
        # TODO: If we want to store the provider name (and we do)
        # this has to be serialized, converted to object, or
        # something, before saving
        if link is not None:
            # using the appengine db.stringlistproperty
            self.videos.append(link)
        if provider:
            # should store the provider of the video
            # TODO: find a way to store both snnippets of data in the same place
            pass

    def addTitle(self, t):
        """add the title property"""
        if t:
            self.title = t
        else:
            logging.debug("No title to add")


    def addDesc(self, text):
        """adds a description text"""
        if text:
            self.description = text
        else:
            logging.error("no description given")


    def addDetails(self, details):
        """Add the details of the episode to the property.
        It has to convert the dictionary to json string"""
        self.details = json.dumps(details)
        self.detailsDict = details


    def getDetails(self):
        """Get the details from the episode and return a
           dict of the contents"""
        if self.details is not None:
            return json.loads(self.details)
        else:
            return {}

    def addPicture(self, link):
        self.picture = link

    def deserializeDetails(self):
        """Here be dragons. This is a big mistake, creating the object
        episode, or the way i use jinja.
        Because the details are saved in json, they need to be deserialized
        before showing...
        It would be nice to serialize and deserialize automagicly"""
        if self.details is not None:
            self.detailsDict = self.getDetails()


    # DONE: this should be in the episode object's method test
    def all_the_same_by_link(self):
        """find all the duplicates of this episode"""
        others = []
        for ep in self.all():
            if self.link == ep.link:
                others.append(ep)
        return others



