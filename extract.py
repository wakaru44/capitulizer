#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library to extract data from website.

import logging
import quopri
import time
import random
import urllib2
#import json  # Utilizado para serializar el diccionario con episode Details
# import unicodedata
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
        logging.error(repr(e))
        raise urllib2.URLError


def openLink(link):
    # TEST
    """open a link and return the redirection. I do this in a separate
    function, besides the overkill, to get the sleep time apart, and
    maybe, join all the urllib request in the same function."""
    humanizer = int(random.random() * (MAXIMUM_WAIT_TIME - MINIMUM_WAIT_TIME))
    time.sleep(MINIMUM_WAIT_TIME + humanizer)
    userAgents = ['Amiga-AWeb/3.4.167SE ',
                  'Mozilla/5.0']
    pickOneUserAgent = userAgents[int((random.random() * 10)
                                  % len(userAgents))]
    logging.debug("user agent")
    logging.debug(pickOneUserAgent)
    logging.debug("sy link to get the video in provider")
    logging.debug(link)
    try:
        #headers = { 'User-Agent' : pickOneUserAgent }
        # safe - mode
        # headers = { 'User-Agent' : 'Mozilla/5.0'}
        # UNsafe - mode TODO
        headers = {'User-Agent': pickOneUserAgent}
        rqst = urllib2.Request(link, None, headers)
        w = urllib2.urlopen(rqst)
        return w
    except urllib2.URLError as e:
        logging.error("Couldn't get the link. Url ERROR")
        logging.error(e)
        logging.error(headers)
        logging.error(repr(link))
        # not quite sure about raising it again.
        # by now, this will make the task to be retried.
        raise urllib2.URLError(e)  # REMOVE - added to raise better


def buildLink(link):
    # TEST
    """check that is a proper www.seriescoco.com link"""
    #logging.debug("building link: ")  # noisy
    #logging.debug(repr(link))  # noisy
    if "seriesyonkis" in link or "seriescoco" in link:
        return link
    else:
        # adding more resiliency to bad constructed URL
        if link[0:7] == "http://":
            logging.error("Malformed SY link")
            # Its malformed, because we expect it to be a SY link,
            # not another website URL, so if it has this at the
            # beginning, means its a broken one
            logging.error(link)
            link = "http://www.seriescoco.com/" + link[7:]
            logging.error(link)
            return link
        else:
            return "http://www.seriescoco.com" + link


def plainString(s):
    # TOTEST
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
    madafaca = madafaca.replace("\n", "")
    return madafaca


def amIARobot(web):
    # TEST
    """checks that the web content is not a captcha website."""
    # TODO: this should be a little bit smartter
    # for example, it should check if the text is in some place
    # if not, this will give false positives
    return "comprobar que eres humano" in web


def linksToEpisodesSY(msg):
    """extract the links to episodes in a seriesyonkis email"""
    # TESTED
    if msg is None:
        raise TypeError

    # TODO testing how to encode an email right
    #logging.info(repr(str_msg))

    #syMsg = f.parsestr(str)
    #syMsg = f.parsestr(str_msg)
    #syMsg = msg
    # TODO: aclarar si esto es asi, o no. mientras tanto, esta funcion
    # falla con errores de encoding, asi que no me vale.
    # con nosetes funciona, con normal falla  -> con encode
    # syMsg = quopri.decodestring(msg.encode("UTF-8"))
    # con nosetest falla, con normal funcion -> sin encode
    syMsg = quopri.decodestring(msg)
    soup = bs4.BeautifulSoup(syMsg)

    episodes = set()

    for link in soup.find_all("a"):
        cleanLink = link.get('href', '')
        if "capitulo" in cleanLink:
            episodes.add(cleanLink.decode())

    lst = list(episodes)
    lst.sort()

    return lst

extractors = {
    "seriesyonkis": linksToEpisodesSY,
    "seriescoco": linksToEpisodesSY
}


def linksToEpisodes(msg, extractors=extractors):
    # TESTED
    """extract the episode links from the mail"""
    applicable_extractors = [extractor for (s, extractor) in extractors.iteritems() if s in msg]

    if len(applicable_extractors) == 0:
        raise NoExtractorFoundError

    episodes = []
    for extractor in applicable_extractors:
        episodes.extend(extractor(msg))

    if len(episodes) == 0:
        raise NoEpisodesFoundError

    episodes = list(set(episodes))
    episodes.sort()

    return episodes


def interLinks(web):
    #TODO: refactor this to return a good link # 2013 03 29
    # TESTED
    """get the html of an episode page.
    It returns a list with the links to the intermediate pages.
    The origin must be a seriesyonkis o seriescoco page."""
    logging.debug("--- Extracting the interLinks---")

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
        raise LinkExtractionError

    return list(set(linkList)) if (len(linkList) > 0) else None


def episodeDataFromEpisodeWeb(web):
    """TODO: this should be a general function and select the proper
    extractor"""
    return episodeDataFromEpisodeWebSY(web)

def episodeDataFromEpisodeWebSY(web):
    # TEST
    """receives a seriescoco webcontent
    returns a dictionary with the details of the episode"""

    logging.debug("extracting data from episode web")
    # In a prior model we used vars instead of dict
    # But the keys are the same
    #fullTitle = u''
    #description = u''
    #originalTitle = u''
    #episodeNumber = u''
    #season = u''
    #tvshow = u''
    details = {}
    details['fullTitle'] = ""
    details['season'] = None
    details['tvshow'] = ""
    details['episodeNumber'] = None
    details['tvshow'] = None

    soup = bs4.BeautifulSoup(web)
        # I tried it this way, but it was a mistake.
        # it brokes sometimes. I think
        # due to the extra chars en the email or something
        # soup = bs4.BeautifulSoup(web.decode("utf-8"))
    # - with this loop, we get the info from the episode
    for block in soup.find_all("div"):
        try:
            if "section-intro ficha_activa" in block['class'] or "section-intro" in block['class']:
                # get the title
                logging.debug(block)
                logging.debug(type(block.h1))
                details['fullTitle'] = plainString(block.h2.contents).strip()
                # get the description
                descriptionTag = block.div.contents
                details['description'] = plainString(descriptionTag).strip()
                logging.debug("Description Tag")
                logging.debug(repr(descriptionTag))
                logging.debug("--- full repr of description ---")
                logging.debug(repr(block.div.contents))
                # Collect the details
                try:
                    #doing this in a separate function, will do perfectly
                    logging.debug("Extracting details of the episode")
                    for elem in descriptionTag:
                        plain = elem.decode()
                        if u'tulo original' in plain:
                            elem.strong.extract()
                            details['originalTitle'] = elem.getText().strip()
                        elif u'Capítulo' in plain:
                            elem.strong.extract()  # remove unwanted tag
                            details['episodeNumber'] = elem.decode_contents().strip()
                            details['episodeNumber'] = int(details['episodeNumber'])
                        elif u'Temporada' in plain:
                            elem.strong.extract()  # remove unwanted tag
                            details['season'] = int(elem.decode_contents().strip())
                        else:
                            try:
                                logging.debug(type(elem))
                                if isinstance(elem, bs4.element.Tag):
                                    logging.debug("this is the TV show")
                                    logging.debug(elem.getText())
                                    details['tvshow'] = elem.getText()
                            except:
                                # this exception must be silenced
                                pass
                except:
                    logging.error("Couldn't get details of the episode")
                    raise
            else:
                logging.error("shit happends!")
                logging.error(block)

        except KeyError:
            # if we enable loggin for this, would be a storm of log.
            # there should be exceptions in this and its normal.
            # we don't need to catch them.
            pass

    logging.debug("fullTitle")
    logging.debug(details['fullTitle'])
    logging.debug("description")
    logging.debug(details['description'])
    logging.debug("tvshow")
    logging.debug(details['tvshow'])
    logging.debug("Original Title")
    logging.debug(details['originalTitle'])
    logging.debug("Seasson")
    logging.debug(details['season'])
    logging.debug("Episode Number")
    logging.debug(details['episodeNumber'])
    return details


def linkToVideoSY(web):
    # This will be part of linkToVideoSYFromInterLink
    # TODO2: ES_ ademas, esto deberia saltar excepciones, no devolver cadenas
    # vacias...
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
                if videoLink == "":
                    #- if no link found, raise exception
                    logging.debug("No link Found")
                    logging.debug(repr(link))
                    raise LinkExtractionError
                return videoLink.decode()
        except KeyError as e:
            # logging.debug "err"
            logging.error("Error extracting the link to videoSY")
            logging.error(e)
        except LinkExtractionError:
            logging.error("No link Found.")


def providerFromInterWebSY(web):
    # TOTEST
    """Takes an intermediate web (in seriesyonkis websites, you
    have to visit an intermediate website with a link to the video).
    returns the video provider.
    """
    # TODO: should this be merged into linkToVideoSY? would avoid 1 parsing.
    # raise a custom exception instead of saying nothing

    # QUESTION
    sopa = bs4.BeautifulSoup(web)
    logging.debug("providerFromInterWeb type")
    logging.debug(type(web))

    for link in sopa.find_all("tr"):
        try:
            videoProv = False
            if "action_link" in link['class']:
                # videoLink = link.a['href']
                videoProv = link['data-server']
                return videoProv.decode()
        except KeyError as e:
            # logging.debug "err"
            logging.error("Error extracting the provider of videoSY")
            logging.error(e)
        except TypeError as e:
            logging.error("Error extracting the provider of VideoSY")
            logging.error(e)
        finally:
            if videoProv:
                pass
            else:
                # TODO: don't really know what im doing here. just trying to
                # not fall appart in a different way.
                # we could choose between None or ""
                return ""



def linkToVideoInProvFromShortedLink(link):
    # TOTEST
    """Takes a link in the shortener and
        returns the link to the video in the hoster or provider"""
    FinalLink = ""
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
            logging.error("""Oops, you seem like a robot to them...
                             We couldn't download this:""")
            logging.error(resultLink)
            suspect = openWebsite(resultLink)
            if amIARobot(suspect):
                logging.error(originLink)
                raise Exception("CaptCha Alert, you seem like a robot")
            else:
                logging.error("Eror getting video in provider. Check:")
                logging.error(resultLink)
        else:
            FinalLink = resultLink
    except urllib2.HTTPError as err:
        if err.code == '404':
            logging.error("""This guys are smart.
                          They send a 404 but its a fake""")
            logging.error(w.geturl())
            FinalLink = resultLink
        else:
            logging.error("""Could not get link to video
                          in provider. HTTPError""")
            logging.error(repr(w))
            logging.error(repr(w.geturl()))
    except Exception as err:
        logging.error("Could not get a link to video in provider. OTHER Error")
        logging.error(repr(err))
    finally:
        return FinalLink


def linkToVideoInProvFromEpisodeLink(link):
    # TOTEST
    """Takes a link to an episode in SY,
        returns a list with links to videos"""
        # TODO: This is a meta-like function. write it?
    pass


def linkToVideoAndProvFromInterLink(interLink):
    # TOTEST
    """Takes a interlink and
        if no link found, returns empty string.Else
        returns the list of videos in the provider"""
    logging.debug("getting the link to video and the provider of it")
    logging.debug(type(interLink))
    try:
        #- extract the link to video, and test it
        SYLink = linkToVideoSY(interLink)
        provLink = linkToVideoInProvFromShortedLink(SYLink)
        logging.debug("Link in provider")
        logging.debug(provLink)
        provName = providerFromInterWebSY(interLink)
        logging.debug("Provider Name: ")
        logging.debug(provName)
        return (provLink, provName)
    except:
        logging.debug("Problem trying to get linkToVideoInProvFromInterLink")
        raise


#######################################
#              Exceptions             #
#######################################
class DataExtractionError(Exception):
    """Another General Exception for this module"""
    pass


class LinkExtractionError(Exception):
    """General exception for this module"""
    pass


class NoExtractorFoundError(LinkExtractionError):
    pass


class NoEpisodesFoundError(LinkExtractionError):
    pass

