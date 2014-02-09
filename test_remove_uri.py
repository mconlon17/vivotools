"""
    test_remove_uri.py -- given an entity URI, shoe the RDF that will remove
    refeerences to that entity

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

print "\nDateTime"
print vt.get_datetime_value("http://vivo.ufl.edu/individual/n7860108656")
print vt.remove_uri("http://vivo.ufl.edu/individual/n7860108656")


print "\nDateTimeInterval"
print vt.get_datetime_interval("http://vivo.ufl.edu/individual/n182882417")
print vt.remove_uri("http://vivo.ufl.edu/individual/n182882417")

print "\nOrganization"
print vt.get_organization("http://vivo.ufl.edu/individual/n182882417")
print vt.remove_uri("http://vivo.ufl.edu/individual/n182882417")


print "\nAuthorship"
print vt.get_authorship("http://vivo.ufl.edu/individual/n148010391")
print vt.remove_uri("http://vivo.ufl.edu/individual/n148010391")

print "\nRole"
print vt.get_role("http://vivo.ufl.edu/individual/n1864549239")
print vt.remove_uri("http://vivo.ufl.edu/individual/n1864549239")


print "\nPerson"
print vt.get_person("http://vivo.ufl.edu/individual/n39051")
print vt.remove_uri("http://vivo.ufl.edu/individual/n39051")

print "\nNot Found"
print vt.remove_uri("http://vivo.ufl.edu/notfound")

print "\nPublication Venue"
print vt.get_publication("http://vivo.ufl.edu/individual/n378789540")
print vt.remove_uri("http://vivo.ufl.edu/individual/n378789540")

print "\nGrant"
print vt.get_grant("http://vivo.ufl.edu/individual/n614029206")
print vt.remove_uri("http://vivo.ufl.edu/individual/n614029206")

print "\nWebpage"
print vt.get_webpage("http://vivo.ufl.edu/individual/n104143")
print vt.remove_uri("http://vivo.ufl.edu/individual/n104143")

print datetime.now(),"Finish"
