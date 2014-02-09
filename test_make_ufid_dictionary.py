"""
    test_make_ufid_dictionary.py -- query VIVO and return a dictionary
    containing the ufid entities.  Key is ufid, value is URI.
    
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
print datetime.now(),"Making ufid dictionary"
ufid_dictionary = vt.make_ufid_dictionary(debug=True)
print datetime.now(),"ufid dictionary has ",len(ufid_dictionary),"entries"
k = 0
print "First 20 entries:"
for ufid in sorted(ufid_dictionary.keys()):
    uri = ufid_dictionary[ufid]
    k = k + 1
    print "    ",ufid,uri
    if k > 20:
        break

print datetime.now(),"Finished"
