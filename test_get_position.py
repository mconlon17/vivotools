"""
    test_get_position.py -- Given a URI of a position, return a python
    structure representing the attributes of the position

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
positions = [
    "http://vivo.ufl.edu/individual/n962011",
    "http://vivo.ufl.edu/individual/n849745220",
    "http://vivo.ufl.edu/individual/n8262508057",
    "http://vivo.ufl.edu/individual/n950",
    "http://vivo.ufl.edu/individual/n2417078599",
    "http://vivo.ufl.edu/individual/n5207883537",
    "http://vivo.ufl.edu/individual/n17281",
    "http://vivo.ufl.edu/individual/n241190",
    "http://vivo.ufl.edu/individual/n600567949",
    "http://vivo.ufl.edu/individual/n2117590223"
    ]
for position in positions:
    print "\n",vt.get_position(position)
print datetime.now(),"Finish"
