"""
    test_vivo_find_result.py -- find entities in VIVO by title and label

    Version 0.1 MC 2013-12-27
    --  Initial version.

    Note:
    vivo_find_result is deprecated
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"

print vt.vivo_find_result()
print vt.vivo_find_result("vivo:FacultyMember","Conlon, Mike")
print vt.vivo_find_result("foaf:Organization","Bucknell University")

print datetime.now(),"Finish"
