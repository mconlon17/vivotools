"""
    test_make_dt_interval_rdf.py -- given date uri
    make interval rdf

    Version 0.1 MC 2013-12-27
    --  Initial version.
    Version 0.2 MC 2014-01-11
    --  Test all cases involving None
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.2"

import vivotools as vt
from datetime import datetime

a = "http://start"
b = "http://end"

print datetime.now(), "Start"

print "\n", vt.make_dt_interval_rdf(a, b)
print "\n", vt.make_dt_interval_rdf(a, None)
print "\n", vt.make_dt_interval_rdf(None, b)
print "\n", vt.make_dt_interval_rdf(None, None)

print datetime.now(), "Finish"
