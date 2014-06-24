"""
    test_get_types.py -- Given a URI, get the types

    Version 0.1 MC 2014-06-21
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2014, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

#  Test cases for access and display functions

print "\nDateTime"
print vt.get_types("http://vivo.ufl.edu/individual/n7860108656")


print "\nDateTimeInterval"
print vt.get_types("http://vivo.ufl.edu/individual/n182882417")

print "\nOrganization"
print vt.get_types("http://vivo.ufl.edu/individual/n8763427")


print "\nAuthorship"
print vt.get_types("http://vivo.ufl.edu/individual/n148010391")

print "\nRole"
print vt.get_types("http://vivo.ufl.edu/individual/n1864549239")

print "\nPerson"
print vt.get_types("http://vivo.ufl.edu/individual/n39051")

print "\nNot Found"
print vt.get_types("http://vivo.ufl.edu/notfound")

print "\nPublication Venue"
print vt.get_types("http://vivo.ufl.edu/individual/n378789540")

print "\nPaper"
print vt.get_types("http://vivo.ufl.edu/individual/n4703866415")

print "\nGrant"
print vt.get_types("http://vivo.ufl.edu/individual/n614029206")

