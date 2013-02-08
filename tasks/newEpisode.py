#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm
# we want task to aleviate the effort of parsing the emails and the episodes
# from our main request, so it wont get interrupted

import logging
import webapp2
from google.appengine.api import taskqueue
from google.appengine.ext import db

import episode
import extractSY
import searcher


class NewEpisodeHandler(webapp2.RequestHandler):
    def post(self):
        try:
            # - get the params
            episodeLink = self.request.get('episodeLink')
            submitter = self.request.get('submitter')
            logging.debug(episodeLink)
            episodeLink = extractSY.buildLink(episodeLink)  # make sure link its ok
            logging.debug("Creating new Episode")
            logging.debug(episodeLink)

            # - we create an object to store the episode data
            epObj = episode.episode(link=episodeLink)
            epObj.submitter = submitter

            # - to retrieve the links to intermediate, we need to
            # - get the webcontent
            logging.debug("opening a website")
            episodeWeb = extractSY.openWebsite(episodeLink)
            # extract the interlinks
            linksInter = extractSY.interLinks(episodeWeb)

            # - and the data of the episode
            details = extractSY.episodeDataFromEpisodeWeb(episodeWeb)
            logging.debug("details")
            logging.debug(repr(details))

            # - and a cool picture too
            try:
                picture = self.buildSearch(details)
            except:
                logging.error("Something happend in newEpisode with the picture")
                logging.info("trying again")
                raise

            epObj.addTitle(details["fullTitle"])
            epObj.addDesc(details["description"])
            epObj.addDetails(details)
            epObj.addPicture(picture)

            # We use a function to store the object in a single transaction
            def putEpisode(epObj):
                """ put the episode instance in the bd and return the key.
                    Ensure that we are not writing it twice, etc..."""
                    # TODO this is still a sketch. should improve soon
                #try:
                # first put the episode
                logging.debug("saving - newEpisodeHandle:48")
                try:
                    epObj.save()
                    #logging.debug("--------- ** real transaction ** --------")  # noisy
                except Exception as e:
                    # catch the Duplicate Exception, and fail permanently
                    logging.error("Duplicate Object. Giving Up")
                    logging.error(e.args)
                    # Option 1: using deferred library
                    #raise deferred.PermanentTaskFailure
                    # Option 2: using taskqueue errors
                    raise taskqueue.TaskAlreadyExistsError

                # then get the key
                # TODO 1 : This fails, because queries are not allowed in
                # transactions
                #keyEpisode = epObj.key()
                # and give it away
                # TODO 1 : this should return someting, fail, etc
                #return keyEpisode
                # QUESTION how can i catch Timeout?
                #except  (Timeout, TransactionFailedError, InternalError) as err:
                #    # TO-DO catch errors puttin in bd
                #    logging.error("Error Putting episode in the bd")
                #    logging.error(err)
                #    raise Exception(err)
                #NOTE: add the serialized details dictionary to episode
                # attributes

            # put the episode in the bd and get the key in a transaction
            if len(linksInter) == 0:
                logging.error("There are no videos found, so it doesn't deserve to be saved")
                logging.info("trying again")
                raise Exception

            #keyEpisode = db.run_in_transaction(putEpisode, epObj)
            db.run_in_transaction(putEpisode, epObj)
            keyEpisode = epObj.key()
            queue = taskqueue.Queue('watchNotify')
            task = taskqueue.Task(url='/tasks/watchNotify',
                                  params={'keyEpisode': keyEpisode,
                                          'submitter': submitter,})
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
                    logging.error("We still have a limit set")
                    break
        #except TypeError as err:
        except TypeError:
            #logging.error(err)
            logging.info("trying again")
            raise
        #except :
        #    # TODO handle key errors in the request, to die completly and notify
        #    logging.error("Error adding the episode")
        ##    pass

    def get(self):
        self.response.out.write("welcome")


    def buildSearch(self, details):
        """ Build a search string for an image """
        ss = searcher.image.getLink(details["tvshow"],
                                             "91.142.222.222" )
        logging.debug("search String")
        logging.debug(ss)
        return ss


