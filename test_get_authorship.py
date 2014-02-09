"""
    test_get_authorship.py -- Given a URI of an authorship, return a python
    structure representing the attributes of the authorship

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
authorships = [
    "http://vivo.ufl.edu/individual/n4368384731",
    "http://vivo.ufl.edu/individual/n1866513500",
    "http://vivo.ufl.edu/individual/n7379013390",
    "http://vivo.ufl.edu/individual/n6643177200",
    "http://vivo.ufl.edu/individual/n5359424335",
    "http://vivo.ufl.edu/individual/n2248061668",
    "http://vivo.ufl.edu/individual/n943734503",
    "http://vivo.ufl.edu/individual/n9870226211",
    "http://vivo.ufl.edu/individual/n3005974623",
    "http://vivo.ufl.edu/individual/n8064100744",
    ]
for authorship in authorships:
    print "\n",vt.get_authorship(authorship)
print datetime.now(),"Finish"
