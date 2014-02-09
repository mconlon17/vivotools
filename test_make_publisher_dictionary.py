"""
    test_make_publisher_dictionary.py -- query VIVO and return a dictionary
    containing the publisher entities.  Key is publisher label as key_string,
    value is URI.

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
print datetime.now(),"Making publisher dictionary"
publisher_dictionary = vt.make_publisher_dictionary(debug=True)
print datetime.now(),"publisher dictionary has ",len(publisher_dictionary),"entries"
k = 0
print "First 20 entries:"
for publisher in sorted(publisher_dictionary.keys()):
    uri = publisher_dictionary[publisher]
    k = k + 1
    print "    ",publisher,uri
    if k > 20:
        break

print datetime.now(),"Finished"
