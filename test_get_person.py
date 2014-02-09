"""
    test_get_person.py -- Given a URIof a person entity in VIVO, return a
    python sturcture containing attrbutes of the person

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
print "\n",vt.get_person("http://vivo.ufl.edu/individual/n13049",get_grants=True,
                    get_publications=True,get_positions=True) # Richard Macmaster
print "\n",vt.get_person("http://vivo.ufl.edu/individual/n3698",
                    get_positions=True) # Chelsea Dinsmore
print "\n",vt.get_person("http://vivo.ufl.edu/individual/n25562",
                    get_degrees=True) # Mike Conlon
print "\n",vt.get_person("http://vivo.ufl.edu/individual/n1770144435",
                    get_positions=True) # Colleen Abad
print datetime.now(),"Finish"
