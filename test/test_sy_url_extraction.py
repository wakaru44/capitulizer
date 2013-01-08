from nose.tools import raises, assert_equal

import extract as x

def message(filename):
    """Loads a fixture from a file, usually an HTML document and returns its
    content."""
    with open("./test/fixtures/" + filename, "r") as fn:
        return fn.read().decode('utf-8')

@raises(TypeError)
def test_fails_when_message_is_None():
    x.linksToEpisodesSY(None)

def test_returns_no_episodes_when_unsupported_message():
    assert_equal([], x.linksToEpisodesSY(""))

def test_return_list_when_good_message():
    msg = message("extractEpisodes-goodMulti.html")
    expect = [
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-14/217220',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-15/217214',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-16/217213',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-17/217212',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-18/217215',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-19/217216',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-20/217219',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-21/217218',
        u'http://www.seriesyonkis.com/capitulo/true-blood/capitulo-22/217217'
        ]

    assert_equal(x.linksToEpisodesSY(msg), expect)
