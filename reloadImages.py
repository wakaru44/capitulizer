# sketch to reload all images


import logging

from google.appengine.ext import db
#from google.appengine.api import taskqueue # see raise taskqu
import webapp2

import episode
import searcher



class reloaderHandler(webapp2.RequestHandler):

    def get(self):
        #self.epObjs = episode.episode.all
        self.epObjs = db.GqlQuery("SELECT * FROM episode")
        self.recorrer_todos_los_episodios()

    def replace_picture(self, episode, nuPic):
        episode.picture = nuPic
        episode.put()
        

    def recorrer_todos_los_episodios(self):
        for epObj in self.epObjs:
            imgLink = epObj.picture
            try:
                if imgLink == None or imgLink == "":
                    imgLink = "imagen vacia"

                if "blogspot" not in imgLink:
                    # - repeat the search and replace the link in db
                    logging.debug("existing details")
                    logging.debug(epObj.details)
                    logging.debug("existing image")
                    logging.debug(epObj.picture)

                    newImgLink = searcher.image.getLink(epObj.getDetails())
                    logging.debug("new image")
                    logging.debug(newImgLink)

                    db.run_in_transaction(self.replace_picture, epObj, newImgLink)

                else:
                    # - the links does not need to be replaced
                    logging.info("el episodio ya tiene una imagen bonita")
                    logging.info(epObj.picture)
                    #raise taskqueue.TaskAlreadyExistsError
                    # Comentamos esto , puesto que por ahora no es tarea 
            except:
                logging.error("There was an error with an image")

