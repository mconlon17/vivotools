"""
    test_make_harvest_datetime.py -- show the current datetime

    Version 0.1 MC 2013-12-28
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"

print vt.make_harvest_datetime()

print datetime.now(),"Finish"
