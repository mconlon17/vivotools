"""
    test_make_concept_dictionary.py -- query VIVO and return a dictionary
    containing the skos:Concept entities.  Key is concept label, value is URI

    Version 0.1 MC 2013-12-121
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
print datetime.now(),"Making concept dictionary"
vt.make_concept_dictionary(debug=True)
print datetime.now(),"Concept dictionary has ",len(vt.concept_dictionary),"entries"
k = 0
print "First 20 entries:"
for label in sorted(vt.concept_dictionary.keys()):
    uri = vt.concept_dictionary[label]
    k = k + 1
    print "    ",label,uri
    if k > 20:
        break

print datetime.now(),"Making concept dictionary"
vt.make_concept_dictionary()
print datetime.now(),"Concept dictionary has ",len(vt.concept_dictionary),"entries"
print datetime.now(),"Finish"
