"""
    test_find_journal.py -- from a journal dictionary, find journals via their
    ISSN and return their URIs.

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
journals = [
    "0742-4477",
    "1916-2790",
    "1089-5639",
    "1522-8037",
    "0045-7930",
    "9999-9999",
    "2044-4753",
    "1759-6653",
    "0306-7734",
    "1072-0847",
    "1234-1010"
    ]
for journal in journals:
    [found,uri] = vt.find_journal(journal,journal_dictionary)
    print str(found).ljust(5),journal,uri

print datetime.now(),"Finished"
