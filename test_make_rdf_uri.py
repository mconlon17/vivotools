"""
    test_make_rdf_uri.py -- from a VIVO uri, make the corresponding uri for
    the RDF

    Version 0.1 MC 2013-12-27
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"


import vivotools as vt
from datetime import datetime
#
#  Test cases
#

print datetime.now(),"Start"
print vt.make_rdf_uri("http://vivo.ufl.edu/individual/n1232")
print datetime.now(),"Finish"
