"""
    test_untag_predicate.py -- given a tagged predicate such as "owl:Thing",
    return a full URI predciate such as http://www.w3.org/2002/07/owl#Thing

    Version 0.1 MC 2014-06-03
    --  Initial version.
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

from vivotools import untag_predicate
from datetime import datetime

print datetime.now(),"Start"
print untag_predicate("owl:Thing")
print untag_predicate("ufVivo:Course")
print untag_predicate("skos:Concept")
print untag_predicate("vivo:FacultyMember")
print datetime.now(),"Finish"

