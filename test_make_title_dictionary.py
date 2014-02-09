"""
    test_make_title_dictionary.py -- query VIVO and return a dictionary
    containing the titles for all documents.  The key is prepared title (see
    key_string), value is URI.
    
    Version 0.1 MC 2013-12-28
    --  Initial version.  Make a dictionary and make a dictionary with
        debug=True
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"
print datetime.now(),"Making title dictionary"
title_dictionary = vt.make_title_dictionary(debug=True)
print datetime.now(),"title dictionary has ",len(title_dictionary),"entries"
k = 0
print "First 20 entries:"
for title in sorted(title_dictionary.keys()):
    uri = title_dictionary[title]
    k = k + 1
    print "    ",title,uri
    if k > 20:
        break

print datetime.now(),"Finished"
