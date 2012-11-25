#!/usr/bin/python
# -*- coding: utf-8 -*-

import tools


############################################################# 
# import pickle
# import bs4
# import urllib2
# c = tools.cargar_fixt("episodeDataFromEpisodeWeb-GoodUnicode-input.html")
# 
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

import random
import time
import urllib2
MAXIMUM_WAIT_TIME = 12
MINIMUM_WAIT_TIME = 2

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
    print("user agent")
    print(pickOneUserAgent)
    try:
        #headers = { 'User-Agent' : pickOneUserAgent }
        # safe - mode TODO
        headers = { 'User-Agent' : 'Mozilla/5.0'}
        rqst = urllib2.Request(link, None, headers)
        w = urllib2.urlopen(rqst)
        return w
    except urllib2.URLError as e:
        print("Could't get the link. Url ERROR")
        print(e)
        print(headers)
        print(repr(link))
        # not quite sure about raising it again.
        # by now, this will make the task to be retried.
        raise urllib2.URLError

c = openLink("http://www.seriescoco.com/s/y/3573901/0/s/1205")
d = openLink(u'http://www.seriescoco.com/s/y/2997570/0/s/3566')

print c.geturl()
print d.geturl()
