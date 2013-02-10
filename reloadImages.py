# sketch to reload all images


import episode
import searcher
from google.appengine.ext import db
import webapp2



class reloaderHandler(webapp2.RequestHandler):

    def get(self):
        self.epObjs = episode.episode.all
        self.recorrer_todos_los_episodios()

    def replace_picture(self, episode, nuPic):
        episode.picture = newImgLink
        episode.put()
        

    def recorrer_todos_los_episodios(self):
        for epObj in self.epObjs:
            imgLink = epObj.picture
            if "blogspot" not in imgLink:
                # - repeat the search and replace the link in db
                newImgLink = searcher.image.getLink(epObj.details)
                db.run_in_transaction(replace_picture, epObj, newImgLink)

            else:
                # - the links does not need to be replaced
                raise taskqueue.TaskAlreadyExistsError
