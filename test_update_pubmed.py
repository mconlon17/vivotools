"""
    test_update_pubmed.py -- given a puburi, get PubMed attributes and generate
    add and sub ardf for updating the pubmed content of the publication in VIVO

    Version 0.1 MC 2013-12-21
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"
vt.make_concept_dictionary()
print "Concept dictionary has ",len(vt.concept_dictionary),"entities"
print vt.update_pubmed("http://vivo.ufl.edu/individual/n2820964262") # already has concept
print vt.update_pubmed(None)
print vt.update_pubmed("http://vivo.ufl.edu/individual/n950864862") # normal
print vt.update_pubmed("http://vivo.ufl.edu/individual/n6919808728") # No Pubmed
print vt.update_pubmed("http://vivo.ufl.edu/individual/n3354210934") # no DOI
print datetime.now(),"Finish"

