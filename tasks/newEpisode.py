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
import extract
import searcher


class NewEpisodeHandler(webapp2.RequestHandler):
    def post(self):
        try:
            # - get the params
            episodeLink = self.request.get('episodeLink')
            submitter = self.request.get('submitter')
            logging.debug(episodeLink)
            episodeLink = extract.buildLink(episodeLink)  # make sure link its ok
            logging.debug("Creating new Episode")
            logging.debug(episodeLink)

            # - we create an object to store the episode data
            epObj = episode.episode(link=episodeLink)
            epObj.submitter = submitter

            # - to retrieve the links to intermediate, we need to
            # - get the webcontent
            logging.debug("opening a website")
            episodeWeb = extract.openWebsite(episodeLink)
            # extract the interlinks
            linksInter = extract.interLinks(episodeWeb)

            # - and the data of the episode
            details = extract.episodeDataFromEpisodeWeb(episodeWeb)
            logging.debug("details")
            logging.debug(repr(details))

            # - and a cool picture too
            try:
                picture = self.getImageLink(details)
            except:
                logging.error("Something happened in newEpisode with the picture")
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
                # first put the episode
                logging.debug("saving - newEpisodeHandle:48")
                try:
                    # - check for duplicates must be done outside transaction.
                    episodes = epObj.all()
                    logging.debug("Episodes ")
                    logging.debug(episodes)
                    dupes = False
                    for epi in episodes:
                        if epi.link == self.link:
                            dupes = True
                    # - save
                    if dupes == False:
                        logging.debug("Saving the episode")
                        epObj.put()
                    else:
                        # - Raise a "duplicate" exception.
                        # - This should make the task fail permanently
                        raise Exception("Duplicate Episode")

                except Exception as e:
                    # - catch the Duplicate Exception, and fail permanently
                    logging.error("Duplicate Object or DDBB error. Giving Up")
                    logging.error(e.args)
                    # - using taskqueue errors
                    raise taskqueue.TaskAlreadyExistsError

                # then get the key
                keyEpisode = epObj.key()
                # and give it away
                return keyEpisode
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

            keyEpisode = db.run_in_transaction(putEpisode, epObj)
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

    def getImageLink(self, details):
        ss = searcher.image.getLink(self.buildSearch(details),
                                             "91.142.222.222")
        logging.debug("search String")
        logging.debug(ss)
        return ss

    def buildSearch(self, details):
        """ Build a search string for an image """
        restrictions = u'inurl:blogspot '
        if details["tvshoe"] != u'':
            return details["tvshow"] + restrictions
        else:
            raise ValueError("No tvshow data in image search")



