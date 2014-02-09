"""
    test_make_datetime_rdf.py -- given dates in isoformat
    make datetime rdf, supporting various precisions

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

value = datetime.now().isoformat()

cases = {
    "1.  Year precision": [value,"year"],
    "2.  Year month": [value,"yearMonth"],
    "3.  Year month day": [value,"yearMonthDay"],
    "4.  date value is unspecified": [None,"year"],
    "5.  Precision is unspecified": [value,None],

    }

for case in sorted(cases.keys()):
    print "\n",case,":"
    [a,b] = cases[case]
    [rdf,uri] = vt.make_datetime_rdf(a,b)
    print "    RDF:"
    print rdf
    print "    URI:"
    print "   ",uri


print datetime.now(),"Finish"
