#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm
# file for the first task, created as a test.
# we want task to aleviate the effort of parsing the emails and the episodes
# from our main request, so it wont get interrupted

import logging
import webapp2
from google.appengine.api import taskqueue
from google.appengine.ext import db

import episode
import extractSY


class NewEpisodeHandler(webapp2.RequestHandler):
    def post(self):  
        try:
            episodeLink = self.request.get('episodeLink')
            episodeLink = extractSY.buildLink(episodeLink)  # make sure link its ok
            logging.debug("Creating new Episode")
            logging.debug(episodeLink)
            # we create an object to store the episode data
            epObj = episode.episode(link=episodeLink)
            # to retrieve the links to intermediate, we need to
            # get the webcontent
            logging.debug("opening a website")
            episodeWeb = extractSY.openWebsite(episodeLink)
            # extract the interlinks
            linksInter = extractSY.interLinks(episodeWeb)
            # and the data of the episode
            title, description = extractSY.episodeDataFromEpisodeWeb(
                                                              episodeWeb)
            logging.debug("title:")
            logging.debug(title)
            logging.debug("desc:")
            logging.debug(description)

            epObj.addTitle(title)
            epObj.addDesc(description)
     
            def putEpisode(epObj):
                """ put the episode instance in the bd and return the key.
                    Ensure that we are not writing it twice, etc..."""
                    # TODO this is still a sketch. should improve soon
                try:
                    # first put the episode
                    epObj.put()
                    logging.debug("-------------- ** real transaction ** ----------------")
                    # then get the key
                    keyEpisode = epObj.key()
                    # and give it away
                    return keyEpisode 
                except:
                    # TODO catch errors puttin in bd
                    logging.error("Error Putting episode in the bd")
                    raise Exception("error putEpisode")

            # put the episode in the bd and get the key in a transaction
            keyEpisode = db.run_in_transaction(putEpisode, epObj)
            # REMOVE old model, non trasactional
            # epObj.put()
            # get the key to the episode
            # keyEpisode = epObj.key()

            # TODO 1: we should launch the task to watch the episode and notify
            queue = taskqueue.Queue('watchNotify')
            task = taskqueue.Task(url='/tasks/watchNotify',
                                  params={'keyEpisode': keyEpisode,})
            queue.add(task)

            # create newVideo tasks to add videos to the episode.
            limit = 10    # TODO eliminate this limit. is horrible, sucker
                          #if we want to set a limit, we should do it better
            # with the interlinks, get some data
            for linkInter in linksInter:
                # TODO: rename linkInter to interLink
                limit -= 1
                # build a link if its not complete
                linkInter = extractSY.buildLink(linkInter)
                # and dont get past the limit
                if limit > 0:
                    # Call a newVideo task for each interlink
                    queue = taskqueue.Queue('newVideo')
                    task = taskqueue.Task(url='/tasks/newVideo', 
                                  params={'keyEpisode': keyEpisode,
                                          'interLink': linkInter})
                    queue.add(task)

                    # CAREFULL this is meant to be launched once for episode
                    # REMOVE
                    #queue = taskqueue.Queue('newEmail')
                    #task = taskqueue.Task(url='/tasks/newEmail',
                    #                      params={'keyEpisode': keyEpisode,})
                    #queue.add(task)


                else:
                    logging.error(
                        "We still have a limit set")
                    break
        except TypeError as err:
            logging.error("Type Error madafaca")  # TODO just dont remember why...
            logging.error(err)
        #except:
        #    # TODO handle key errors in the request, to die completly and notify
        #    logging.error("Error adding the episode")
        #    pass

    def get(self):
        self.response.out.write("welcome")
