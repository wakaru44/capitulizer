#!/usr/bin/python
# -*- coding: utf-8 -*-

#import tools
#import json


#############################################################
# import pickle
# import bs4
# import urllib2
# c = tools.cargar_fixt("episodeDataFromEpisodeWeb-GoodUnicode-input.html")

# soup = bs4.BeautifulSoup(c)
#
# print type(soup)
#
# ass = soup.find_all("div")[1]
# print type(ass)
# print "clase sopa: ", repr(ass.__class__)
# if isinstance(ass, bs4.element.Tag):
#     print "es una etiqueta"
#     print repr(ass.__str__())
#     print "---------------__"
#     print dir(ass)
# elif isinstance(ass, bs4.navigableString):
#     print "es una cadena"
#     print repr(ass.__str__())
# else:
#     print "es mierda en bote"
#############################################################

############################################################
## testing opening links
# import random
# import time
# import urllib2
# MAXIMUM_WAIT_TIME = 12
# MINIMUM_WAIT_TIME = 2
#
# def openLink(link):
#     """open a link and return the redirection. I do this in a separate
#     function, besides the overkill, to get the sleep time apart, and
#     maybe, join all the urllib request in the same function."""
#     humanizer = int(random.random() *
#                     (MAXIMUM_WAIT_TIME - MINIMUM_WAIT_TIME))
#     time.sleep(MINIMUM_WAIT_TIME + humanizer)
#     userAgents = ['Amiga-AWeb/3.4.167SE ',
#                    'Mozilla/5.0']
#     pickOneUserAgent = userAgents[int((random.random() * 10 )
#                                         % len(userAgents) )]
#     print("user agent")
#     print(pickOneUserAgent)
#     try:
#         #headers = { 'User-Agent' : pickOneUserAgent }
#         # safe - mode TODO
#         headers = { 'User-Agent' : 'Mozilla/5.0'}
#         rqst = urllib2.Request(link, None, headers)
#         w = urllib2.urlopen(rqst)
#         return w
#     except urllib2.URLError as e:
#         print("Could't get the link. Url ERROR")
#         print(e)
#         print(headers)
#         print(repr(link))
#         # not quite sure about raising it again.
#         # by now, this will make the task to be retried.
#         raise urllib2.URLError
#
# c = openLink("http://www.seriescoco.com/s/y/3573901/0/s/1205")
# d = openLink(u'http://www.seriescoco.com/s/y/2997570/0/s/3566')
#
# print c.geturl()
# print d.geturl()


# def addDetails(details):
#     print "normal"
#     print details
#     details = json.dumps(details)
#     print "jeison"
#     print details
#     return details
#
# def getDetails(details):
#     details = json.loads(details)
#     print "and again"
#     print details
#
# details = {'episodeNumber': 7,
#               'description': u'<h2> The Walking Dead</h2> <p>
#                            <strong>  T\xedtulo original: </strong>
#                            Cap\xedtulo 7</p> <p>  <strong>
#                            Temporada: </strong> 3</p> <p> <strong>
#                            Cap\xedtulo: </strong> 7</p>',
#               'season': 3,
#               'originalTitle': u'Cap\xedtulo 7',
#               'tvshow': u'The Walking Dead',
#               'fullTitle': u'Cap\xedtulo 7 <span> 3x7</span>'}
# detallucos = addDetails(details)
# getDetails(detallucos)

#############################################################
## testing web search for images
# import urllib2
# import json
#
# # The request also includes the userip parameter which provides the end
# # user's IP address. Doing so will help distinguish this legitimate
# server-side traffic from traffic which doesn't come from an end-user.
# url = ('https://ajax.googleapis.com/ajax/services/search/images'
#               '?v=1.0&q=Paris%20Hilton&userip=91.142.222.222')
#
# request = urllib2.Request(
#         url, None, {'Referer': 'capitulizer.appspot.com'})
# response = urllib2.urlopen(request)
#
# # Process the JSON string.
# results = json.load(response)
#
# print json.dumps(results,sort_keys=True,indent=4, separators=(',', ': ') )
#
# #print results
