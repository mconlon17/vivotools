"""
    test_get_datetime_value.py -- Given a URI of a datetime value, return
    a python structure withthe attributes of the date time

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
datetime_values = [
    "http://vivo.ufl.edu/individual/n3704515248",
    "http://vivo.ufl.edu/individual/n1010507230",
    "http://vivo.ufl.edu/individual/n4877327108",
    "http://vivo.ufl.edu/individual/n2721877",
    "http://vivo.ufl.edu/individual/n7118224",
    "http://vivo.ufl.edu/individual/n1711565",
    "http://vivo.ufl.edu/individual/n9339603516",
    "http://vivo.ufl.edu/individual/n5690009465",
    "http://vivo.ufl.edu/individual/n1909241",
    "http://vivo.ufl.edu/individual/n2897909"
    ]
for datetime_value in datetime_values:
    print "\n",vt.get_datetime_value(datetime_value)
print datetime.now(),"Finish"
