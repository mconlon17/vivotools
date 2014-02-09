"""
    test_hr_abbrev_to_words.py -- Given an HR abbreviation for a job title,
    resolve the various HR abbreviations to full text words.

    Version 0.1 MC 2013-12-27
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"
before = "SR TECH"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "ASS PROF"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "HLT MGR 3"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "GRD STUD"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "ADMIN AST"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "JR COMM SPC"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "VP"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "IT CLRK"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "BIO CHEM"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "AGRIC MSTR"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
before = "FIN ANAL"
print "Before = ",before,"After = ",vt.hr_abbrev_to_words(before)
print datetime.now(),"Finish"

