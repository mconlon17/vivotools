"""
    test_get_organization.py -- Given a URI of an organization entity in VIVO,
    return a python sturcture containing attrbutes of the organization

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
print "\n",vt.get_organization("http://vivo.ufl.edu/individual/n1278130")
print "\n",vt.get_organization("http://vivo.ufl.edu/individual/n8763427")
print "\n",vt.get_organization("http://vivo.ufl.edu/individual/n4820")
print "\n",vt.get_organization("http://vivo.ufl.edu/individual/n534413")
print datetime.now(),"Finish"
