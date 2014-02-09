"""
    test_update_resource_property.py -- Given a VIVO URI, a predicate, and two
    URIs -- VIVO resource URI and the source URI, generate the add and subtract
    RDF necessary to execute "five case logic" in updating VIVO with an
    authoritative source URI.

    Note.  In common use, the source data is presented with a "key" value, not
    a URI.  The key value must be translated using a dictionary to a URI.  For
    example, a person might be referred to in source data via a UFID.  The
    UFID is translated to a URI using a UFID dictionary.

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
cases = {
    "1.  VIVO has A, Source Has B": ["A","B"],
    "2.  VIVO has A and Source also has A": ["A","A"],
    "3.  VIVO has A, source has no value": ["A",None],
    "4.  VIVO has no value, Source has B": [None,"B"],
    "5.  VIVO has no value and Source also has no value": [None,None]
    }

for case in sorted(cases.keys()):
    print "\n",case,":"
    [vivo,source] = cases[case]
    [add,sub] = vt.update_resource_property("http://vivo.uri","http://pred.uri",
                                        vivo,source)
    print "    Add:"
    print add
    print "    Subtract:"
    print sub
print datetime.now(),"Finish"

