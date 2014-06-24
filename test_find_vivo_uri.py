"""
    test_find_vivo_uri.py -- return the first VIVO URI that staisfies a
    match on predicate and value

    Version 0.1 MC 2014-03-25
    --  Initial version.

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"

print vt.find_vivo_uri("ufVivo:ufid","84808900") # Person from UFID
print vt.find_vivo_uri("vivo:eRACommonsId","mconlon") # Person from eRACommons
print vt.find_vivo_uri("vivo:orcidId","0000-0002-1304-8447") # person from ORCID
print vt.find_vivo_uri("ufVivo:ISNI","0000 0001 2193 2008") # No such predicate
print vt.find_vivo_uri("ufVivo:isni","0000 0001 2193 2008") # Org from ISNI
print vt.find_vivo_uri("bibo:issn","0028-4793") # Journal from ISSN
print vt.find_vivo_uri("bibo:issn","9876-5432") # No such ISSN
print vt.find_vivo_uri("bibo:pmid","12763083") # paper from PubMed ID

print datetime.now(),"Finished"
