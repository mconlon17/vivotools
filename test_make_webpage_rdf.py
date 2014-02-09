"""
    test_make_webpage_rdf.py -- given a uri and optional attributes,
    make RDF for a webpage entity

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
print vt.make_webpage_rdf("http://google.com/article_name")
print vt.make_webpage_rdf(None)
print vt.make_webpage_rdf("http://google.com/article_name",rank="2")
print vt.make_webpage_rdf("http://google.com/article_name",\
    harvested_by="Test Harvest",\
    link_anchor_text="Home Page",\
    rank="8",\
    uri_type="http://vivo.ufl.edu/ontology/vivo-ufl/SomeType")
print vt.make_webpage_rdf("http://google.com/article_name")
print datetime.now(),"Finish"

