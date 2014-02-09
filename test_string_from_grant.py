"""
    test_string_from_grant.py -- Given a URI of a grant, return a string
    describing the grant

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
grants = [
    "http://vivo.ufl.edu/individual/n1769500492",
    "http://vivo.ufl.edu/individual/n678985748",
    "http://vivo.ufl.edu/individual/n1725957599",
    "http://vivo.ufl.edu/individual/n859986285",
    "http://vivo.ufl.edu/individual/n899821550",
    "http://vivo.ufl.edu/individual/n2026295266",
    "http://vivo.ufl.edu/individual/n719692692",
    "http://vivo.ufl.edu/individual/n482305201",
    "http://vivo.ufl.edu/individual/n276081150",
    "http://vivo.ufl.edu/individual/n1863481639"
    ]
for grant in grants:
    print "\n",vt.string_from_grant(vt.get_grant(grant))
print datetime.now(),"Finish"
