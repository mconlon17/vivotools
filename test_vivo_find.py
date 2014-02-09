"""
    test_vivo_find.py -- find entities in VIVO by title and label

    Version 0.1 MC 2013-12-28
    --  Initial version.

    Note:
    vivo_find is deprecated
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"

print vt.vivo_find()
print vt.vivo_find("vivo:FacultyMember","Conlon, Mike")
print vt.vivo_find("foaf:Organization","Bucknell University")

print datetime.now(),"Finish"
