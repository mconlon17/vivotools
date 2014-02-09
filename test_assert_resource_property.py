"""
    test_assert_resource_property.py -- Given a URI, a vivo resource property
    predicate and a resource URI, generate RDF for asserting that the URI has
    the resource property URI.  The tests demonsrate that that the function does
    not check for a valid predicate, nor a valid resource URI.

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

print vt.assert_resource_property("http://a.b","http://c.d","http://e.f")
print vt.assert_resource_property("http://a.b","vivo:authorInAuthorship",
                                  "http://c.d")
print vt.assert_resource_property("http://a.b","vivo:authorinauthorlist",
                                  "42")

print datetime.now(),"Finish"

