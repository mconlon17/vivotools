"""
    test_make_deptid_dictionary.py -- query VIVO and return a dictionary
    containing the deptid entities.  Key is deptid, value is URI.  The same
    URI may have several deptids.

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
print datetime.now(),"Making deptid dictionary"
deptid_dictionary = vt.make_deptid_dictionary(debug=True)
print datetime.now(),"deptid dictionary has ",len(deptid_dictionary),"entries"
k = 0
print "First 20 entries:"
for deptid in sorted(deptid_dictionary.keys()):
    uri = deptid_dictionary[deptid]
    k = k + 1
    print "    ",deptid,uri
    if k > 20:
        break

print datetime.now(),"Finished"
