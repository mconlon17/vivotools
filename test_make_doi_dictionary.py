"""
    test_make_doi_dictionary.py -- query VIVO and return a dictionary
    containing the doi for all documents.  Key is doi, value is URI.
    
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
print datetime.now(),"Making doi dictionary"
doi_dictionary = vt.make_doi_dictionary(debug=True)
print datetime.now(),"doi dictionary has ",len(doi_dictionary),"entries"
k = 0
print "First 20 entries:"
for doi in sorted(doi_dictionary.keys()):
    uri = doi_dictionary[doi]
    k = k + 1
    print "    ",doi,uri
    if k > 20:
        break

print datetime.now(),"Finished"
