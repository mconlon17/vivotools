"""
    test_get_vivo_uri.py -- return a valid, unused, vivo URI

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

for i in range(0,9):
    print vt.get_vivo_uri()

print datetime.now(),"Finished"
