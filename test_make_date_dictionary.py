"""
    test_make_date_dictionary.py -- query VIVO and return a dictionary
    containing the date entities.  Key is date, value is URI.
    
    Version 0.1 MC 2014-05-19
    --  Initial version.  Make a dictionary and make a dictionary with
        debug=True
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

from vivotools import make_date_dictionary
from datetime import datetime

print datetime.now(),"Start"
print datetime.now(),"Making date dictionary"
date_dictionary = make_date_dictionary(debug=True)
print datetime.now(),"date dictionary has ",len(date_dictionary),"entries"
k = 0
print "First 20 entries:"
for date in sorted(date_dictionary.keys()):
    uri = date_dictionary[ufid]
    k = k + 1
    print "    ",date.isoformat(),uri
    if k > 20:
        break

print datetime.now(),"Finished"
