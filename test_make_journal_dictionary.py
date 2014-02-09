"""
    test_make_journal_dictionary.py -- query VIVO and return a dictionary
    containing the journal entities.  Key is ISSN, value is URI.
    
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
print datetime.now(),"Making journal dictionary"
journal_dictionary = vt.make_journal_dictionary(debug=True)
print datetime.now(),"journal dictionary has ",len(journal_dictionary),"entries"
k = 0
print "First 20 entries:"
for journal in sorted(journal_dictionary.keys()):
    uri = journal_dictionary[journal]
    k = k + 1
    print "    ",journal,uri
    if k > 20:
        break

print datetime.now(),"Finished"
