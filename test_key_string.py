"""
    test_key_string.py -- from text, make a key string for use in dictionaries
    where text may not match exactly, such as publication and grant titles

    Version 0.1 MC 2013-12-27
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime
#
#  Test cases
#

print datetime.now(),"Start"
print vt.key_string("  A +Walk+ in (the) Woods")
print vt.key_string("A wALK  in the, woods   ")
print vt.key_string("AWALKINTHEWOODS")
print vt.key_string("awalkinthewoods")
print datetime.now(),"Finish"
