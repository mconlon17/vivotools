"""
    test_assert_data_property.py -- Given a URI, a vivo data property predicate
    and a value, generate RDF for asserting thar the URI has the data property
    value.  The tests demonsrate that that the function does not check for
    a valid predicate, nor a valid value.

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

print vt.assert_data_property("http://a.b","http://c.d","5")
print vt.assert_data_property("http://a.b","vivo:phoneNumber","5")
print vt.assert_data_property("http://a.b","bibo:abstract","We escape nasty ampersands & other characters that <trip up> RDF")

print datetime.now(),"Finish"

