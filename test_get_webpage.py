"""
    test_get_webpage.py -- Given a URI of a webpage, return a python
    structure representing the attributes of the webpage

    Version 0.1 MC 2013-12-27
    --  Initial version.

"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"
webpages = [
    "http://vivo.ufl.edu/individual/n3549388983",
    "http://vivo.ufl.edu/individual/n5167070257",
    "http://vivo.ufl.edu/individual/n7734440333",
    "http://vivo.ufl.edu/individual/n4996654872",
    "http://vivo.ufl.edu/individual/n2167668630",
    "http://vivo.ufl.edu/individual/n4627222448",
    "http://vivo.ufl.edu/individual/n328795",
    "http://vivo.ufl.edu/individual/n2274340",
    "http://vivo.ufl.edu/individual/n7404140895",
    "http://vivo.ufl.edu/individual/n8657219888"
    ]
for webpage in webpages:
    print "\n",vt.get_webpage(webpage)
print datetime.now(),"Finish"
