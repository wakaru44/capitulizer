#!/usr/bin/python
# -*- coding: utf-8 -*-

# 17-nov-2012 juanantoniofm

import webapp2
import logging
from google.appengine.ext import db
import extractSY
import episode

class NewVideoHandler(webapp2.RequestHandler):


#    def __init__(self, request, response):
#        logging.error("request")
#        logging.error(request)
#        logging.error("response")
#        logging.error(response)
#        super(NewVideoHandler, self).__init__(request, response)

    def post(self):
        """This task is responsible for adding the video links
            to an episode. If we are detected like robots, retry
            if the link is broken, or we try for many time, 
            warn the submitter about the error in some way"""
        # TODO: ^^^^ maybe storing the broken link, and send it in brief

        try:
            logging.debug("newVideoHandler")
            # get the key to episode to retrieve from db
            keyEpisode = self.request.get('keyEpisode')
            # get the link to the intermedia website
            interLink = self.request.get('interLink')  

            # extract the link to the video and the data 
            # try to get the shortened link to the video
            # and add it to the object
            interWeb = extractSY.openWebsite(interLink)

            logging.debug("interWeb type")
            logging.debug(type(interWeb))

            vLink, vProv = extractSY.linkToVideoAndProvFromInterLink(
                                                              interWeb)
            # save the video link in the episode entity
            # I use a function to work with the bd in a single transaction
            self.keepThatShit(keyEpisode, vLink, vProv)
            #logging.debug("****40****")  # noisy
            

        except:
            # TODO 1: define a imARobotException
            # TODO : catch errors getting request parameters
            # if we are detected like robots, fail to retry
            logging.error("Couldn't handle this")
            raise 


        #return 0


    def keepThatShit(self, keyEpisode, vLink, vProv  ):

        try:
            # I use a function to work with the bd in a single transaction
            def saveVideo(keyEpisode, vLink, vProv):
                # retrieve the object from the bd
                epObj = db.get(keyEpisode)
                if epObj and vLink != "":
                    epObj.addVideo(vLink, vProv)
                    #logging.debug(vLink)
                    logging.debug("saving that video for this episode in the datastore")
                    logging.debug(epObj)
                    epObj.put()
                else:
                    # if there is no object retrieved, fail the trasaction.
                    # QUESTION isn't a better way to see that it failed? i don't 
                    # know how to catch a exception or something for that 
                    # kind of failure
                    logging.debug("vLink")
                    logging.debug(vLink)
                    logging.debug("epObj")
                    logging.debug(epObj)
                    raise Exception("We wont store this video.")

            db.run_in_transaction(saveVideo, keyEpisode, vLink, vProv)
            #logging.debug("****90****")  # noisy

        except db.datastore_errors as e:
            # TODO : catch error getting the thing from db
            logging.error("Error getting episode from bd")
            #logging.error(e)
            logging.debug(dir(e))
        except db.datastore_errors.BadKeyError as e:
            # QUESTION sure that's ok folk?
            logging.error("Error getting episode from bd.BadKeyError")
            #logging.error(e)
            #raise db.datastore_errors.BadKeyError
            raise 
        except NameError as e:
            logging.error("Maybe not link found")
            logging.error(e)
        except Exception as err:
            # TODO 1: define a imARobotException
            # if we are detected like robots, raise again to retry
            # TODO : catch errors getting request parameters
            logging.error("Couldn't handle this")
            logging.error(err)
            #raise 

        # save the video link in the episode entity

#        return 0


    def get(self):
        self.response.out.write("Welcome")
