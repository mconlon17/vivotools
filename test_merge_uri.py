"""
    test_merge_uri.py -- given from and to URIs, generate add and sub RDF for
    merging the from URI to the to URI

    Version 0.1 MC 2014-06-21
    --  Initial version.
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

from vivotools import merge_uri
from vivotools import rdf_header
from vivotools import rdf_footer
from datetime import datetime

print datetime.now(),"Start"

furi = "http://vivo.ufl.edu/individual/n4449932692"
touri = "http://vivo.ufl.edu/individual/n39051"
[add,sub] = merge_uri(furi, touri)

print "Add RDF:"
print rdf_header()
print add
print rdf_footer()
print "Sub RDF:"
print rdf_header()
print sub
print rdf_footer()

print datetime.now(),"Finish"
