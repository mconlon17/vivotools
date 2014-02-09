"""
    test_make_datetime_interval_rdf.py -- given dates in isoformat
    make interval rdf

    Version 0.1 MC 2013-12-27
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"

start = datetime.now().isoformat()
end = datetime.now().isoformat()

cases = {
    "1.  Start and end are both specified": [start,end],
    "2.  Start is specified, no end date": [start,None],
    "3.  No start date, end is specified": [None,end],
    "4.  start and end are both not specified": [None,None],
    }

for case in sorted(cases.keys()):
    print "\n",case,":"
    [a,b] = cases[case]
    [rdf,uri] = vt.make_datetime_interval_rdf(a,b)
    print "    RDF:"
    print rdf
    print "    URI:"
    print "   ",uri


print datetime.now(),"Finish"
