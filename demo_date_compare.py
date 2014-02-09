"""
    demo_date_compare.py -- Show comparisons of dates in python

    Version 0.1 MC 2013-12-28
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import dateutil.parser

date1_text = "1968-01-01T00:00:00Z"
date1 = dateutil.parser.parse(date1_text)
#date1 = date1.replace(tzinfo=dateutil.tz.tzlocal())

print "Date 1 Text  ",date1_text
print "Date 1 Format",date1.isoformat()

date2_text = "2013-01-31T05:00:00Z"
date2 = dateutil.parser.parse(date2_text)

print "Date 2 Text  ",date2_text
print "Date 2 Format",date2.isoformat()

print "Text 1 == 2?",date1_text==date2_text
print "Date 1 == 2?",date1==date2

date3_text = "2013-01-31T00:00:00"
date3 = dateutil.parser.parse(date3_text)

print "Date 3 Text  ",date3_text
print "Date 3 Format",date3.isoformat()

print "Text 1 == 3?",date1_text==date3_text
print "Date 1 == 3?",date1==date3
