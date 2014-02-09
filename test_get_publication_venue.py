"""
    test_get_publication_venue.py -- Given a URI of a publication_venue, return a python
    structure representing the attributes of the publication_venue

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
publication_venues = [
    "http://vivo.ufl.edu/individual/n4766035388",
    "http://vivo.ufl.edu/individual/n3893423675",
    "http://vivo.ufl.edu/individual/n7233910538",
    "http://vivo.ufl.edu/individual/n1503430672",
    "http://vivo.ufl.edu/individual/n180017",
    "http://vivo.ufl.edu/individual/n8193104182",
    "http://vivo.ufl.edu/individual/n7501763467",
    "http://vivo.ufl.edu/individual/n7500516719",
    "http://vivo.ufl.edu/individual/n90678",
    "http://vivo.ufl.edu/individual/n43992"
    ]
for publication_venue in publication_venues:
    print "\n",vt.get_publication_venue(publication_venue)
print datetime.now(),"Finish"
