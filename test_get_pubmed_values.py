"""
    test_get_pubmed_values.py -- Given a doi, use Entrez to get the pubmed
    values from PubMed

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
print "\n",vt.get_pubmed_values("10.1111/j.1752-8062.2011.00348.x",debug=True)
print "\n",vt.get_pubmed_values("10.1016/j.arcmed.2006.09.002")
print "\n",vt.get_pubmed_values("unfindable")
print "\n",vt.get_pubmed_values("10.1111/j.1365-2036.2010.04512.x")
print datetime.now(),"Finish"
