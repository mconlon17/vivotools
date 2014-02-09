"""
    test_get_datetime_interval.py -- Given a URI of a datetime interval, return
    a python structure with the attributes of the date time interval

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
datetime_intervals = [
    "http://vivo.ufl.edu/individual/n6241194045",
    "http://vivo.ufl.edu/individual/n251060",
    "http://vivo.ufl.edu/individual/n1902493026",
    "http://vivo.ufl.edu/individual/n5194397097",
    "http://vivo.ufl.edu/individual/n1787130662",
    "http://vivo.ufl.edu/individual/n6340364",
    "http://vivo.ufl.edu/individual/n77803",
    "http://vivo.ufl.edu/individual/n5104716880",
    "http://vivo.ufl.edu/individual/n694420232",
    "http://vivo.ufl.edu/individual/n658362325"
    ]
for datetime_interval in datetime_intervals:
    print "\n",vt.get_datetime_interval(datetime_interval)
print datetime.now(),"Finish"
