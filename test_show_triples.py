"""
    test_show_triples.py -- print a tabular result from the returns of get_triples

    Version 0.1 MC 2013-12-27
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

#  Test cases for access and display functions

print "\nDateTime"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n7860108656"))


print "\nDateTimeInterval"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n182882417"))

print "\nOrganization"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n8763427"))


print "\nAuthorship"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n148010391"))

print "\nRole"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n1864549239"))


print "\nPerson"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n39051"))

print "\nNot Found"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/notfound"))

print "\nPublication Venue"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n378789540"))

print "\nPaper"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n4703866415"))

print "\nGrant"
print vt.show_triples(vt.get_triples("http://vivo.ufl.edu/individual/n614029206"))

