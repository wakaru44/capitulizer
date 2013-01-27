# sketch to reload all images

import episode
import searcher

epObjs = episode.episode.all

for epObj in epObjs:
    imgLink = epObj.imgLink
    if "blogspot" not in imgLink:
        # - repeat the search and replace the link in db
        newImgLink = searcher.image.getLink(epObj.details)

    else:
        # - the links does not need to be replaced
        raise taskqueue.TaskAlreadyExistsError
