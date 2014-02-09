"""
    test_make_concept_rdf.py -- given a concept label, make RDF

    Version 0.1 MC 2013-12-121
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"
print vt.make_concept_rdf("Vanilla")
print vt.make_concept_rdf(None)
print vt.make_concept_rdf("Vanilla and Chocolate and Strawberry")
print datetime.now(),"Finish"

