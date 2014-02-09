"""
    test_catalyst_pmid_request.py -- use the Harvard web service to find
    pmid that may be the work of the indicated author

    Version 0.1 MC 2013-12-28
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"

print "\nMike Conlon",vt.catalyst_pmid_request("Michael","","Conlon","mconlon@ufl.eedu")
print "\nCarl Pepine",vt.catalyst_pmid_request("Carl","J","Pepine","pepincj@ufl.edu")
print "\nArt Edison",vt.catalyst_pmid_request("Arthur","Scott","Edison","aedison@ufl.edu")
print "\nLinda Cottler",vt.catalyst_pmid_request("Linda","B","Cottler","lbcottler@ufl.edu")

print datetime.now(),"Finish"
