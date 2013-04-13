#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm
# we want task to aleviate the effort of parsing the emails and the episodes
# from our main request, so it wont get interrupted
############
# NOTAS:
# Este archivo esta siendo reescrito. por el momento hemos separado el metodo
# post en varios submetodos, con trucos guarros como tirar de self. para las
# variables. Ahora hay que limpiar esas variables, y empezar a hacer que sean
# parametros y returns de cada metodo.

import logging
import webapp2
from google.appengine.api import taskqueue
from google.appengine.ext import db

import episode
import extract
import searcher


class NewEpisodeHandler(webapp2.RequestHandler):

    def get_params(self):
        try:
            episodeLink = self.request.get('episodeLink')
            submitter = self.request.get('submitter')  #TODO:remove this
            episodeLink = extract.buildLink(episodeLink)  # make sure link its ok
            logging.debug("Creating new Episode")
            logging.debug(episodeLink)
            return (episodeLink, submitter)
        except:
            raise # TODO if no link given should we fail permanently?


    def create_object(self, link = "", submitter = "" ):
        try:
            # - we create an object to store the episode data
            self.epObj = episode.episode(link=link)
            return self.epObj
        except:
            raise # TODO


    def get_episode_data(self, episodeLink = ""):
        try:
            # - to retrieve the links to intermediate, we need to
            # - get the webcontent
            logging.debug("opening a website")
            episodeWeb = extract.openWebsite(episodeLink)
            # extract the interlinks
            self.linksInter = extract.interLinks(episodeWeb)
            # - and the data of the episode
            self.details = extract.episodeDataFromEpisodeWeb(episodeWeb)
            logging.debug("details")
            logging.debug(repr(self.details))
            return self.details, self.linksInter


        except:
            raise  # TODO

    def get_episode_picture(self, details = None):
        """Get a picture from google"""
        try:
            # - and a cool picture too
            picture = searcher.image.getLink(details, "91.142.232.122")
            return picture
        except:
            logging.error("Something happened in newEpisode with the picture")
            logging.info("trying again")
            raise # as is 


    def populate_episode_object(self, episode_object = None,  details = {},
                                picture = None, submitter = None):
        try:
            episode_object.addTitle(details['fullTitle'])
            episode_object.addDesc(details['description'])
            episode_object.addDetails(details)
            if picture != None:
                episode_object.addPicture(picture)
            else:
                raise ValueError("No picture given")
            episode_object.submitter = submitter
            return episode_object
        except:
            raise  # TODO

    def putEpisode(self, epObj):
        """ put the episode instance in the bd and return the key.
            Ensure that we are not writing it twice, etc..."""
        # We use a function to store the object in a single transaction
        # first put the episode
        logging.debug("saving")
        try:
            epObj.put()
        except Exception as e:
            # - catch the Duplicate Exception, and fail permanently
            logging.error("Duplicate Object or DDBB error. Giving Up")
            logging.error(e.args)
            # - using taskqueue errors
            raise taskqueue.TaskAlreadyExistsError
        # then get the key and give it away
        keyEpisode = epObj.key()
        return keyEpisode
        
    def is_dupe(self, episode_link):
        # - check for duplicates must be done outside transaction.
        # TODO: this should be in the episode object's method
        episodes = episode.episode.all()
        logging.debug("Episodes ")
        logging.debug(episodes)
        dupes = False
        for epi in episodes:
            dir(self)
            if epi.link == episode_link:
                dupes = True
        return dupes


    def deserves_to_be_saved(self, linksInter = 0):
        if len(self.linksInter) == 0:
            logging.info("No videos found. Trying again")
            return False
        else:
            return True


    def create_watch_task(self, keyEpisode = "", submitter = ""):
        try:
            queue = taskqueue.Queue('watchNotify')
            task = taskqueue.Task(url='/tasks/watchNotify',
                                  params={'keyEpisode': keyEpisode,
                                          'submitter': submitter,})
            queue.add(task)
        except:
            raise  # TODO


    def create_videos_tasks(self, linksInter = [], keyEpisode = ""):
        try:
            # create newVideo tasks to add videos to the episode.
            limit = 30    # TODO eliminate this limit. is horrible, sucker
                          #if we want to set a limit, we should do it better
            # with the interlinks, get some data
            for linkInter in linksInter:
                # TODO: rename linkInter to interLink
                limit -= 1
                # build a link if its not complete
                linkInter = extract.buildLink(linkInter)
                # and dont get past the limit
                if limit > 0:
                    # Call a newVideo task for each interlink
                    queue = taskqueue.Queue('newVideo')
                    task = taskqueue.Task(url='/tasks/newVideo',
                                  params={'keyEpisode': keyEpisode,
                                          'interLink': linkInter})
                    queue.add(task)

                else:
                    logging.error("We still have a limit set")
                    break
        except:
            raise  # TODO

    def check_and_save(self, epObj = None, linksInter = 0):
        """check if the episode should be saved or not"""
        if epObj == None:
            raise TypeError("Not an episode")
        if not self.deserves_to_be_saved(linksInter):
            raise Exception

        if not self.is_dupe():
            logging.debug("Saving the episode")
            keyEpisode = db.run_in_transaction(self.putEpisode, epObj)
            return keyEpisode
        else:
            # - Raise a "duplicate" exception.
            # - This should make the task fail permanently
            logging.error("Duplicate Episode. Permanent Fail")
            raise Exception("Duplicate Episode")



    def post(self):
        episodeLink, submitter = self.get_params()
        episode_object = self.create_object(episodeLink)
        #- get the data and pictures for the object
        episode_details, linksInter = self.get_episode_data(episodeLink)
        picture = self.get_episode_picture( episode_details )
        self.populate_episode_object(episode_object, episode_details, picture , submitter) 

        #- check if we have everything and save it 
        keyEpisode = self.check_and_save(self.epObj, linksInter)  # TODO: the
        # problem with this method is even in the name. It has to do too many
        # things for a simple method. It should be splitted.
        #- create tasks
        self.create_watch_task(keyEpisode, submitter)
        self.create_videos_tasks(linksInter, keyEpisode)

    def get(self):
        self.response.out.write("welcome")
