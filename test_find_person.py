"""
    test_find_person.py -- from a ufid dictionary, find the ufid and return
    the URI of the person.

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
ufids = [
    "02001000",
    "57000000",
    "80147616",
    "33100000",
    "16010000",
    "16020000",
    "60100000",
    "84808900",
    "27000000",
    "11040000"
    ]
for ufid in ufids:
    [found,uri] = vt.find_person(ufid,ufid_dictionary)
    print str(found).ljust(5),ufid,uri

print datetime.now(),"Finished"
