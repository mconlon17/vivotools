"""
    test_get_vivo_value.py -- Given a subject URi and a predicate,
    get the value of the object.  Assumes the object is single valued.

    Version 0.1 MC 2013-12-30
    --  Initial version.

"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"

print vt.get_vivo_value("http://vivo.ufl.edu/individual/n25562","foaf:lastName")
print vt.get_vivo_value("http://vivo.ufl.edu/individual/n1278130",
                        "rdfs:label")
print vt.get_vivo_value("http://vivo.ufl.edu/individual/n25562","foaf:noName")
print vt.get_vivo_value("http://vivoweb.org/ontology/degree/academicDegree4",
                        "core:abbreviation")

print datetime.now(),"Finish"
