#!/usr/bin/python
# -*- coding: utf-8 -*-


## helper function. NOT A TEST
def loadFixt(filename):
    """Loads a fixture from a file, usually an HTML document and returns its
    content."""
    path = "./tests/fixtures/" + filename
    fh = open(path, "r")
    c = fh.read()

    return c.decode('utf-8')

### y aqui empezamos a probar


class test_LoadFixt:

    def test_loadFixt_basico(self):
        expect = u'Loremp ipsum\ndolor Sit\n'
        result = loadFixt("faux-fixture.txt")
        print "expect", expect
        print "result", result
        assert result == expect
