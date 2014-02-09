"""
    test_get_pmid_from_doi.py -- Given a doi, use Entrez to find the PMID at
    PubMed

    Version 0.1 MC 2013-12-28
    --  Initial version
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"
print vt.get_pmid_from_doi("10.1016/j.arcmed.2006.09.002")
print vt.get_pmid_from_doi("unfindable")
print vt.get_pmid_from_doi("10.1111/j.1365-2036.2010.04512.x")
print datetime.now(),"Finish"
