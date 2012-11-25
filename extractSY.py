#!/usr/bin/python
# -*- coding: utf-8 -*-


# Library to extract data from SY website.
import logging

import time
import random
import urllib2
import bs4

# minimum wait time in seconds
MINIMUM_WAIT_TIME = 2
MAXIMUM_WAIT_TIME = 12


def openWebsite(link):
    """opens a website. We have this function so we can modify the way we get
    the websites easyly (like the time to wait betwen requests)"""
    try:
        logging.debug("opening website " + link)
        w = openLink(link)
        return w.read()
    except urllib2.URLError as e:
        logging.error("Error opening website")
        raise urllib2.URLError


def openLink(link):
    """open a link and return the redirection. I do this in a separate 
    function, besides the overkill, to get the sleep time apart, and
    maybe, join all the urllib request in the same function."""
    humanizer = int(random.random() * (MAXIMUM_WAIT_TIME - MINIMUM_WAIT_TIME))
    time.sleep(MINIMUM_WAIT_TIME + humanizer)
    userAgents = ['Amiga-AWeb/3.4.167SE ', 
                   'Mozilla/5.0']
    pickOneUserAgent = userAgents[int((random.random() * 10 )
                                        % len(userAgents) )]
    logging.debug("user agent")
    logging.debug(pickOneUserAgent)
    try:
        #headers = { 'User-Agent' : pickOneUserAgent }
        # safe - mode
        # headers = { 'User-Agent' : 'Mozilla/5.0'}
        # UNsafe - mode TODO
        headers = { 'User-Agent' : pickOneUserAgent}
        rqst = urllib2.Request(link, None, headers)
        w = urllib2.urlopen(rqst)
        return w
    except urllib2.URLError as e:
        logging.error("Could't get the link. Url ERROR")
        logging.error(e)
        logging.error(headers)
        logging.error(repr(link))
        # not quite sure about raising it again.
        # by now, this will make the task to be retried.
        raise urllib2.URLError(e)  # REMOVE - added to raise better 


def buildLink(link):
    """check that is a proper www.seriescoco.com link"""
    logging.debug("building link: ")  # noisy
    logging.debug(repr(link))  # noisy
    if "seriesyonkis" in link or "seriescoco" in link:
        return link
    else:
        return "http://www.seriescoco.com" + link


def plainString(s):
    """gets a beautifulSoup Element down to its string
        If thats just easy, do it in unicode madafaca"""
    # as excuse for the comentary, i would say that
    # i wrote this as a solution to a supposed encoding problem
    madafaca = u''
    for snip in s:
        if isinstance(snip, unicode):
            # if its an unicode string, we add it
            madafaca += snip
        else:
            # if its something else, is probably a bs4 tag
            #logging.debug("entity kind")  # noisy
            #logging.debug(type(snip))  # noisy
            if isinstance(snip, bs4.element.Tag):
                #logging.debug("is a tag")  # noisy
                madafaca += snip.prettify().strip()
                # madafaca += snip.__str__() # this method fails sometimes
                                            # giving unicode errors
            elif isinstance(snip, bs4.NavigableString):
                #logging.debug("is a navigable string")  # noisy
                madafaca += snip.__str__().strip()
            else:
                logging.error("is unaputamierda")
                #logging.debug(snip)  # noisy
    madafaca = madafaca.replace("\n","")
    return madafaca


def amIARobot(web):
    """checks that the web content is not a captcha website."""
    # TODO: this should be a little bit smartter
    # for example, it should check if the text is in some place
    # if not, this will give false positives
    if "comprobar que eres humano" in web:
        return True
    else:
        return False


def linksToEpisodes(msg):
    """extract the episode links from the mail"""
    logging.debug("linkstToEpisodes has Received:")
    #logging.debug(msg) #  too many output
    episodeList = []

    if "seriesyonkis" or "seriescoco" in msg:
        logging.debug("it seems a seriesyonkis kind of email")
        # SY especifics
        # First, we have to clean the message
        # from some weird chars in emails
        syMsg = msg.replace("=\n", "")
        soup = bs4.BeautifulSoup(syMsg)
        for link in soup.find_all("a"):
            # Check that is a "capitulo" kind of link
            # logging.debug("a link found")  # noisy
            # logging.debug(link)  # noisy
            try:
                l1 = link['href']
                l1 = l1.replace('3D"', '')
                cleanLink = l1.replace('"', '')
                if "capitulo" in cleanLink:
                    logging.debug("agregando capitulo a la lista")
                    episodeList.append(cleanLink.decode())
                else:
                    # logging.debug("no agregamos el enlace a la lista")  #
                    # noisy
                    pass
            except KeyError as e:
                #logging.debug("No href Found in Email Message")  # noisy
                #logging.debug(e)  # noisy
                pass

    if len(episodeList) <= 0:
        logging.error("No episodes found in the mail. PLEASE REPORT THIS")
        logging.debug(msg)  # carefull. too much output
    else:
        episodeList = list(set(episodeList))
        episodeList.sort()

    logging.debug(episodeList)
    #lint:disable
    return episodeList
    #lint:enable


def interLinks(web):
    """get the html of an episode page.
    It returns a list with the links to the intermediate pages.
    The origin must be a seriesyonkis o seriescoco page."""
    logging.debug("--- Extracting the interLinks---")

    ## TODO working on it.
    # Note: we are keeping the retrieval of the document out of this function
    # to ease the testing. Will it be the right choice?
    # yes, indeed. it seems the rigth choice by now ;)
    # QUESTION
    linkList = []
    sopa = bs4.BeautifulSoup(web)
    i = 0
    for link in sopa.find_all("a"):
        i += 1
        try:
            if ("ngo" in link['href']) and ("eproducir" in link['title']):
                #logging.debug(link['href'])k
                linkList.append(link['href'])
                #logging("Hemos guardado un enlace")
        except KeyError:
            #logging.debug("Error getting interlinks")
            # TODO: this should not even got logged.
            #       we should log it or break in case no interLinks gotten
            # logging.debug(e) #  irrelevant
            pass 

    if len(linkList) < 1:
        logging.error("No interlinks Found on the website given")
        logging.debug(sopa.find_all("a"))

    return list(set(linkList)) if (len(linkList) > 0) else None


def episodeDataFromEpisodeWeb(web):
    """receives a seriescoco webcontent
        returns the data of the episode"""

    logging.debug("extracting data from episode web")

    fullTitle = u''
    description = u''

    # ERROR - this can lead to a recursion error, if we feed the parser with
    # some kind of crap. QUESTION: how can i check this
    #print "---------------------------------------------------"
    #print web
    #print "---------------------------------------------------"
    soup = bs4.BeautifulSoup(web)
    # I tried it this way, but it was a mistake. it brokes sometimes
    # soup = bs4.BeautifulSoup(web.decode("utf-8"))  # es tonteria ponerlo asi,pero

    # with this loop, we get the info from the episode
    for block in soup.find_all("div"):
        try:
            if "section-intro" in block['class']:
                # get the title
                fullTitle = plainString(block.h1.contents).strip()
                # get the description
                # this way, we plain the string
                #description = plainString(block.div.contents)
                # this way, we use the html
                description = plainString(block.div.contents).strip()

        except KeyError:
            # if we enable loggin for this, would be a stom of log.
            # there should be exceptions in this and its normal.
            # we don't need to catch them.
            pass

    logging.debug("fullTitle")
    logging.debug(fullTitle)
    logging.debug("description")
    logging.debug(description)
    return fullTitle, description



def linkToVideoSY(web):
    # TODO: change this to linkToVideoSYFromInterWeb
    """Takes an intermediate web (in seriesyonkis websites, you
    have to visit an intermediate website with a link to the video).
    returns the link to the video in the SY shortener.
    The returned link, still has to be converted to a link from a video hoster
    The origin must be a seriesyonkis o seriescoco page"""
    sopa = bs4.BeautifulSoup(web)
    for link in sopa.find_all("tr"):
        try:
            if "action_link" in link['class']:
                videoLink = link.a['href']
                #videoProv = link['data-server']
                return videoLink.decode()
        except KeyError as e:
            # logging.debug "err"
            logging.error("Error extracting the link to videoSY")
            logging.error(e)


def providerFromInterWeb(web):
    """Takes an intermediate web (in seriesyonkis websites, you
    have to visit an intermediate website with a link to the video).
    returns the the provider.
    """
    # TODO: should this be merged into linkToVideoSY? would avoid 1 parsing.
    # QUESTION
    sopa = bs4.BeautifulSoup(web)
    logging.debug("providerFromInterWeb type")
    logging.debug(type(web))

    for link in sopa.find_all("tr"):
        try:
            if "action_link" in link['class']:
                # videoLink = link.a['href']
                videoProv = link['data-server']
                return videoProv.decode()
        except KeyError as e:
            # logging.debug "err"
            logging.error("Error extracting the link to videoSY")
            logging.error(e)
        except TypeError as e:
            logging.error("Error extracting the link to VideoSY")
            logging.error(e)
        finally:
            if videoProv:
                pass
            else:
                # TODO: don't really know what im doing here. just trying to
                # not fall appart in a different way.
                # we could choose between None or ""
                return ""


def linkToVideoInProv(link):
    """Takes a link and
        returns the link to the video in the hoster or provider"""
    try:
        originLink = buildLink(link)
        logging.debug("LinkToVideoInProv")
        logging.debug(originLink)
        w = openLink(originLink)
        logging.debug("resultLink")
        logging.debug(w)
        resultLink = w.geturl()
        logging.debug(resultLink)
        if "seriescoco" in resultLink:
            logging.error(
        "Oops, you seem like a robot to them... We couldn't download this:")
            logging.error(resultLink)
            suspect = openWebsite(resultLink)
            if amIARobot(suspect):
                logging.error(originLink)
                raise Exception("CaptCha Alert, you seem like a robot")
            else:
                logging.error("Eror getting video in provider. Check:")
                logging.error(resultlink)
        else:
            FinalLink = resultLink
    except urllib2.HTTPError as err:
        if err.code == '404':
            logging.error("This guys are smart. They send a 404 but its a fake")
            logging.error(w.geturl())
            FinalLink = resultLink
        else:
            logging.error("Could not get a link to video in provider. HTTPError")
            logging.error(repr(w))
            logging.error(repr(w.geturl()))
    except Exception as err:
        logging.error("Could not get a link to video in provider. OTHER Error")
        logging.error(repr(err))
        FinalLink = ""
    finally:
        return FinalLink


def linkToVideoInProvFromEpisodeLink(link):
    """Takes a link to an episode in SY,
        returns a list with links to videos"""
    pass


def linkToVideoAndProvFromInterLink(interWeb):
    """Takes a interlink and
        if no link found, returns empty string
        returns the list of videos in the provider"""
    logging.debug("getting the link to video and the provider of it")
    logging.debug(type(interWeb))
    try:
        SYLink = linkToVideoSY(interWeb)
        if SYLink != "":
            provLink = linkToVideoInProv(SYLink)
        else:
            logging.error("Ups, there was no return from linkToVideoSY extractSY:327")
            provLink = ""
        provName = providerFromInterWeb(interWeb)
        logging.debug("Provider Name: ")
        logging.debug(provName)
        return (provLink, provName)
    except:
        logging.debug("Problem trying to get linkToVideoInProvFromInterLink")
        raise

