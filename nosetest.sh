#!/bin/bash
export PYTHONPATH=$PATH:/usr/local/google_appengine/capitulizer:/home/wakaru/google_appengine/lib:/home/wakaru/workspace/google_appengine/capitulizer/bs4/builder
#PYTHONPATH = `python ./get_mod_py_path.py`
python ./get_mod_py_path.py
nosetests --with-nosegunit --gae-lib-path="/home/wakaru/workspace/google_appengine" $@
# deprecated:  --gae-application="../capitulizer"
# deprecated: --gae-lib-root="/home/wakaru/google_appengine"
