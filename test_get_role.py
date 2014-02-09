"""
    test_get_role.py -- Given a URI of a role, return a python structure
    representing the attributes of the role

    Version 0.1 MC 2013-12-27
    --  Initial version.
    Version 0.2 MC 2014-01-04
    --  Use JSON dumps

    To Do
    --  Generalize get_role.  It works only for some grant roles
    
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.2"

import vivotools as vt
from datetime import datetime
import json

print datetime.now(),"Start"
roles = [
    "http://vivo.ufl.edu/individual/n1665912700",
    "http://vivo.ufl.edu/individual/n206828627",
    "http://vivo.ufl.edu/individual/n1901240698",
    "http://vivo.ufl.edu/individual/n9688",
    "http://vivo.ufl.edu/individual/n1796432519",
    "http://vivo.ufl.edu/individual/n468916789",
    "http://vivo.ufl.edu/individual/n1216606496",
    "http://vivo.ufl.edu/individual/n1613740695",
    "http://vivo.ufl.edu/individual/n1071648987",
    "http://vivo.ufl.edu/individual/n270897"]
for role in roles:
    print "\n",json.dumps(vt.get_role(role),indent=4,sort_keys=True)
print datetime.now(),"Finish"
