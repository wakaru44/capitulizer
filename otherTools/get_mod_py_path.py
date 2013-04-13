#!/usr/bin/python
import os
import sys

# Remove the global Python modules from the PYTHONPATH.
path=""
try:
    path = os.environ['PYTHONPATH'].split(os.pathsep)
    if os.environ['GLOB_PY_MODULES'] in path: 
        path.remove(os.environ['GLOB_PY_MODULES'])
        print "hi"
except:
    pass

    # Construct the new path and print it. 
path = ':'.join(path)
print path
